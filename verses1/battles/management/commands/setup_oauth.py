"""
Management command to setup OAuth providers (Google and GitHub)
Run: python manage.py setup_oauth
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os


class Command(BaseCommand):
    help = 'Setup OAuth providers for Google and GitHub'

    def handle(self, *args, **options):
        # Update the default site
        site, _ = Site.objects.get_or_create(id=1)
        site.domain = os.environ.get('SITE_DOMAIN', 'localhost:8000')
        site.name = 'Verses1'
        site.save()
        self.stdout.write(f'Site updated: {site.domain}')

        # Setup Google OAuth
        google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        google_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
        
        if google_client_id and google_secret:
            google_app, created = SocialApp.objects.update_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': google_client_id,
                    'secret': google_secret,
                }
            )
            google_app.sites.add(site)
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} Google OAuth app'))
        else:
            self.stdout.write(self.style.WARNING(
                'Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.'
            ))

        # Setup GitHub OAuth
        github_client_id = os.environ.get('GITHUB_CLIENT_ID', '')
        github_secret = os.environ.get('GITHUB_CLIENT_SECRET', '')
        
        if github_client_id and github_secret:
            github_app, created = SocialApp.objects.update_or_create(
                provider='github',
                defaults={
                    'name': 'GitHub',
                    'client_id': github_client_id,
                    'secret': github_secret,
                }
            )
            github_app.sites.add(site)
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} GitHub OAuth app'))
        else:
            self.stdout.write(self.style.WARNING(
                'GitHub OAuth not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment variables.'
            ))

        self.stdout.write(self.style.SUCCESS('\nOAuth setup complete!'))
        self.stdout.write('\nTo configure OAuth providers:')
        self.stdout.write('1. Google: https://console.cloud.google.com/apis/credentials')
        self.stdout.write('   - Create OAuth 2.0 Client ID')
        self.stdout.write('   - Add redirect URI: http://localhost:8000/accounts/google/login/callback/')
        self.stdout.write('   - For production: https://your-domain.com/accounts/google/login/callback/')
        self.stdout.write('')
        self.stdout.write('2. GitHub: https://github.com/settings/developers')
        self.stdout.write('   - Create new OAuth App')
        self.stdout.write('   - Add callback URL: http://localhost:8000/accounts/github/login/callback/')
        self.stdout.write('   - For production: https://your-domain.com/accounts/github/login/callback/')
