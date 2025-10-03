import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'verses1.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from battles.models import Battle, CodeSubmission, BattleResult
from django.core.files.uploadedfile import SimpleUploadedFile

client1 = Client()
client2 = Client()

username1 = 'tester1'
password1 = 'testpass123'
email1 = 'tester1@example.com'

username2 = 'tester2'
password2 = 'testpass123'
email2 = 'tester2@example.com'

print('--- Smoke test start ---')


resp = client1.post('/register/', data={
    'username': username1,
    'email': email1,
    'password1': password1,
    'password2': password1,
}, follow=True)
print('Register user1 status:', resp.status_code)


resp = client1.post('/login/', data={'username': username1, 'password': password1}, follow=True)
print('Login user1 status:', resp.status_code)


resp = client1.post('/battle/create/', data={}, follow=True)
print('Create battle status:', resp.status_code)


try:
    battle = Battle.objects.filter(creator__username=username1).latest('created_at')
    print('Battle created with code:', battle.battle_code, 'id:', battle.id)
except Exception as e:
    print('Failed to find battle:', e)
    raise SystemExit(1)


if not User.objects.filter(username=username2).exists():
    User.objects.create_user(username=username2, email=email2, password=password2)

resp = client2.post('/login/', data={'username': username2, 'password': password2}, follow=True)
print('Login user2 status:', resp.status_code)


resp = client2.post('/battle/join/', data={'battle_code': battle.battle_code}, follow=True)
print('Join battle status:', resp.status_code)


code1 = b"def add(a,b):\n    return a+b\n\nprint(add(1,2))\n"
code2 = b"def add(a,b):\n    s = 0\n    for i in range(a):\n        s += b\n    print(s)\n"

file1 = SimpleUploadedFile('code1.py', code1, content_type='text/x-python')
file2 = SimpleUploadedFile('code2.py', code2, content_type='text/x-python')


resp = client1.post(f'/battle/{battle.id}/', data={'code_file': file1}, follow=True)
print('User1 submit status:', resp.status_code)


resp = client2.post(f'/battle/{battle.id}/', data={'code_file': file2}, follow=True)
print('User2 submit status:', resp.status_code)


battle.refresh_from_db()
try:
    result = BattleResult.objects.get(battle=battle)
    winner = battle.winner.username if battle.winner else 'No winner set'
    print('BattleResult created. Winner:', winner)
    print('Complexity comparison snippet:', result.complexity_comparison[:200])
    print('Performance comparison snippet:', result.performance_comparison[:200])
    print('Readability comparison snippet:', result.readability_comparison[:200])
    print('Winner submission total score:', result.winner_submission.total_score)
except BattleResult.DoesNotExist:
    print('BattleResult not created yet.')

print('--- Smoke test end ---')
