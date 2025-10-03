from django.contrib import admin
from .models import Battle, CodeSubmission, BattleResult, LoginActivity


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
	list_display = ('user', 'timestamp', 'ip_address')
	list_filter = ('timestamp', 'user')
	search_fields = ('user__username', 'ip_address', 'user_agent')


admin.site.register(Battle)
admin.site.register(CodeSubmission)
admin.site.register(BattleResult)
