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
    code_file = models.FileField(upload_to='code_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Code analysis metrics
    complexity_score = models.FloatField(null=True, blank=True)
    performance_score = models.FloatField(null=True, blank=True)
    readability_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Submission by {self.user.username} for battle {self.battle.battle_code}"

class BattleResult(models.Model):
    battle = models.OneToOneField(Battle, on_delete=models.CASCADE)
    winner_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='won_battles', null=True, blank=True)
    loser_submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='lost_battles', null=True, blank=True)
    complexity_comparison = models.TextField()
    performance_comparison = models.TextField()
    readability_comparison = models.TextField()
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
