from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone

def generate_battle_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Battle(models.Model):
    battle_code = models.CharField(max_length=8, unique=True, default=generate_battle_code)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_battles')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_battles', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_battles')

    def __str__(self):
        return f"Battle {self.battle_code} - {self.creator.username} vs {self.opponent.username if self.opponent else 'Waiting'}"

class CodeSubmission(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_content = models.TextField(default='')
    code_file = models.FileField(upload_to='code_submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    complexity_score = models.FloatField(null=True, blank=True)
    performance_score = models.FloatField(null=True, blank=True)
    readability_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)

    cyclomatic_complexity = models.FloatField(null=True, blank=True)
    cognitive_complexity = models.FloatField(null=True, blank=True)
    maintainability_index = models.FloatField(null=True, blank=True)
    halstead_volume = models.FloatField(null=True, blank=True)
    halstead_difficulty = models.FloatField(null=True, blank=True)
    halstead_effort = models.FloatField(null=True, blank=True)

    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.FloatField(null=True, blank=True)
    cpu_usage = models.FloatField(null=True, blank=True)
    time_complexity_estimate = models.CharField(max_length=20, null=True, blank=True)

    pylint_score = models.FloatField(null=True, blank=True)
    flake8_score = models.FloatField(null=True, blank=True)
    documentation_score = models.FloatField(null=True, blank=True)

    vulnerability_score = models.FloatField(null=True, blank=True)
    security_issues_count = models.IntegerField(default=0)
    security_issues_details = models.JSONField(null=True, blank=True)

    lines_of_code = models.IntegerField(null=True, blank=True)
    functions_count = models.IntegerField(null=True, blank=True)
    classes_count = models.IntegerField(null=True, blank=True)
    imports_count = models.IntegerField(null=True, blank=True)

    analysis_completed = models.BooleanField(default=False)
    analysis_error = models.TextField(null=True, blank=True)
    analysis_version = models.CharField(max_length=10, default='1.0')

    def __str__(self):
        return f"Submission by {self.user.username} for battle {self.battle.battle_code}"

    def get_advanced_score(self) -> float:
        """Calculate advanced total score using weighted metrics"""
        weights = {
            'complexity': 0.20,
            'performance': 0.30,
            'quality': 0.25,
            'security': 0.15,
            'structure': 0.10
        }

        scores = []

        if self.maintainability_index is not None:
            complexity_score = min(100, self.maintainability_index)
            scores.append((complexity_score, weights['complexity']))

        perf_score = 0
        perf_count = 0
        if self.execution_time is not None:
            perf_score += max(0, 100 - self.execution_time * 20)
            perf_count += 1
        if self.memory_usage is not None:
            perf_score += max(0, 100 - self.memory_usage * 2)
            perf_count += 1
        if self.cpu_usage is not None:
            perf_score += max(0, 100 - self.cpu_usage)
            perf_count += 1
        if perf_count > 0:
            scores.append((perf_score / perf_count, weights['performance']))

        quality_score = 0
        quality_count = 0
        if self.pylint_score is not None:
            quality_score += self.pylint_score * 10
            quality_count += 1
        if self.flake8_score is not None:
            quality_score += self.flake8_score * 10
            quality_count += 1
        if self.documentation_score is not None:
            quality_score += self.documentation_score
            quality_count += 1
        if quality_count > 0:
            scores.append((quality_score / quality_count, weights['quality']))

        if self.vulnerability_score is not None:
            scores.append((self.vulnerability_score, weights['security']))

        if self.lines_of_code and self.functions_count:
            avg_function_size = self.lines_of_code / max(1, self.functions_count)
            structure_score = max(0, 100 - (avg_function_size - 20))
            scores.append((structure_score, weights['structure']))

        if not scores:
            return 0.0

        total_weighted_score = sum(score * weight for score, weight in scores)
        total_weight = sum(weight for _, weight in scores)

        return total_weighted_score / total_weight if total_weight > 0 else 0.0

class BattleResult(models.Model):
    battle = models.OneToOneField(Battle, on_delete=models.CASCADE)
    winner_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='won_battles', null=True, blank=True)
    loser_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='lost_battles', null=True, blank=True)
    
    complexity_comparison = models.TextField()
    performance_comparison = models.TextField()
    readability_comparison = models.TextField()
    
    detailed_comparison = models.JSONField(null=True, blank=True)
    winner_score = models.FloatField(null=True, blank=True)
    loser_score = models.FloatField(null=True, blank=True)
    score_difference = models.FloatField(null=True, blank=True)
    
    complexity_winner = models.ForeignKey(CodeSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name='complexity_wins')
    performance_winner = models.ForeignKey(CodeSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name='performance_wins')
    quality_winner = models.ForeignKey(CodeSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name='quality_wins')
    security_winner = models.ForeignKey(CodeSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_wins')
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_draw = models.BooleanField(default=False)

    def __str__(self):
        return f"Result for battle {self.battle.battle_code}"


class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Login: {self.user.username} @ {self.timestamp.isoformat()}"
