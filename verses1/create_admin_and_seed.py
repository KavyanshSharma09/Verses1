import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'verses1.settings')
django.setup()

from django.contrib.auth.models import User
from battles.models import Battle, CodeSubmission

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'adminpass123'
ADMIN_EMAIL = 'admin@example.com'

if not User.objects.filter(username=ADMIN_USERNAME).exists():
    User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
    print('Admin user created')
else:
    print('Admin user already exists')

# create demo users
for i in range(1,3):
    username = f'demo{i}'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, f'{username}@example.com', 'testpass123')
        print('Created user', username)

# Create a demo battle if none exists
if not Battle.objects.exists():
    creator = User.objects.filter(username='demo1').first()
    opponent = User.objects.filter(username='demo2').first()
    if creator and opponent:
        b = Battle.objects.create(creator=creator, opponent=opponent)
        print('Created demo battle', b.battle_code)

print('Seeding complete')
