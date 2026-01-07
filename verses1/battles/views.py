from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .forms import UserRegistrationForm, BattleCreationForm, CodeSubmissionForm, BattleJoinForm
from .models import Battle, CodeSubmission, BattleResult, ProblemStatement, Category, PracticeSubmission, UserStats
from .models import LoginActivity
from django.contrib.admin.views.decorators import staff_member_required
from . import utils
from django.http import JsonResponse
from django.urls import reverse
import json

def home(request):
    # Show available problems on home page
    problems = ProblemStatement.objects.filter(is_active=True).order_by('difficulty', 'title')[:6]
    categories = Category.objects.all()[:8]
    return render(request, "home.html", {
        'featured_problems': problems,
        'categories': categories,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserStats for new user
            UserStats.objects.get_or_create(user=user)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def problem_list(request):
    """List all available problems with category filtering"""
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    problems = ProblemStatement.objects.filter(is_active=True)
    
    if category_slug:
        problems = problems.filter(categories__slug=category_slug)
    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    
    problems = problems.order_by('difficulty', 'title').distinct()
    categories = Category.objects.all()
    
    # Get user's solved problems
    solved_problems = []
    if request.user.is_authenticated:
        solved_problems = list(
            PracticeSubmission.objects.filter(
                user=request.user, 
                all_tests_passed=True
            ).values_list('problem_id', flat=True).distinct()
        )
    
    return render(request, 'battles/problem_list.html', {
        'problems': problems,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'solved_problems': solved_problems,
    })


@login_required
def problem_detail(request, slug):
    """View problem details"""
    problem = get_object_or_404(ProblemStatement, slug=slug, is_active=True)
    visible_tests = problem.get_visible_test_cases()
    
    # Check if user has solved this problem
    user_solved = PracticeSubmission.objects.filter(
        user=request.user,
        problem=problem,
        all_tests_passed=True
    ).exists()
    
    return render(request, 'battles/problem_detail.html', {
        'problem': problem,
        'visible_tests': visible_tests,
        'user_solved': user_solved,
    })


@login_required
def create_battle(request):
    if request.method == 'POST':
        form = BattleCreationForm(request.POST)
        if form.is_valid():
            battle = form.save(commit=False)
            battle.creator = request.user
            battle.save()
            messages.success(request, f'Battle created! Share code: {battle.battle_code}')
            return redirect('battle_detail', battle_id=battle.id)
    else:
        form = BattleCreationForm()
    
    problems = ProblemStatement.objects.filter(is_active=True).order_by('difficulty', 'title')
    return render(request, 'battles/create_battle.html', {'form': form, 'problems': problems})

@login_required
def join_battle(request):
    if request.method == 'POST':
        form = BattleJoinForm(request.POST, user=request.user)
        if form.is_valid():
            battle = Battle.objects.get(battle_code=form.cleaned_data['battle_code'])
            battle.opponent = request.user
            battle.save()
            messages.success(request, 'Successfully joined the battle!')
            return redirect('battle_detail', battle_id=battle.id)
    else:
        form = BattleJoinForm(user=request.user)
    return render(request, 'battles/join_battle.html', {'form': form})

@login_required
def battle_detail(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    
    # Check if user is part of this battle
    if request.user != battle.creator and request.user != battle.opponent:
        messages.error(request, 'You are not a participant in this battle.')
        return redirect('home')
    
    # Get user's submission if exists
    user_submission = battle.submissions.filter(user=request.user, all_tests_passed=True).first()
    user_has_submitted = user_submission is not None
    
    # Get problem and visible test cases
    problem = battle.problem
    visible_tests = problem.get_visible_test_cases()
    
    context = {
        'battle': battle,
        'problem': problem,
        'visible_tests': visible_tests,
        'submissions': battle.submissions.filter(all_tests_passed=True),
        'user_has_submitted': user_has_submitted,
        'user_submission': user_submission,
        'starter_code': problem.starter_code or f"{problem.function_signature}\n    # Write your code here\n    pass",
    }
    return render(request, 'battles/battle_detail.html', context)


@login_required
def run_tests(request, battle_id):
    """AJAX endpoint to run code against test cases"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    battle = get_object_or_404(Battle, id=battle_id)
    
    # Check if user is part of this battle
    if request.user != battle.creator and request.user != battle.opponent:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)
        
        # Import code runner
        from .code_runner import run_tests as execute_tests, execution_result_to_dict
        
        # Get all test cases for the problem
        test_cases = list(battle.problem.get_all_test_cases())
        
        # Run tests
        result = execute_tests(code, battle.problem, test_cases)
        
        return JsonResponse(execution_result_to_dict(result))
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def submit_code(request, battle_id):
    """Submit code after all tests pass"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    battle = get_object_or_404(Battle, id=battle_id)
    
    # Check if user is part of this battle
    if request.user != battle.creator and request.user != battle.opponent:
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    # Check if user already submitted
    if battle.submissions.filter(user=request.user, all_tests_passed=True).exists():
        return JsonResponse({'error': 'You have already submitted code for this battle'}, status=400)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)
        
        # Import code runner and analysis engine
        from .code_runner import run_tests as execute_tests, execution_result_to_dict
        from .analysis_engine import analyze_code
        
        # Get all test cases
        test_cases = list(battle.problem.get_all_test_cases())
        
        # Run tests first
        test_result = execute_tests(code, battle.problem, test_cases)
        
        if not test_result.all_passed:
            return JsonResponse({
                'error': 'All tests must pass before submitting',
                'test_result': execution_result_to_dict(test_result)
            }, status=400)
        
        # Analyze code
        analysis = analyze_code(code)
        
        # Create submission
        submission = CodeSubmission.objects.create(
            battle=battle,
            user=request.user,
            code_content=code,
            tests_passed=test_result.tests_passed,
            tests_total=test_result.tests_total,
            all_tests_passed=True,
            test_results=execution_result_to_dict(test_result),
            avg_execution_time=test_result.avg_execution_time,
            max_memory_used=test_result.max_memory_used,
            complexity_score=analysis.complexity_score,
            performance_score=analysis.performance_score,
            readability_score=analysis.readability_score,
            total_score=analysis.total_score,
            cyclomatic_complexity=analysis.cyclomatic_complexity,
            cognitive_complexity=analysis.cognitive_complexity,
            maintainability_index=analysis.maintainability_index,
            lines_of_code=analysis.lines_of_code,
            functions_count=analysis.functions_count,
            classes_count=analysis.classes_count,
            time_complexity_estimate=analysis.time_complexity,
        )
        
        # Check if both users have submitted
        valid_submissions = battle.submissions.filter(all_tests_passed=True)
        if valid_submissions.count() == 2:
            # Determine winner based on analysis scores
            sub1, sub2 = list(valid_submissions)
            
            comparisons = utils.compare_submissions(sub1, sub2)
            
            # Calculate final scores (weighted: execution time + code quality)
            def calculate_final_score(sub):
                # Lower execution time is better (convert to score)
                time_score = max(0, 100 - (sub.avg_execution_time or 0) * 50)
                # Analysis score
                analysis_score = sub.total_score or 0
                # Weighted combination
                return time_score * 0.4 + analysis_score * 0.6
            
            score1 = calculate_final_score(sub1)
            score2 = calculate_final_score(sub2)
            
            import math
            if math.isclose(score1, score2, rel_tol=0.01):
                # Draw
                result = BattleResult.objects.create(
                    battle=battle,
                    winner_submission=None,
                    loser_submission=None,
                    complexity_comparison=comparisons['complexity'],
                    performance_comparison=comparisons['performance'],
                    readability_comparison=comparisons['readability'],
                    winner_score=score1,
                    loser_score=score2,
                    is_draw=True,
                )
                battle.winner = None
            else:
                winner_sub = sub1 if score1 > score2 else sub2
                loser_sub = sub2 if score1 > score2 else sub1
                
                result = BattleResult.objects.create(
                    battle=battle,
                    winner_submission=winner_sub,
                    loser_submission=loser_sub,
                    complexity_comparison=comparisons['complexity'],
                    performance_comparison=comparisons['performance'],
                    readability_comparison=comparisons['readability'],
                    winner_score=max(score1, score2),
                    loser_score=min(score1, score2),
                    score_difference=abs(score1 - score2),
                    is_draw=False,
                )
                battle.winner = winner_sub.user
            
            battle.is_completed = True
            battle.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Code submitted! Battle completed!',
                'battle_completed': True,
                'result_url': reverse('battle_result', args=[battle.id])
            })
        
        return JsonResponse({
            'success': True,
            'message': 'Code submitted successfully! Waiting for opponent.',
            'battle_completed': False
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@login_required
def battle_result(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    result = get_object_or_404(BattleResult, battle=battle)
    
    # Get both submissions
    submissions = battle.submissions.filter(all_tests_passed=True)
    
    return render(request, 'battles/battle_result.html', {
        'battle': battle, 
        'result': result,
        'submissions': submissions,
    })


@login_required
def battle_status(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    
    # Get submission status for both users
    creator_submitted = battle.submissions.filter(user=battle.creator, all_tests_passed=True).exists()
    opponent_submitted = battle.submissions.filter(user=battle.opponent, all_tests_passed=True).exists() if battle.opponent else False
    
    # Determine current user's opponent
    if request.user == battle.creator:
        opponent_name = battle.opponent.username if battle.opponent else None
        opponent_has_submitted = opponent_submitted
        user_has_submitted = creator_submitted
    else:
        opponent_name = battle.creator.username
        opponent_has_submitted = creator_submitted
        user_has_submitted = opponent_submitted
    
    data = {
        'opponent_joined': bool(battle.opponent),
        'opponent_name': opponent_name,
        'is_completed': bool(battle.is_completed),
        'winner': battle.winner.username if battle.winner else None,
        'result_url': reverse('battle_result', args=[battle.id]),
        'creator_submitted': creator_submitted,
        'opponent_submitted': opponent_submitted,
        'user_has_submitted': user_has_submitted,
        'opponent_has_submitted': opponent_has_submitted,
        'submissions_count': battle.submissions.filter(all_tests_passed=True).count(),
    }
    return JsonResponse(data)

@login_required
def battle_history(request):
    user_battles = Battle.objects.filter(is_completed=True).filter(
        models.Q(creator=request.user) | models.Q(opponent=request.user)
    ).order_by('-created_at')
    
    battle_rows = []
    for b in user_battles:
        try:
            res = BattleResult.objects.get(battle=b)
        except BattleResult.DoesNotExist:
            res = None
        battle_rows.append({'battle': b, 'result': res})

    return render(request, 'battles/battle_history.html', {'battle_rows': battle_rows})


@staff_member_required
def login_activity(request):
    recent = LoginActivity.objects.select_related('user').order_by('-timestamp')[:200]
    return render(request, 'battles/login_activity.html', {'activities': recent})


@login_required
def analyze_code_preview(request):
    """AJAX endpoint to preview code analysis before submission"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    import json
    from .analysis_engine import analyze_code
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        
        if not code.strip():
            return JsonResponse({'error': 'No code provided'}, status=400)
        
        result = analyze_code(code)
        
        return JsonResponse({
            'is_valid': result.is_valid,
            'syntax_error': result.syntax_error,
            'total_score': round(result.total_score, 2),
            'complexity_score': round(result.complexity_score, 2),
            'performance_score': round(result.performance_score, 2),
            'readability_score': round(result.readability_score, 2),
            'security_score': round(result.security_score, 2),
            'style_score': round(result.style_score, 2),
            'cyclomatic_complexity': result.cyclomatic_complexity,
            'cognitive_complexity': result.cognitive_complexity,
            'maintainability_index': round(result.maintainability_index, 2),
            'time_complexity': result.time_complexity,
            'space_complexity': result.space_complexity,
            'lines_of_code': result.lines_of_code,
            'functions_count': result.functions_count,
            'classes_count': result.classes_count,
            'issues': result.issues[:10],  # Limit to 10 issues
            'security_issues': result.security_issues[:5],  # Limit to 5 security issues
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============ PRACTICE MODE VIEWS ============

@login_required
def practice(request):
    """Practice mode - list problems to solve solo"""
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    problems = ProblemStatement.objects.filter(is_active=True)
    
    if category_slug:
        problems = problems.filter(categories__slug=category_slug)
    if difficulty:
        problems = problems.filter(difficulty=difficulty)
    
    problems = problems.order_by('difficulty', 'title').distinct()
    categories = Category.objects.all()
    
    # Get user's solved problems
    solved_problems = list(
        PracticeSubmission.objects.filter(
            user=request.user, 
            all_tests_passed=True
        ).values_list('problem_id', flat=True).distinct()
    )
    
    # Get user stats
    user_stats, _ = UserStats.objects.get_or_create(user=request.user)
    
    return render(request, 'battles/practice.html', {
        'problems': problems,
        'categories': categories,
        'current_category': category_slug,
        'current_difficulty': difficulty,
        'solved_problems': solved_problems,
        'user_stats': user_stats,
    })


@login_required
def practice_problem(request, slug):
    """Practice a specific problem"""
    problem = get_object_or_404(ProblemStatement, slug=slug, is_active=True)
    visible_tests = problem.get_visible_test_cases()
    
    # Check if user has solved this problem
    user_solved = PracticeSubmission.objects.filter(
        user=request.user,
        problem=problem,
        all_tests_passed=True
    ).exists()
    
    # Get user's previous submissions for this problem
    user_submissions = PracticeSubmission.objects.filter(
        user=request.user,
        problem=problem
    ).order_by('-submitted_at')[:5]
    
    starter_code = problem.starter_code or f"{problem.function_signature}\n    # Write your code here\n    pass"
    
    return render(request, 'battles/practice_problem.html', {
        'problem': problem,
        'visible_tests': visible_tests,
        'user_submissions': user_submissions,
        'user_solved': user_solved,
        'starter_code': starter_code,
    })


@login_required
def practice_run_tests(request, slug):
    """AJAX endpoint to run code against test cases in practice mode"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    problem = get_object_or_404(ProblemStatement, slug=slug, is_active=True)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)
        
        from .code_runner import run_tests as execute_tests, execution_result_to_dict
        
        test_cases = list(problem.get_all_test_cases())
        result = execute_tests(code, problem, test_cases)
        
        return JsonResponse(execution_result_to_dict(result))
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def practice_submit(request, slug):
    """Submit practice solution"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    problem = get_object_or_404(ProblemStatement, slug=slug, is_active=True)
    
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'error': 'No code provided'}, status=400)
        
        from .code_runner import run_tests as execute_tests, execution_result_to_dict
        from .analysis_engine import analyze_code
        
        test_cases = list(problem.get_all_test_cases())
        test_result = execute_tests(code, problem, test_cases)
        
        if not test_result.all_passed:
            return JsonResponse({
                'error': 'All tests must pass before submitting',
                'test_result': execution_result_to_dict(test_result)
            }, status=400)
        
        # Analyze code
        analysis = analyze_code(code)
        
        # Check if this is a first-time solve
        previously_solved = PracticeSubmission.objects.filter(
            user=request.user,
            problem=problem,
            all_tests_passed=True
        ).exists()
        
        # Create submission
        submission = PracticeSubmission.objects.create(
            user=request.user,
            problem=problem,
            code_content=code,
            tests_passed=test_result.tests_passed,
            tests_total=test_result.tests_total,
            all_tests_passed=True,
            test_results=execution_result_to_dict(test_result),
            avg_execution_time=test_result.avg_execution_time,
            complexity_score=analysis.complexity_score,
            performance_score=analysis.performance_score,
            total_score=analysis.total_score,
            time_complexity_estimate=analysis.time_complexity,
        )
        
        # Update user stats if first time solving
        if not previously_solved:
            user_stats, _ = UserStats.objects.get_or_create(user=request.user)
            user_stats.problems_solved += 1
            if problem.difficulty == 'easy':
                user_stats.easy_solved += 1
            elif problem.difficulty == 'medium':
                user_stats.medium_solved += 1
            else:
                user_stats.hard_solved += 1
            user_stats.save()
        
        return JsonResponse({
            'success': True,
            'all_passed': True,
            'message': 'Solution accepted!' if not previously_solved else 'Solution submitted!',
            'first_solve': not previously_solved,
            'score': analysis.total_score,
            'tests_passed': test_result.tests_passed,
            'tests_total': test_result.tests_total,
            'execution_time': test_result.avg_execution_time,
            'max_memory': test_result.max_memory_used,
            'complexity_score': analysis.complexity_score,
            'performance_score': analysis.performance_score,
            'time_complexity': analysis.time_complexity,
            'test_results': [
                {
                    'test_id': tr.test_id,
                    'passed': tr.passed,
                    'input_data': tr.input_data,
                    'expected_output': tr.expected_output,
                    'actual_output': tr.actual_output,
                    'execution_time': tr.execution_time,
                    'error_message': tr.error_message,
                }
                for tr in test_result.test_results
            ]
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)


@login_required
def submission_history(request, slug):
    """View submission history for a specific problem"""
    problem = get_object_or_404(ProblemStatement, slug=slug, is_active=True)
    
    submissions = PracticeSubmission.objects.filter(
        user=request.user,
        problem=problem
    ).order_by('-submitted_at')
    
    return render(request, 'battles/submission_history.html', {
        'problem': problem,
        'submissions': submissions,
    })


@login_required
def submission_detail(request, submission_id):
    """View a specific submission with code"""
    submission = get_object_or_404(
        PracticeSubmission, 
        id=submission_id, 
        user=request.user
    )
    
    return render(request, 'battles/submission_detail.html', {
        'submission': submission,
        'problem': submission.problem,
    })


@login_required
def all_submissions(request):
    """View all submissions across all problems"""
    submissions = PracticeSubmission.objects.filter(
        user=request.user
    ).select_related('problem').order_by('-submitted_at')
    
    # Group by problem for summary
    problem_stats = {}
    for sub in submissions:
        if sub.problem_id not in problem_stats:
            problem_stats[sub.problem_id] = {
                'problem': sub.problem,
                'total': 0,
                'passed': 0,
                'latest': sub,
            }
        problem_stats[sub.problem_id]['total'] += 1
        if sub.all_tests_passed:
            problem_stats[sub.problem_id]['passed'] += 1
    
    return render(request, 'battles/all_submissions.html', {
        'submissions': submissions[:50],  # Latest 50
        'problem_stats': problem_stats.values(),
        'total_submissions': submissions.count(),
    })


@login_required
def user_profile(request, username=None):
    """User profile dashboard with stats and activity"""
    from django.db.models import Avg, Count, Q
    from django.db.models.functions import TruncDate
    from datetime import timedelta
    from django.utils import timezone
    
    # Get profile user (self or another user)
    if username:
        from django.contrib.auth.models import User
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    is_own_profile = profile_user == request.user
    
    # Get or create user stats
    user_stats, _ = UserStats.objects.get_or_create(user=profile_user)
    
    # Battle statistics
    battles_as_creator = Battle.objects.filter(creator=profile_user, is_completed=True)
    battles_as_opponent = Battle.objects.filter(opponent=profile_user, is_completed=True)
    all_battles = battles_as_creator | battles_as_opponent
    
    # Update stats if needed
    total_battles = all_battles.count()
    wins = Battle.objects.filter(winner=profile_user, is_completed=True).count()
    draws = BattleResult.objects.filter(battle__in=all_battles, is_draw=True).count()
    losses = total_battles - wins - draws
    
    # Update user stats
    user_stats.battles_played = total_battles
    user_stats.battles_won = wins
    user_stats.battles_lost = losses
    user_stats.battles_drawn = draws
    user_stats.save()
    
    # Practice statistics - count unique solved problems
    solved_problem_ids = PracticeSubmission.objects.filter(
        user=profile_user, 
        all_tests_passed=True
    ).values_list('problem_id', flat=True).distinct()
    
    solved_problem_ids = list(set(solved_problem_ids))  # Ensure unique
    
    # Count by difficulty
    easy_count = ProblemStatement.objects.filter(id__in=solved_problem_ids, difficulty='easy').count()
    medium_count = ProblemStatement.objects.filter(id__in=solved_problem_ids, difficulty='medium').count()
    hard_count = ProblemStatement.objects.filter(id__in=solved_problem_ids, difficulty='hard').count()
    
    user_stats.problems_solved = easy_count + medium_count + hard_count
    user_stats.easy_solved = easy_count
    user_stats.medium_solved = medium_count
    user_stats.hard_solved = hard_count
    user_stats.save()
    
    # Recent activity (last 10 items)
    recent_battles = all_battles.order_by('-created_at')[:5]
    recent_practice = PracticeSubmission.objects.filter(
        user=profile_user
    ).select_related('problem').order_by('-submitted_at')[:5]
    
    # Combine and sort recent activity
    activity = []
    for battle in recent_battles:
        is_winner = battle.winner == profile_user
        is_draw = hasattr(battle, 'battleresult') and battle.battleresult.is_draw
        activity.append({
            'type': 'battle',
            'date': battle.created_at,
            'title': f"Battle vs {battle.opponent.username if battle.creator == profile_user else battle.creator.username}",
            'problem': battle.problem.title if battle.problem else 'Unknown',
            'result': 'draw' if is_draw else ('won' if is_winner else 'lost'),
            'link': f'/battle/{battle.id}/result/'
        })
    
    for submission in recent_practice:
        activity.append({
            'type': 'practice',
            'date': submission.submitted_at,
            'title': submission.problem.title,
            'problem': submission.problem.title,
            'result': 'solved' if submission.all_tests_passed else 'attempted',
            'link': f'/practice/{submission.problem.slug}/'
        })
    
    # Sort by date descending
    activity.sort(key=lambda x: x['date'], reverse=True)
    activity = activity[:10]
    
    # Submission heatmap data (last 365 days)
    today = timezone.now().date()
    year_ago = today - timedelta(days=365)
    
    # Get practice submissions by day
    daily_submissions = PracticeSubmission.objects.filter(
        user=profile_user,
        submitted_at__date__gte=year_ago
    ).annotate(
        date=TruncDate('submitted_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Create heatmap data
    heatmap_data = {str(item['date']): item['count'] for item in daily_submissions}
    
    # Calculate streak
    current_streak = 0
    check_date = today
    while True:
        date_str = str(check_date)
        if date_str in heatmap_data or PracticeSubmission.objects.filter(
            user=profile_user, 
            submitted_at__date=check_date
        ).exists():
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Best submission scores
    best_practice = PracticeSubmission.objects.filter(
        user=profile_user,
        all_tests_passed=True,
        total_score__isnull=False
    ).order_by('-total_score').first()
    
    # Categories solved
    categories_solved = Category.objects.filter(
        problems__id__in=solved_problem_ids
    ).annotate(
        solved_count=Count('problems', filter=Q(problems__id__in=solved_problem_ids))
    ).order_by('-solved_count')[:6]
    
    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'stats': user_stats,
        'activity': activity,
        'heatmap_data': json.dumps(heatmap_data),
        'current_streak': current_streak,
        'best_practice': best_practice,
        'categories_solved': categories_solved,
        'total_problems': ProblemStatement.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'battles/profile.html', context)
