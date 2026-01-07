"""
Management command to seed sample problems for Verses1
"""
from django.core.management.base import BaseCommand
from battles.models import ProblemStatement, TestCase


SAMPLE_PROBLEMS = [
    {
        'title': 'Two Sum',
        'slug': 'two-sum',
        'difficulty': 'easy',
        'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.''',
        'input_format': 'A list of integers nums and an integer target, passed as arguments to the function.',
        'output_format': 'Return a list of two indices.',
        'constraints': '''2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.''',
        'example_input': '[[2, 7, 11, 15], 9]',
        'example_output': '[0, 1]',
        'example_explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].',
        'function_signature': 'def two_sum(nums, target):',
        'starter_code': '''def two_sum(nums, target):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[2, 7, 11, 15], 9]', 'output': '[0, 1]', 'hidden': False, 'sample': True},
            {'input': '[[3, 2, 4], 6]', 'output': '[1, 2]', 'hidden': False, 'sample': True},
            {'input': '[[3, 3], 6]', 'output': '[0, 1]', 'hidden': False, 'sample': False},
            {'input': '[[1, 2, 3, 4, 5], 9]', 'output': '[3, 4]', 'hidden': True, 'sample': False},
            {'input': '[[-1, -2, -3, -4, -5], -8]', 'output': '[2, 4]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'FizzBuzz',
        'slug': 'fizzbuzz',
        'difficulty': 'easy',
        'description': '''Given an integer n, return a list of strings where:
- "FizzBuzz" if i is divisible by 3 and 5.
- "Fizz" if i is divisible by 3.
- "Buzz" if i is divisible by 5.
- i (as a string) if none of the above conditions are true.''',
        'input_format': 'An integer n.',
        'output_format': 'Return a list of strings.',
        'constraints': '1 <= n <= 10^4',
        'example_input': '[3]',
        'example_output': '["1", "2", "Fizz"]',
        'example_explanation': 'For n=3: 1 is "1", 2 is "2", 3 is divisible by 3 so "Fizz".',
        'function_signature': 'def fizzbuzz(n):',
        'starter_code': '''def fizzbuzz(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[3]', 'output': '["1", "2", "Fizz"]', 'hidden': False, 'sample': True},
            {'input': '[5]', 'output': '["1", "2", "Fizz", "4", "Buzz"]', 'hidden': False, 'sample': True},
            {'input': '[15]', 'output': '["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]', 'hidden': False, 'sample': False},
            {'input': '[1]', 'output': '["1"]', 'hidden': True, 'sample': False},
            {'input': '[30]', 'output': '["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz", "16", "17", "Fizz", "19", "Buzz", "Fizz", "22", "23", "Fizz", "Buzz", "26", "Fizz", "28", "29", "FizzBuzz"]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Reverse String',
        'slug': 'reverse-string',
        'difficulty': 'easy',
        'description': '''Write a function that reverses a string. The input string is given as a list of characters s.

You must do this by modifying the input list in-place with O(1) extra memory.''',
        'input_format': 'A list of characters s.',
        'output_format': 'Return the reversed list of characters.',
        'constraints': '''1 <= s.length <= 10^5
s[i] is a printable ascii character.''',
        'example_input': '[["h", "e", "l", "l", "o"]]',
        'example_output': '["o", "l", "l", "e", "h"]',
        'example_explanation': 'The input "hello" becomes "olleh" when reversed.',
        'function_signature': 'def reverse_string(s):',
        'starter_code': '''def reverse_string(s):
    # Modify s in-place and return it
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[["h", "e", "l", "l", "o"]]', 'output': '["o", "l", "l", "e", "h"]', 'hidden': False, 'sample': True},
            {'input': '[["H", "a", "n", "n", "a", "h"]]', 'output': '["h", "a", "n", "n", "a", "H"]', 'hidden': False, 'sample': True},
            {'input': '[["a"]]', 'output': '["a"]', 'hidden': True, 'sample': False},
            {'input': '[["a", "b"]]', 'output': '["b", "a"]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Valid Palindrome',
        'slug': 'valid-palindrome',
        'difficulty': 'easy',
        'description': '''A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.''',
        'input_format': 'A string s.',
        'output_format': 'Return true or false.',
        'constraints': '''1 <= s.length <= 2 * 10^5
s consists only of printable ASCII characters.''',
        'example_input': '["A man, a plan, a canal: Panama"]',
        'example_output': 'true',
        'example_explanation': '"amanaplanacanalpanama" is a palindrome.',
        'function_signature': 'def is_palindrome(s):',
        'starter_code': '''def is_palindrome(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["A man, a plan, a canal: Panama"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["race a car"]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[" "]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '["aa"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '["0P"]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Maximum Subarray',
        'slug': 'maximum-subarray',
        'difficulty': 'medium',
        'description': '''Given an integer array nums, find the subarray with the largest sum, and return its sum.

A subarray is a contiguous non-empty sequence of elements within an array.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the maximum sum as an integer.',
        'constraints': '''1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4''',
        'example_input': '[[-2, 1, -3, 4, -1, 2, 1, -5, 4]]',
        'example_output': '6',
        'example_explanation': 'The subarray [4, -1, 2, 1] has the largest sum = 6.',
        'function_signature': 'def max_subarray(nums):',
        'starter_code': '''def max_subarray(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[-2, 1, -3, 4, -1, 2, 1, -5, 4]]', 'output': '6', 'hidden': False, 'sample': True},
            {'input': '[[1]]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '[[5, 4, -1, 7, 8]]', 'output': '23', 'hidden': False, 'sample': False},
            {'input': '[[-1]]', 'output': '-1', 'hidden': True, 'sample': False},
            {'input': '[[-2, -1]]', 'output': '-1', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Binary Search',
        'slug': 'binary-search',
        'difficulty': 'easy',
        'description': '''Given a sorted array of distinct integers nums and a target value target, return the index if the target is found. If not, return -1.

You must write an algorithm with O(log n) runtime complexity.''',
        'input_format': 'A sorted list of integers nums and a target integer.',
        'output_format': 'Return the index of target, or -1 if not found.',
        'constraints': '''1 <= nums.length <= 10^4
-10^4 < nums[i], target < 10^4
All the integers in nums are unique.
nums is sorted in ascending order.''',
        'example_input': '[[-1, 0, 3, 5, 9, 12], 9]',
        'example_output': '4',
        'example_explanation': '9 exists in nums and its index is 4.',
        'function_signature': 'def binary_search(nums, target):',
        'starter_code': '''def binary_search(nums, target):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[-1, 0, 3, 5, 9, 12], 9]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[-1, 0, 3, 5, 9, 12], 2]', 'output': '-1', 'hidden': False, 'sample': True},
            {'input': '[[5], 5]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[[2, 5], 5]', 'output': '1', 'hidden': True, 'sample': False},
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample problems'

    def handle(self, *args, **options):
        self.stdout.write('Seeding problems...')
        
        for prob_data in SAMPLE_PROBLEMS:
            test_cases = prob_data.pop('test_cases')
            
            problem, created = ProblemStatement.objects.get_or_create(
                slug=prob_data['slug'],
                defaults=prob_data
            )
            
            if created:
                self.stdout.write(f'  Created problem: {problem.title}')
                
                # Create test cases
                for i, tc in enumerate(test_cases):
                    TestCase.objects.create(
                        problem=problem,
                        input_data=tc['input'],
                        expected_output=tc['output'],
                        is_hidden=tc['hidden'],
                        is_sample=tc['sample'],
                        order=i + 1,
                        points=10
                    )
                self.stdout.write(f'    Added {len(test_cases)} test cases')
            else:
                self.stdout.write(f'  Problem already exists: {problem.title}')
        
        self.stdout.write(self.style.SUCCESS('Done! Seeded sample problems.'))
