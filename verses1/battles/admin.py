from django.contrib import admin
from .models import (
    Battle, CodeSubmission, BattleResult, LoginActivity, 
    ProblemStatement, TestCase, Category, PracticeSubmission, UserStats
)


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 3
    fields = ['order', 'input_data', 'expected_output', 'is_hidden', 'is_sample', 'points']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(ProblemStatement)
class ProblemStatementAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'is_active', 'time_limit_seconds', 'created_at']
    list_filter = ['difficulty', 'is_active', 'categories']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']
    inlines = [TestCaseInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'difficulty', 'categories', 'is_active')
        }),
        ('Problem Description', {
            'fields': ('description', 'input_format', 'output_format', 'constraints')
        }),
        ('Example', {
            'fields': ('example_input', 'example_output', 'example_explanation')
        }),
        ('Code Setup', {
            'fields': ('function_signature', 'starter_code')
        }),
        ('Limits', {
            'fields': ('time_limit_seconds', 'memory_limit_mb')
        }),
    )


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['problem', 'order', 'is_hidden', 'is_sample', 'points']
    list_filter = ['problem', 'is_hidden', 'is_sample']


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'ip_address')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'ip_address', 'user_agent')


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['battle_code', 'problem', 'creator', 'opponent', 'is_completed', 'winner', 'created_at']
    list_filter = ['is_completed', 'problem']
    search_fields = ['battle_code', 'creator__username', 'opponent__username']


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['battle', 'user', 'all_tests_passed', 'tests_passed', 'tests_total', 'total_score', 'submitted_at']
    list_filter = ['all_tests_passed', 'battle']


@admin.register(BattleResult)
class BattleResultAdmin(admin.ModelAdmin):
    list_display = ['battle', 'is_draw', 'winner_score', 'loser_score', 'created_at']
    list_filter = ['is_draw']


@admin.register(PracticeSubmission)
class PracticeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'all_tests_passed', 'tests_passed', 'tests_total', 'submitted_at']
    list_filter = ['all_tests_passed', 'problem']
    search_fields = ['user__username', 'problem__title']


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'battles_played', 'battles_won', 'problems_solved']
    search_fields = ['user__username']
