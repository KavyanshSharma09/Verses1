"""
Management command to re-analyze existing code submissions with the advanced analyzer
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from battles.models import CodeSubmission, BattleResult
from battles import utils
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Re-analyze existing code submissions with advanced metrics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10,
            help='Number of submissions to process at a time'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )
        parser.add_argument(
            '--submission-id',
            type=int,
            help='Re-analyze only a specific submission'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        submission_id = options['submission_id']

        if submission_id:
            submissions = CodeSubmission.objects.filter(id=submission_id)
        else:
            # Only re-analyze submissions that haven't been analyzed with v2.0
            submissions = CodeSubmission.objects.exclude(analysis_version='2.0')

        total_submissions = submissions.count()
        self.stdout.write(f"Found {total_submissions} submissions to analyze")

        if dry_run:
            self.stdout.write("DRY RUN - No changes will be made")
            return

        processed = 0
        updated = 0

        for submission in submissions.iterator(chunk_size=batch_size):
            try:
                with transaction.atomic():
                    self.stdout.write(f"Analyzing submission {submission.id} by {submission.user.username}")

                    # Read the code file
                    code_content = submission.code_file.read().decode('utf-8')

                    # Perform comprehensive analysis
                    metrics = utils.analyze_code_comprehensive(code_content)

                    # Update submission with new metrics
                    submission.cyclomatic_complexity = metrics.cyclomatic_complexity
                    submission.cognitive_complexity = metrics.cognitive_complexity
                    submission.maintainability_index = metrics.maintainability_index
                    submission.halstead_volume = metrics.halstead_metrics.get('volume')
                    submission.halstead_difficulty = metrics.halstead_metrics.get('difficulty')
                    submission.halstead_effort = metrics.halstead_metrics.get('effort')

                    submission.execution_time = metrics.execution_time
                    submission.memory_usage = metrics.memory_usage
                    submission.cpu_usage = metrics.cpu_usage
                    submission.time_complexity_estimate = metrics.time_complexity_estimate

                    submission.pylint_score = metrics.pylint_score
                    submission.flake8_score = metrics.flake8_score
                    submission.documentation_score = metrics.documentation_score

                    submission.vulnerability_score = metrics.vulnerability_score
                    submission.security_issues_count = len(metrics.security_issues)
                    submission.security_issues_details = [issue for issue in metrics.security_issues]

                    submission.lines_of_code = metrics.lines_of_code
                    submission.functions_count = metrics.functions_count
                    submission.classes_count = metrics.classes_count
                    submission.imports_count = metrics.imports_count

                    submission.analysis_completed = True
                    submission.analysis_version = '2.0'

                    # Update legacy scores for backward compatibility
                    submission.complexity_score = metrics.maintainability_index or 0.0
                    submission.performance_score = max(0, 100 - (metrics.execution_time * 20)) if metrics.execution_time else 50.0
                    submission.readability_score = metrics.readability_score or 0.0
                    submission.total_score = submission.get_advanced_score()

                    submission.save()
                    updated += 1

                    # Update battle result if both submissions are complete
                    battle = submission.battle
                    if battle.submissions.count() == 2 and battle.is_completed:
                        self._update_battle_result(battle)

            except Exception as e:
                logger.error(f"Failed to analyze submission {submission.id}: {e}")
                submission.analysis_error = str(e)
                submission.save()

            processed += 1
            if processed % batch_size == 0:
                self.stdout.write(f"Processed {processed}/{total_submissions} submissions")

        self.stdout.write(
            self.style.SUCCESS(
                f"Analysis complete. Processed {processed} submissions, updated {updated}."
            )
        )

    def _update_battle_result(self, battle):
        """Update battle result with new comparison data"""
        try:
            submissions = list(battle.submissions.all())
            if len(submissions) != 2:
                return

            sub1, sub2 = submissions

            # Perform detailed comparison
            analyzer = utils.get_advanced_analyzer()
            comparison = analyzer.compare_submissions_detailed(
                utils.analyze_code_comprehensive(sub1.code_file.read().decode('utf-8')),
                utils.analyze_code_comprehensive(sub2.code_file.read().decode('utf-8'))
            )

            # Update or create battle result
            result, created = BattleResult.objects.get_or_create(
                battle=battle,
                defaults={
                    'complexity_comparison': utils.compare_submissions_legacy(sub1, sub2)['complexity'],
                    'performance_comparison': utils.compare_submissions_legacy(sub1, sub2)['performance'],
                    'readability_comparison': utils.compare_submissions_legacy(sub1, sub2)['readability'],
                }
            )

            # Update with new data
            score1 = sub1.get_advanced_score()
            score2 = sub2.get_advanced_score()

            import math
            if math.isclose(score1, score2, rel_tol=1e-9, abs_tol=1e-9):
                result.winner_submission = None
                result.loser_submission = None
                result.winner_score = score1
                result.loser_score = score2
                result.is_draw = True
                battle.winner = None
            else:
                winner_sub = sub1 if score1 > score2 else sub2
                loser_sub = sub2 if score1 > score2 else sub1
                result.winner_submission = winner_sub
                result.loser_submission = loser_sub
                result.winner_score = max(score1, score2)
                result.loser_score = min(score1, score2)
                result.score_difference = abs(score1 - score2)
                result.is_draw = False
                battle.winner = winner_sub.user

            # Update category winners
            result.complexity_winner = sub1 if comparison['categories']['complexity']['winner'] == 1 else (sub2 if comparison['categories']['complexity']['winner'] == 2 else None)
            result.performance_winner = sub1 if comparison['categories']['performance']['winner'] == 1 else (sub2 if comparison['categories']['performance']['winner'] == 2 else None)
            result.quality_winner = sub1 if comparison['categories']['quality']['winner'] == 1 else (sub2 if comparison['categories']['quality']['winner'] == 2 else None)
            result.security_winner = sub1 if comparison['categories']['security']['winner'] == 1 else (sub2 if comparison['categories']['security']['winner'] == 2 else None)

            result.detailed_comparison = comparison
            result.save()
            battle.save()

        except Exception as e:
            logger.error(f"Failed to update battle result for battle {battle.id}: {e}")