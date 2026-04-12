from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone

def generate_battle_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Category(models.Model):
    """Category/tag for problems"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="SVG icon class or name")
    color = models.CharField(max_length=7, default='#3b82f6', help_text="Hex color for the category")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProblemStatement(models.Model):
    """Problem that users solve in a battle"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text="Problem description in Markdown")
    input_format = models.TextField(help_text="Description of input format")
    output_format = models.TextField(help_text="Description of expected output format")
    constraints = models.TextField(help_text="Constraints (e.g., 1 <= n <= 10^5)")
    
    example_input = models.TextField(help_text="Example input to show users")
    example_output = models.TextField(help_text="Expected output for example")
    example_explanation = models.TextField(blank=True, help_text="Explanation of the example")
    
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    categories = models.ManyToManyField(Category, related_name='problems', blank=True)
    time_limit_seconds = models.FloatField(default=2.0, help_text="Time limit per test case")
    memory_limit_mb = models.IntegerField(default=256, help_text="Memory limit in MB")
    
    function_signature = models.CharField(
        max_length=200, 
        help_text="Function signature users must implement, e.g., 'def solution(nums, target):'"
    )
    starter_code = models.TextField(
        blank=True,
        help_text="Starter code template for users"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['difficulty', 'title']
        indexes = [
            models.Index(fields=['is_active', 'difficulty', 'title'], name='prob_active_diff_title_idx'),
        ]
    
    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"
    
    def get_visible_test_cases(self):
        return self.test_cases.filter(is_hidden=False)
    
    def get_all_test_cases(self):
        return self.test_cases.all()


class TestCase(models.Model):
    """Test case for a problem"""
    problem = models.ForeignKey(ProblemStatement, on_delete=models.CASCADE, related_name='test_cases')
    
    input_data = models.TextField(help_text="Input to pass to the function")
    expected_output = models.TextField(help_text="Expected output/return value")
    
    is_hidden = models.BooleanField(default=False, help_text="Hidden tests are not shown to users")
    is_sample = models.BooleanField(default=False, help_text="Sample tests shown in problem description")
    
    order = models.IntegerField(default=0, help_text="Order of test case execution")
    points = models.IntegerField(default=10, help_text="Points for passing this test")
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['problem', 'is_hidden', 'order'], name='tc_prob_hidden_order_idx'),
        ]
    
    def __str__(self):
        hidden_str = " (hidden)" if self.is_hidden else ""
        return f"Test {self.order} for {self.problem.title}{hidden_str}"


class Battle(models.Model):
    battle_code = models.CharField(max_length=8, unique=True, default=generate_battle_code)
    problem = models.ForeignKey(ProblemStatement, on_delete=models.CASCADE, related_name='battles', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_battles')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_battles', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_battles')

    class Meta:
        indexes = [
            models.Index(fields=['is_completed', 'created_at'], name='bat_complete_created_idx'),
            models.Index(fields=['creator', 'is_completed'], name='bat_creator_complete_idx'),
            models.Index(fields=['opponent', 'is_completed'], name='bat_opponent_complete_idx'),
        ]

    def __str__(self):
        problem_title = self.problem.title if self.problem else 'No Problem'
        return f"Battle {self.battle_code} - {problem_title} - {self.creator.username} vs {self.opponent.username if self.opponent else 'Waiting'}"


class CodeSubmission(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code_content = models.TextField(default='')
    code_file = models.FileField(upload_to='code_submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Test case results
    tests_passed = models.IntegerField(default=0)
    tests_total = models.IntegerField(default=0)
    all_tests_passed = models.BooleanField(default=False)
    test_results = models.JSONField(null=True, blank=True, help_text="Detailed results for each test case")
    avg_execution_time = models.FloatField(null=True, blank=True, help_text="Average execution time across tests")
    max_memory_used = models.FloatField(null=True, blank=True, help_text="Max memory used in MB")
    
    # Analysis scores
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

    class Meta:
        indexes = [
            models.Index(fields=['battle', 'all_tests_passed'], name='cs_battle_passed_idx'),
            models.Index(fields=['battle', 'user', 'all_tests_passed'], name='cs_battle_user_passed_idx'),
        ]

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

    class Meta:
        indexes = [
            models.Index(fields=['timestamp'], name='la_timestamp_idx'),
            models.Index(fields=['user', 'timestamp'], name='la_user_timestamp_idx'),
        ]

    def __str__(self):
        return f"Login: {self.user.username} @ {self.timestamp.isoformat()}"


class PracticeSubmission(models.Model):
    """Practice mode submission - solo problem solving"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_submissions')
    problem = models.ForeignKey(ProblemStatement, on_delete=models.CASCADE, related_name='practice_submissions')
    code_content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Test results
    tests_passed = models.IntegerField(default=0)
    tests_total = models.IntegerField(default=0)
    all_tests_passed = models.BooleanField(default=False)
    test_results = models.JSONField(null=True, blank=True)
    avg_execution_time = models.FloatField(null=True, blank=True)
    
    # Analysis scores (optional)
    complexity_score = models.FloatField(null=True, blank=True)
    performance_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    time_complexity_estimate = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', 'problem', 'submitted_at'], name='ps_user_prob_submitted_idx'),
            models.Index(fields=['user', 'all_tests_passed'], name='ps_user_passed_idx'),
        ]
    
    def __str__(self):
        status = "✓" if self.all_tests_passed else "✗"
        return f"{status} {self.user.username} - {self.problem.title}"


class UserStats(models.Model):
    """User statistics for leaderboard"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    
    # Battle stats
    battles_played = models.IntegerField(default=0)
    battles_won = models.IntegerField(default=0)
    battles_lost = models.IntegerField(default=0)
    battles_drawn = models.IntegerField(default=0)
    
    # Practice stats
    problems_solved = models.IntegerField(default=0)
    easy_solved = models.IntegerField(default=0)
    medium_solved = models.IntegerField(default=0)
    hard_solved = models.IntegerField(default=0)
    
    # Rating
    rating = models.IntegerField(default=1200)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.user.username}"
    
    @property
    def win_rate(self):
        if self.battles_played == 0:
            return 0
        return round((self.battles_won / self.battles_played) * 100, 1)
