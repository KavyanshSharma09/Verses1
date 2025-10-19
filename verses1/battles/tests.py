from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import LoginActivity
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Battle, CodeSubmission, BattleResult


class AuthActivityTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='tester', password='pass')
		self.staff = User.objects.create_user(username='admin', password='pass', is_staff=True)

	def test_login_creates_activity(self):
		resp = self.client.post(reverse('login'), {'username': 'tester', 'password': 'pass'})
		self.assertIn(resp.status_code, (302, 200))
		activities = LoginActivity.objects.filter(user=self.user)
		self.assertTrue(activities.exists())

	def test_logout_post_and_access(self):
		self.client.login(username='tester', password='pass')
		resp = self.client.post(reverse('logout'))
		self.assertEqual(resp.status_code, 302)

	def test_login_activity_view_requires_staff(self):
		self.client.login(username='tester', password='pass')
		resp = self.client.get(reverse('login_activity'))
		self.assertIn(resp.status_code, (302, 403))
		self.client.logout()
		self.client.login(username='admin', password='pass')
		resp = self.client.get(reverse('login_activity'))
		self.assertEqual(resp.status_code, 200)

	def test_draw_detection_via_view(self):
		battle = Battle.objects.create(creator=self.user)
		battle.opponent = self.staff
		battle.save()
		from battles import utils as utils_mod
		orig_complexity = utils_mod.analyze_code_complexity
		orig_performance = utils_mod.analyze_code_performance
		orig_readability = utils_mod.analyze_code_readability
		orig_total = utils_mod.calculate_total_score

		try:
			utils_mod.analyze_code_complexity = lambda s: 10.0
			utils_mod.analyze_code_performance = lambda s: 10.0
			utils_mod.analyze_code_readability = lambda s: 10.0
			utils_mod.calculate_total_score = lambda c,p,r: 30.0
			file_content = b"print('hello')\n"
			f1 = SimpleUploadedFile('a.py', file_content, content_type='text/x-python')
			f2 = SimpleUploadedFile('b.py', file_content, content_type='text/x-python')
			self.client.login(username='tester', password='pass')
			resp = self.client.post(reverse('battle_detail', args=[battle.id]), {'code_file': f1})
			self.assertIn(resp.status_code, (302, 200))
			self.client.logout()
			self.client.login(username='admin', password='pass')
			resp = self.client.post(reverse('battle_detail', args=[battle.id]), {'code_file': f2})
			self.assertIn(resp.status_code, (302, 200))
			battle.refresh_from_db()
			self.assertTrue(battle.is_completed)
			self.assertIsNone(battle.winner)
			result = BattleResult.objects.get(battle=battle)
			self.assertTrue(result.is_draw)
		finally:
			utils_mod.analyze_code_complexity = orig_complexity
			utils_mod.analyze_code_performance = orig_performance
			utils_mod.analyze_code_readability = orig_readability
			utils_mod.calculate_total_score = orig_total
