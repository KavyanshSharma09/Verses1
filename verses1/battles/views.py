from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .forms import UserRegistrationForm, BattleCreationForm, CodeSubmissionForm, BattleJoinForm
from .models import Battle, CodeSubmission, BattleResult
from .models import LoginActivity
from django.contrib.admin.views.decorators import staff_member_required
from . import utils
from django.http import JsonResponse
from django.urls import reverse

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

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
    return render(request, 'battles/create_battle.html', {'form': form})

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
    
    # Check if user already submitted
    user_has_submitted = battle.submissions.filter(user=request.user).exists()
    
    if request.method == 'POST' and 'code_file' in request.FILES:
        if user_has_submitted:
            messages.error(request, 'You have already submitted code for this battle.')
            return redirect('battle_detail', battle_id=battle.id)
        form = CodeSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.battle = battle
            submission.user = request.user
            code_content = submission.code_file.read().decode('utf-8')
            submission.complexity_score = utils.analyze_code_complexity(code_content)
            submission.performance_score = utils.analyze_code_performance(code_content)
            submission.readability_score = utils.analyze_code_readability(code_content)
            submission.total_score = utils.calculate_total_score(
                submission.complexity_score,
                submission.performance_score,
                submission.readability_score
            )
            submission.save()
            if battle.submissions.count() == 2:
                submissions = battle.submissions.all()
                sub1, sub2 = submissions[0], submissions[1]
                import math
                comparisons = utils.compare_submissions(sub1, sub2)
                a = float(sub1.total_score or 0)
                b = float(sub2.total_score or 0)
                if math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9):
                    
                    result = BattleResult.objects.create(
                        battle=battle,
                        winner_submission=None,
                        loser_submission=None,
                        complexity_comparison=comparisons['complexity'],
                        performance_comparison=comparisons['performance'],
                        readability_comparison=comparisons['readability'],
                        is_draw=True,
                    )
                    battle.winner = None
                else:
                    winner_sub = sub1 if sub1.total_score > sub2.total_score else sub2
                    loser_sub = sub2 if sub1.total_score > sub2.total_score else sub1
                    result = BattleResult.objects.create(
                        battle=battle,
                        winner_submission=winner_sub,
                        loser_submission=loser_sub,
                        complexity_comparison=comparisons['complexity'],
                        performance_comparison=comparisons['performance'],
                        readability_comparison=comparisons['readability'],
                        is_draw=False,
                    )
                    battle.winner = winner_sub.user

                battle.is_completed = True
                battle.save()
                
                return redirect('battle_result', battle_id=battle.id)
            
            messages.success(request, 'Code submitted successfully!')
            return redirect('battle_detail', battle_id=battle.id)
    else:
        form = CodeSubmissionForm()
    
    context = {
        'battle': battle,
        'form': form,
        'submissions': battle.submissions.all(),
        'user_has_submitted': user_has_submitted
    }
    return render(request, 'battles/battle_detail.html', context)

@login_required
def battle_result(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    result = get_object_or_404(BattleResult, battle=battle)
    return render(request, 'battles/battle_result.html', {'battle': battle, 'result': result})


@login_required
def battle_status(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    data = {
        'opponent_joined': bool(battle.opponent),
        'is_completed': bool(battle.is_completed),
        'winner': battle.winner.username if battle.winner else None,
        'result_url': reverse('battle_result', args=[battle.id])
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
