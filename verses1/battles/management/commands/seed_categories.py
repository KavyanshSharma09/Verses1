from django.core.management.base import BaseCommand
from battles.models import Category


class Command(BaseCommand):
    help = 'Seed initial problem categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Arrays',
                'slug': 'arrays',
                'description': 'Problems involving array manipulation, searching, and sorting',
                'icon': 'arrays',
                'color': '#3b82f6'
            },
            {
                'name': 'Strings',
                'slug': 'strings',
                'description': 'String manipulation, pattern matching, and text processing',
                'icon': 'strings',
                'color': '#10b981'
            },
            {
                'name': 'Math',
                'slug': 'math',
                'description': 'Mathematical computations and number theory',
                'icon': 'math',
                'color': '#f59e0b'
            },
            {
                'name': 'Dynamic Programming',
                'slug': 'dynamic-programming',
                'description': 'Optimization problems using memoization and tabulation',
                'icon': 'dynamic-programming',
                'color': '#8b5cf6'
            },
            {
                'name': 'Trees',
                'slug': 'trees',
                'description': 'Binary trees, BST, tree traversals, and tree algorithms',
                'icon': 'trees',
                'color': '#22c55e'
            },
            {
                'name': 'Graphs',
                'slug': 'graphs',
                'description': 'Graph traversal, shortest paths, and connectivity',
                'icon': 'graphs',
                'color': '#06b6d4'
            },
            {
                'name': 'Linked Lists',
                'slug': 'linked-lists',
                'description': 'Single and double linked list operations',
                'icon': 'linked-lists',
                'color': '#ec4899'
            },
            {
                'name': 'Stack & Queue',
                'slug': 'stack-queue',
                'description': 'Stack and queue data structure problems',
                'icon': 'stack-queue',
                'color': '#f97316'
            },
            {
                'name': 'Hash Table',
                'slug': 'hash-table',
                'description': 'Hashing, dictionaries, and frequency counting',
                'icon': 'hash-table',
                'color': '#14b8a6'
            },
            {
                'name': 'Recursion',
                'slug': 'recursion',
                'description': 'Recursive algorithms and backtracking',
                'icon': 'recursion',
                'color': '#a855f7'
            },
            {
                'name': 'Sorting',
                'slug': 'sorting',
                'description': 'Various sorting algorithms and their applications',
                'icon': 'sorting',
                'color': '#6366f1'
            },
            {
                'name': 'Binary Search',
                'slug': 'binary-search',
                'description': 'Binary search and its variations',
                'icon': 'binary-search',
                'color': '#0ea5e9'
            },
            {
                'name': 'Two Pointers',
                'slug': 'two-pointers',
                'description': 'Two pointer technique for array problems',
                'icon': 'two-pointers',
                'color': '#84cc16'
            },
            {
                'name': 'Greedy',
                'slug': 'greedy',
                'description': 'Greedy algorithms and optimization',
                'icon': 'greedy',
                'color': '#eab308'
            },
            {
                'name': 'Bit Manipulation',
                'slug': 'bit-manipulation',
                'description': 'Bitwise operations and binary representations',
                'icon': 'bit-manipulation',
                'color': '#ef4444'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for cat_data in categories:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                updated_count += 1
                self.stdout.write(f'Updated category: {category.name}')
        
        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count} new categories, updated {updated_count} existing.'
        ))
