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
    {
        'title': 'Merge Two Sorted Lists',
        'slug': 'merge-two-sorted-lists',
        'difficulty': 'easy',
        'description': '''You are given two sorted lists of integers. Merge them into a single sorted list and return it.

The merged list should be made by splicing together the elements of the two input lists in sorted order.''',
        'input_format': 'Two sorted lists of integers list1 and list2.',
        'output_format': 'Return a single sorted list containing all elements from both lists.',
        'constraints': '''0 <= list1.length, list2.length <= 50
-100 <= list1[i], list2[i] <= 100
Both list1 and list2 are sorted in non-decreasing order.''',
        'example_input': '[[1, 2, 4], [1, 3, 4]]',
        'example_output': '[1, 1, 2, 3, 4, 4]',
        'example_explanation': 'Merging [1,2,4] and [1,3,4] gives [1,1,2,3,4,4].',
        'function_signature': 'def merge_two_lists(list1, list2):',
        'starter_code': '''def merge_two_lists(list1, list2):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 4], [1, 3, 4]]', 'output': '[1, 1, 2, 3, 4, 4]', 'hidden': False, 'sample': True},
            {'input': '[[], []]', 'output': '[]', 'hidden': False, 'sample': True},
            {'input': '[[], [0]]', 'output': '[0]', 'hidden': False, 'sample': False},
            {'input': '[[1, 3, 5, 7], [2, 4, 6, 8]]', 'output': '[1, 2, 3, 4, 5, 6, 7, 8]', 'hidden': True, 'sample': False},
            {'input': '[[-5, -3, 0], [-4, -2, 1]]', 'output': '[-5, -4, -3, -2, 0, 1]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Climbing Stairs',
        'slug': 'climbing-stairs',
        'difficulty': 'easy',
        'description': '''You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?''',
        'input_format': 'An integer n representing the number of steps.',
        'output_format': 'Return the number of distinct ways to climb to the top.',
        'constraints': '1 <= n <= 45',
        'example_input': '[2]',
        'example_output': '2',
        'example_explanation': 'There are two ways to climb to the top: 1+1 or 2.',
        'function_signature': 'def climb_stairs(n):',
        'starter_code': '''def climb_stairs(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[2]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[3]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[5]', 'output': '8', 'hidden': True, 'sample': False},
            {'input': '[10]', 'output': '89', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Contains Duplicate',
        'slug': 'contains-duplicate',
        'difficulty': 'easy',
        'description': '''Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return true if duplicates exist, false otherwise.',
        'constraints': '''1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9''',
        'example_input': '[[1, 2, 3, 1]]',
        'example_output': 'true',
        'example_explanation': '1 appears twice in the array.',
        'function_signature': 'def contains_duplicate(nums):',
        'starter_code': '''def contains_duplicate(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3, 1]]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[1, 2, 3, 4]]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '[[1]]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '[[0, 0]]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Longest Common Prefix',
        'slug': 'longest-common-prefix',
        'difficulty': 'easy',
        'description': '''Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string "".''',
        'input_format': 'A list of strings strs.',
        'output_format': 'Return the longest common prefix as a string.',
        'constraints': '''1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters.''',
        'example_input': '[["flower", "flow", "flight"]]',
        'example_output': '"fl"',
        'example_explanation': '"fl" is the longest common prefix.',
        'function_signature': 'def longest_common_prefix(strs):',
        'starter_code': '''def longest_common_prefix(strs):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[["flower", "flow", "flight"]]', 'output': '"fl"', 'hidden': False, 'sample': True},
            {'input': '[["dog", "racecar", "car"]]', 'output': '""', 'hidden': False, 'sample': True},
            {'input': '[["a"]]', 'output': '"a"', 'hidden': False, 'sample': False},
            {'input': '[["", "b"]]', 'output': '""', 'hidden': True, 'sample': False},
            {'input': '[["interspecies", "interstellar", "interstate"]]', 'output': '"inters"', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Product of Array Except Self',
        'slug': 'product-of-array-except-self',
        'difficulty': 'medium',
        'description': '''Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return a list where each element is the product of all other elements.',
        'constraints': '''2 <= nums.length <= 10^5
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.''',
        'example_input': '[[1, 2, 3, 4]]',
        'example_output': '[24, 12, 8, 6]',
        'example_explanation': 'For index 0: 2*3*4=24, index 1: 1*3*4=12, etc.',
        'function_signature': 'def product_except_self(nums):',
        'starter_code': '''def product_except_self(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[1, 2, 3, 4]]', 'output': '[24, 12, 8, 6]', 'hidden': False, 'sample': True},
            {'input': '[[-1, 1, 0, -3, 3]]', 'output': '[0, 0, 9, 0, 0]', 'hidden': False, 'sample': True},
            {'input': '[[2, 3]]', 'output': '[3, 2]', 'hidden': False, 'sample': False},
            {'input': '[[1, 1, 1, 1]]', 'output': '[1, 1, 1, 1]', 'hidden': True, 'sample': False},
            {'input': '[[0, 0]]', 'output': '[0, 0]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Single Number',
        'slug': 'single-number',
        'difficulty': 'easy',
        'description': '''Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the single number that appears only once.',
        'constraints': '''1 <= nums.length <= 3 * 10^4
-3 * 10^4 <= nums[i] <= 3 * 10^4
Each element appears twice except for one.''',
        'example_input': '[[2, 2, 1]]',
        'example_output': '1',
        'example_explanation': '1 appears only once while 2 appears twice.',
        'function_signature': 'def single_number(nums):',
        'starter_code': '''def single_number(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[2, 2, 1]]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '[[4, 1, 2, 1, 2]]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[1]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[0, 1, 0]]', 'output': '1', 'hidden': True, 'sample': False},
            {'input': '[[-1, -1, -2]]', 'output': '-2', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Move Zeroes',
        'slug': 'move-zeroes',
        'difficulty': 'easy',
        'description': '''Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the modified list with zeroes moved to the end.',
        'constraints': '''1 <= nums.length <= 10^4
-2^31 <= nums[i] <= 2^31 - 1''',
        'example_input': '[[0, 1, 0, 3, 12]]',
        'example_output': '[1, 3, 12, 0, 0]',
        'example_explanation': 'All zeroes are moved to the end while maintaining order of other elements.',
        'function_signature': 'def move_zeroes(nums):',
        'starter_code': '''def move_zeroes(nums):
    # Modify nums in-place and return it
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[0, 1, 0, 3, 12]]', 'output': '[1, 3, 12, 0, 0]', 'hidden': False, 'sample': True},
            {'input': '[[0]]', 'output': '[0]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2, 3]]', 'output': '[1, 2, 3]', 'hidden': False, 'sample': False},
            {'input': '[[0, 0, 1]]', 'output': '[1, 0, 0]', 'hidden': True, 'sample': False},
            {'input': '[[4, 0, 5, 0, 6, 0, 7]]', 'output': '[4, 5, 6, 7, 0, 0, 0]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Plus One',
        'slug': 'plus-one',
        'difficulty': 'easy',
        'description': '''You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order.

Increment the large integer by one and return the resulting array of digits.''',
        'input_format': 'A list of integers digits representing a number.',
        'output_format': 'Return the list representing the number plus one.',
        'constraints': '''1 <= digits.length <= 100
0 <= digits[i] <= 9
digits does not contain any leading 0's.''',
        'example_input': '[[1, 2, 3]]',
        'example_output': '[1, 2, 4]',
        'example_explanation': 'The array represents 123. Adding one gives 124.',
        'function_signature': 'def plus_one(digits):',
        'starter_code': '''def plus_one(digits):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3]]', 'output': '[1, 2, 4]', 'hidden': False, 'sample': True},
            {'input': '[[4, 3, 2, 1]]', 'output': '[4, 3, 2, 2]', 'hidden': False, 'sample': True},
            {'input': '[[9]]', 'output': '[1, 0]', 'hidden': False, 'sample': False},
            {'input': '[[9, 9, 9]]', 'output': '[1, 0, 0, 0]', 'hidden': True, 'sample': False},
            {'input': '[[1, 9, 9]]', 'output': '[2, 0, 0]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Best Time to Buy and Sell Stock',
        'slug': 'best-time-to-buy-sell-stock',
        'difficulty': 'easy',
        'description': '''You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.''',
        'input_format': 'A list of integers prices representing stock prices.',
        'output_format': 'Return the maximum profit as an integer.',
        'constraints': '''1 <= prices.length <= 10^5
0 <= prices[i] <= 10^4''',
        'example_input': '[[7, 1, 5, 3, 6, 4]]',
        'example_output': '5',
        'example_explanation': 'Buy on day 2 (price=1) and sell on day 5 (price=6), profit = 6-1 = 5.',
        'function_signature': 'def max_profit(prices):',
        'starter_code': '''def max_profit(prices):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[7, 1, 5, 3, 6, 4]]', 'output': '5', 'hidden': False, 'sample': True},
            {'input': '[[7, 6, 4, 3, 1]]', 'output': '0', 'hidden': False, 'sample': True},
            {'input': '[[1, 2]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[2, 4, 1]]', 'output': '2', 'hidden': True, 'sample': False},
            {'input': '[[3, 2, 6, 5, 0, 3]]', 'output': '4', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Majority Element',
        'slug': 'majority-element',
        'difficulty': 'easy',
        'description': '''Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the majority element.',
        'constraints': '''n == nums.length
1 <= n <= 5 * 10^4
-10^9 <= nums[i] <= 10^9''',
        'example_input': '[[3, 2, 3]]',
        'example_output': '3',
        'example_explanation': '3 appears twice which is more than 3/2 = 1 time.',
        'function_signature': 'def majority_element(nums):',
        'starter_code': '''def majority_element(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[3, 2, 3]]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[[2, 2, 1, 1, 1, 2, 2]]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[[1]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[6, 5, 5]]', 'output': '5', 'hidden': True, 'sample': False},
            {'input': '[[1, 1, 1, 1, 2, 3, 4]]', 'output': '1', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Remove Duplicates from Sorted Array',
        'slug': 'remove-duplicates-sorted-array',
        'difficulty': 'easy',
        'description': '''Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.

Return the number of unique elements in nums.''',
        'input_format': 'A sorted list of integers nums.',
        'output_format': 'Return the count of unique elements.',
        'constraints': '''1 <= nums.length <= 3 * 10^4
-100 <= nums[i] <= 100
nums is sorted in non-decreasing order.''',
        'example_input': '[[1, 1, 2]]',
        'example_output': '2',
        'example_explanation': 'There are 2 unique elements: 1 and 2.',
        'function_signature': 'def remove_duplicates(nums):',
        'starter_code': '''def remove_duplicates(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 1, 2]]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]]', 'output': '5', 'hidden': False, 'sample': True},
            {'input': '[[1]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[-1, 0, 0, 0, 1, 2, 2]]', 'output': '4', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3, 4, 5]]', 'output': '5', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Rotate Array',
        'slug': 'rotate-array',
        'difficulty': 'medium',
        'description': '''Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.''',
        'input_format': 'A list of integers nums and an integer k.',
        'output_format': 'Return the rotated array.',
        'constraints': '''1 <= nums.length <= 10^5
-2^31 <= nums[i] <= 2^31 - 1
0 <= k <= 10^5''',
        'example_input': '[[1, 2, 3, 4, 5, 6, 7], 3]',
        'example_output': '[5, 6, 7, 1, 2, 3, 4]',
        'example_explanation': 'Rotate right by 3: [5,6,7,1,2,3,4].',
        'function_signature': 'def rotate(nums, k):',
        'starter_code': '''def rotate(nums, k):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3, 4, 5, 6, 7], 3]', 'output': '[5, 6, 7, 1, 2, 3, 4]', 'hidden': False, 'sample': True},
            {'input': '[[-1, -100, 3, 99], 2]', 'output': '[3, 99, -1, -100]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2], 3]', 'output': '[2, 1]', 'hidden': False, 'sample': False},
            {'input': '[[1], 0]', 'output': '[1]', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3], 4]', 'output': '[3, 1, 2]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Intersection of Two Arrays II',
        'slug': 'intersection-two-arrays-ii',
        'difficulty': 'easy',
        'description': '''Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must appear as many times as it shows in both arrays and you may return the result in any order.''',
        'input_format': 'Two lists of integers nums1 and nums2.',
        'output_format': 'Return a list of common elements (with duplicates).',
        'constraints': '''1 <= nums1.length, nums2.length <= 1000
0 <= nums1[i], nums2[i] <= 1000''',
        'example_input': '[[1, 2, 2, 1], [2, 2]]',
        'example_output': '[2, 2]',
        'example_explanation': '2 appears twice in both arrays.',
        'function_signature': 'def intersect(nums1, nums2):',
        'starter_code': '''def intersect(nums1, nums2):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 2, 1], [2, 2]]', 'output': '[2, 2]', 'hidden': False, 'sample': True},
            {'input': '[[4, 9, 5], [9, 4, 9, 8, 4]]', 'output': '[4, 9]', 'hidden': False, 'sample': True},
            {'input': '[[1], [1]]', 'output': '[1]', 'hidden': False, 'sample': False},
            {'input': '[[1, 2], [3, 4]]', 'output': '[]', 'hidden': True, 'sample': False},
            {'input': '[[3, 1, 2], [1, 1]]', 'output': '[1]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'First Unique Character in a String',
        'slug': 'first-unique-character',
        'difficulty': 'easy',
        'description': '''Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.''',
        'input_format': 'A string s.',
        'output_format': 'Return the index of the first unique character, or -1.',
        'constraints': '''1 <= s.length <= 10^5
s consists of only lowercase English letters.''',
        'example_input': '["leetcode"]',
        'example_output': '0',
        'example_explanation': 'The first unique character is "l" at index 0.',
        'function_signature': 'def first_uniq_char(s):',
        'starter_code': '''def first_uniq_char(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["leetcode"]', 'output': '0', 'hidden': False, 'sample': True},
            {'input': '["loveleetcode"]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '["aabb"]', 'output': '-1', 'hidden': False, 'sample': False},
            {'input': '["z"]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '["aadadaad"]', 'output': '-1', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Valid Anagram',
        'slug': 'valid-anagram',
        'difficulty': 'easy',
        'description': '''Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.''',
        'input_format': 'Two strings s and t.',
        'output_format': 'Return true if anagram, false otherwise.',
        'constraints': '''1 <= s.length, t.length <= 5 * 10^4
s and t consist of lowercase English letters.''',
        'example_input': '["anagram", "nagaram"]',
        'example_output': 'true',
        'example_explanation': '"nagaram" is an anagram of "anagram".',
        'function_signature': 'def is_anagram(s, t):',
        'starter_code': '''def is_anagram(s, t):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["anagram", "nagaram"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["rat", "car"]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '["a", "a"]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '["ab", "ba"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '["aacc", "ccac"]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Count and Say',
        'slug': 'count-and-say',
        'difficulty': 'medium',
        'description': '''The count-and-say sequence is a sequence of digit strings defined by the recursive formula:
- countAndSay(1) = "1"
- countAndSay(n) is the way you would "say" the digit string from countAndSay(n-1)

To determine how you "say" a digit string, split it into groups of consecutive same digits. Then for each group, say the count followed by the digit.

Given a positive integer n, return the nth term of the count-and-say sequence.''',
        'input_format': 'An integer n.',
        'output_format': 'Return the nth term as a string.',
        'constraints': '1 <= n <= 30',
        'example_input': '[4]',
        'example_output': '"1211"',
        'example_explanation': 'countAndSay(1)="1", countAndSay(2)="11", countAndSay(3)="21", countAndSay(4)="1211".',
        'function_signature': 'def count_and_say(n):',
        'starter_code': '''def count_and_say(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[1]', 'output': '"1"', 'hidden': False, 'sample': True},
            {'input': '[4]', 'output': '"1211"', 'hidden': False, 'sample': True},
            {'input': '[2]', 'output': '"11"', 'hidden': False, 'sample': False},
            {'input': '[5]', 'output': '"111221"', 'hidden': True, 'sample': False},
            {'input': '[6]', 'output': '"312211"', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Power of Three',
        'slug': 'power-of-three',
        'difficulty': 'easy',
        'description': '''Given an integer n, return true if it is a power of three. Otherwise, return false.

An integer n is a power of three if there exists an integer x such that n == 3^x.''',
        'input_format': 'An integer n.',
        'output_format': 'Return true if power of three, false otherwise.',
        'constraints': '-2^31 <= n <= 2^31 - 1',
        'example_input': '[27]',
        'example_output': 'true',
        'example_explanation': '27 = 3^3.',
        'function_signature': 'def is_power_of_three(n):',
        'starter_code': '''def is_power_of_three(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[27]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[0]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[9]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '[45]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '[1]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Roman to Integer',
        'slug': 'roman-to-integer',
        'difficulty': 'easy',
        'description': '''Roman numerals are represented by seven symbols: I, V, X, L, C, D and M.

Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

Given a roman numeral, convert it to an integer.''',
        'input_format': 'A string s representing a roman numeral.',
        'output_format': 'Return the integer value.',
        'constraints': '''1 <= s.length <= 15
s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
s is a valid roman numeral in the range [1, 3999].''',
        'example_input': '["III"]',
        'example_output': '3',
        'example_explanation': 'III = 3.',
        'function_signature': 'def roman_to_int(s):',
        'starter_code': '''def roman_to_int(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["III"]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '["LVIII"]', 'output': '58', 'hidden': False, 'sample': True},
            {'input': '["MCMXCIV"]', 'output': '1994', 'hidden': False, 'sample': False},
            {'input': '["IV"]', 'output': '4', 'hidden': True, 'sample': False},
            {'input': '["IX"]', 'output': '9', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Number of 1 Bits',
        'slug': 'number-of-1-bits',
        'difficulty': 'easy',
        'description': '''Write a function that takes an unsigned integer and returns the number of '1' bits it has (also known as the Hamming weight).''',
        'input_format': 'An integer n.',
        'output_format': 'Return the count of 1 bits.',
        'constraints': 'The input must be a non-negative integer.',
        'example_input': '[11]',
        'example_output': '3',
        'example_explanation': '11 in binary is 1011, which has three 1 bits.',
        'function_signature': 'def hamming_weight(n):',
        'starter_code': '''def hamming_weight(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[11]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[128]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '[255]', 'output': '8', 'hidden': False, 'sample': False},
            {'input': '[0]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[1023]', 'output': '10', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Missing Number',
        'slug': 'missing-number',
        'difficulty': 'easy',
        'description': '''Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the missing number.',
        'constraints': '''n == nums.length
1 <= n <= 10^4
0 <= nums[i] <= n
All the numbers of nums are unique.''',
        'example_input': '[[3, 0, 1]]',
        'example_output': '2',
        'example_explanation': 'n = 3, so the range is [0, 1, 2, 3]. 2 is missing.',
        'function_signature': 'def missing_number(nums):',
        'starter_code': '''def missing_number(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[3, 0, 1]]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[[0, 1]]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[[9, 6, 4, 2, 3, 5, 7, 0, 1]]', 'output': '8', 'hidden': False, 'sample': False},
            {'input': '[[0]]', 'output': '1', 'hidden': True, 'sample': False},
            {'input': '[[1]]', 'output': '0', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Reverse Bits',
        'slug': 'reverse-bits',
        'difficulty': 'easy',
        'description': '''Reverse the bits of a given 32-bit unsigned integer.''',
        'input_format': 'An integer n (treat as 32-bit unsigned).',
        'output_format': 'Return the integer with reversed bits.',
        'constraints': 'The input must be a 32-bit unsigned integer.',
        'example_input': '[43261596]',
        'example_output': '964176192',
        'example_explanation': '43261596 in binary is 00000010100101000001111010011100, reversed is 00111001011110000010100101000000 = 964176192.',
        'function_signature': 'def reverse_bits(n):',
        'starter_code': '''def reverse_bits(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[43261596]', 'output': '964176192', 'hidden': False, 'sample': True},
            {'input': '[4294967293]', 'output': '3221225471', 'hidden': False, 'sample': True},
            {'input': '[0]', 'output': '0', 'hidden': False, 'sample': False},
            {'input': '[1]', 'output': '2147483648', 'hidden': True, 'sample': False},
            {'input': '[2]', 'output': '1073741824', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Pascal\'s Triangle',
        'slug': 'pascals-triangle',
        'difficulty': 'easy',
        'description': '''Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it.''',
        'input_format': 'An integer numRows.',
        'output_format': 'Return a list of lists representing Pascal\'s triangle.',
        'constraints': '1 <= numRows <= 30',
        'example_input': '[5]',
        'example_output': '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]',
        'example_explanation': 'The first 5 rows of Pascal\'s triangle.',
        'function_signature': 'def generate(numRows):',
        'starter_code': '''def generate(numRows):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[5]', 'output': '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': '[[1]]', 'hidden': False, 'sample': True},
            {'input': '[2]', 'output': '[[1], [1, 1]]', 'hidden': False, 'sample': False},
            {'input': '[3]', 'output': '[[1], [1, 1], [1, 2, 1]]', 'hidden': True, 'sample': False},
            {'input': '[6]', 'output': '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'House Robber',
        'slug': 'house-robber',
        'difficulty': 'medium',
        'description': '''You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.''',
        'input_format': 'A list of integers nums representing money in each house.',
        'output_format': 'Return the maximum amount you can rob.',
        'constraints': '''1 <= nums.length <= 100
0 <= nums[i] <= 400''',
        'example_input': '[[1, 2, 3, 1]]',
        'example_output': '4',
        'example_explanation': 'Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 1 + 3 = 4.',
        'function_signature': 'def rob(nums):',
        'starter_code': '''def rob(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3, 1]]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[2, 7, 9, 3, 1]]', 'output': '12', 'hidden': False, 'sample': True},
            {'input': '[[2, 1, 1, 2]]', 'output': '4', 'hidden': False, 'sample': False},
            {'input': '[[1]]', 'output': '1', 'hidden': True, 'sample': False},
            {'input': '[[1, 2]]', 'output': '2', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Valid Parentheses',
        'slug': 'valid-parentheses',
        'difficulty': 'easy',
        'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.''',
        'input_format': 'A string s containing only parentheses characters.',
        'output_format': 'Return true if valid, false otherwise.',
        'constraints': '''1 <= s.length <= 10^4
s consists of parentheses only '()[]{}'.''',
        'example_input': '["()"]',
        'example_output': 'true',
        'example_explanation': 'The parentheses are properly matched.',
        'function_signature': 'def is_valid(s):',
        'starter_code': '''def is_valid(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["()"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["()[]{}"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["(]"]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '["([)]"]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '["{[]}"]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Palindrome Number',
        'slug': 'palindrome-number',
        'difficulty': 'easy',
        'description': '''Given an integer x, return true if x is a palindrome, and false otherwise.

An integer is a palindrome when it reads the same backward as forward.''',
        'input_format': 'An integer x.',
        'output_format': 'Return true if palindrome, false otherwise.',
        'constraints': '-2^31 <= x <= 2^31 - 1',
        'example_input': '[121]',
        'example_output': 'true',
        'example_explanation': '121 reads as 121 from left to right and from right to left.',
        'function_signature': 'def is_palindrome(x):',
        'starter_code': '''def is_palindrome(x):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[121]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[-121]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[10]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[12321]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '[0]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Sqrt(x)',
        'slug': 'sqrtx',
        'difficulty': 'easy',
        'description': '''Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.''',
        'input_format': 'A non-negative integer x.',
        'output_format': 'Return the integer square root of x.',
        'constraints': '0 <= x <= 2^31 - 1',
        'example_input': '[4]',
        'example_output': '2',
        'example_explanation': 'The square root of 4 is 2.',
        'function_signature': 'def my_sqrt(x):',
        'starter_code': '''def my_sqrt(x):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[4]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[8]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[0]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[16]', 'output': '4', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Search Insert Position',
        'slug': 'search-insert-position',
        'difficulty': 'easy',
        'description': '''Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.''',
        'input_format': 'A sorted list of integers nums and a target integer.',
        'output_format': 'Return the index of target or where it should be inserted.',
        'constraints': '''1 <= nums.length <= 10^4
-10^4 <= nums[i] <= 10^4
nums contains distinct values sorted in ascending order.
-10^4 <= target <= 10^4''',
        'example_input': '[[1, 3, 5, 6], 5]',
        'example_output': '2',
        'example_explanation': '5 is found at index 2.',
        'function_signature': 'def search_insert(nums, target):',
        'starter_code': '''def search_insert(nums, target):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 3, 5, 6], 5]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[[1, 3, 5, 6], 2]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '[[1, 3, 5, 6], 7]', 'output': '4', 'hidden': False, 'sample': False},
            {'input': '[[1, 3, 5, 6], 0]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[[1], 1]', 'output': '0', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Length of Last Word',
        'slug': 'length-of-last-word',
        'difficulty': 'easy',
        'description': '''Given a string s consisting of words and spaces, return the length of the last word in the string.

A word is a maximal substring consisting of non-space characters only.''',
        'input_format': 'A string s.',
        'output_format': 'Return the length of the last word.',
        'constraints': '''1 <= s.length <= 10^4
s consists of only English letters and spaces ' '.
There will be at least one word in s.''',
        'example_input': '["Hello World"]',
        'example_output': '5',
        'example_explanation': 'The last word is "World" with length 5.',
        'function_signature': 'def length_of_last_word(s):',
        'starter_code': '''def length_of_last_word(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["Hello World"]', 'output': '5', 'hidden': False, 'sample': True},
            {'input': '["   fly me   to   the moon  "]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '["luffy is still joyboy"]', 'output': '6', 'hidden': False, 'sample': False},
            {'input': '["a"]', 'output': '1', 'hidden': True, 'sample': False},
            {'input': '["day"]', 'output': '3', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Add Binary',
        'slug': 'add-binary',
        'difficulty': 'easy',
        'description': '''Given two binary strings a and b, return their sum as a binary string.''',
        'input_format': 'Two binary strings a and b.',
        'output_format': 'Return the sum as a binary string.',
        'constraints': '''1 <= a.length, b.length <= 10^4
a and b consist only of '0' or '1' characters.
Each string does not contain leading zeros except for the zero itself.''',
        'example_input': '["11", "1"]',
        'example_output': '"100"',
        'example_explanation': '11 + 1 = 100 in binary.',
        'function_signature': 'def add_binary(a, b):',
        'starter_code': '''def add_binary(a, b):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["11", "1"]', 'output': '"100"', 'hidden': False, 'sample': True},
            {'input': '["1010", "1011"]', 'output': '"10101"', 'hidden': False, 'sample': True},
            {'input': '["0", "0"]', 'output': '"0"', 'hidden': False, 'sample': False},
            {'input': '["1", "1"]', 'output': '"10"', 'hidden': True, 'sample': False},
            {'input': '["111", "111"]', 'output': '"1110"', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Excel Sheet Column Number',
        'slug': 'excel-sheet-column-number',
        'difficulty': 'easy',
        'description': '''Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.

For example:
A -> 1
B -> 2
...
Z -> 26
AA -> 27
AB -> 28
...''',
        'input_format': 'A string columnTitle.',
        'output_format': 'Return the column number as an integer.',
        'constraints': '''1 <= columnTitle.length <= 7
columnTitle consists only of uppercase English letters.
columnTitle is in the range ["A", "FXSHRXW"].''',
        'example_input': '["A"]',
        'example_output': '1',
        'example_explanation': 'A is the first column.',
        'function_signature': 'def title_to_number(columnTitle):',
        'starter_code': '''def title_to_number(columnTitle):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["A"]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '["AB"]', 'output': '28', 'hidden': False, 'sample': True},
            {'input': '["ZY"]', 'output': '701', 'hidden': False, 'sample': False},
            {'input': '["Z"]', 'output': '26', 'hidden': True, 'sample': False},
            {'input': '["AA"]', 'output': '27', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Happy Number',
        'slug': 'happy-number',
        'difficulty': 'easy',
        'description': '''Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:
- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.''',
        'input_format': 'A positive integer n.',
        'output_format': 'Return true if happy number, false otherwise.',
        'constraints': '1 <= n <= 2^31 - 1',
        'example_input': '[19]',
        'example_output': 'true',
        'example_explanation': '1^2 + 9^2 = 82, 8^2 + 2^2 = 68, 6^2 + 8^2 = 100, 1^2 + 0^2 + 0^2 = 1.',
        'function_signature': 'def is_happy(n):',
        'starter_code': '''def is_happy(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[19]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[2]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '[7]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '[4]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Isomorphic Strings',
        'slug': 'isomorphic-strings',
        'difficulty': 'easy',
        'description': '''Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.''',
        'input_format': 'Two strings s and t.',
        'output_format': 'Return true if isomorphic, false otherwise.',
        'constraints': '''1 <= s.length <= 5 * 10^4
t.length == s.length
s and t consist of any valid ascii character.''',
        'example_input': '["egg", "add"]',
        'example_output': 'true',
        'example_explanation': 'e maps to a, g maps to d.',
        'function_signature': 'def is_isomorphic(s, t):',
        'starter_code': '''def is_isomorphic(s, t):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["egg", "add"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["foo", "bar"]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '["paper", "title"]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '["a", "a"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '["badc", "baba"]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Reverse Linked List',
        'slug': 'reverse-linked-list',
        'difficulty': 'easy',
        'description': '''Given a list representing the values of a singly linked list, return the list reversed.

For simplicity, we represent the linked list as a Python list.''',
        'input_format': 'A list of integers representing linked list values.',
        'output_format': 'Return the reversed list.',
        'constraints': '''The number of nodes in the list is in range [0, 5000].
-5000 <= Node.val <= 5000''',
        'example_input': '[[1, 2, 3, 4, 5]]',
        'example_output': '[5, 4, 3, 2, 1]',
        'example_explanation': 'The list is reversed.',
        'function_signature': 'def reverse_list(head):',
        'starter_code': '''def reverse_list(head):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3, 4, 5]]', 'output': '[5, 4, 3, 2, 1]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2]]', 'output': '[2, 1]', 'hidden': False, 'sample': True},
            {'input': '[[]]', 'output': '[]', 'hidden': False, 'sample': False},
            {'input': '[[1]]', 'output': '[1]', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3]]', 'output': '[3, 2, 1]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Power of Two',
        'slug': 'power-of-two',
        'difficulty': 'easy',
        'description': '''Given an integer n, return true if it is a power of two. Otherwise, return false.

An integer n is a power of two if there exists an integer x such that n == 2^x.''',
        'input_format': 'An integer n.',
        'output_format': 'Return true if power of two, false otherwise.',
        'constraints': '-2^31 <= n <= 2^31 - 1',
        'example_input': '[1]',
        'example_output': 'true',
        'example_explanation': '2^0 = 1.',
        'function_signature': 'def is_power_of_two(n):',
        'starter_code': '''def is_power_of_two(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[1]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[16]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[3]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[0]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '[64]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Add Digits',
        'slug': 'add-digits',
        'difficulty': 'easy',
        'description': '''Given an integer num, repeatedly add all its digits until the result has only one digit, and return it.''',
        'input_format': 'An integer num.',
        'output_format': 'Return the single digit result.',
        'constraints': '0 <= num <= 2^31 - 1',
        'example_input': '[38]',
        'example_output': '2',
        'example_explanation': '3 + 8 = 11, 1 + 1 = 2.',
        'function_signature': 'def add_digits(num):',
        'starter_code': '''def add_digits(num):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[38]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[0]', 'output': '0', 'hidden': False, 'sample': True},
            {'input': '[9]', 'output': '9', 'hidden': False, 'sample': False},
            {'input': '[123]', 'output': '6', 'hidden': True, 'sample': False},
            {'input': '[999]', 'output': '9', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Ugly Number',
        'slug': 'ugly-number',
        'difficulty': 'easy',
        'description': '''An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.

Given an integer n, return true if n is an ugly number.''',
        'input_format': 'An integer n.',
        'output_format': 'Return true if ugly number, false otherwise.',
        'constraints': '-2^31 <= n <= 2^31 - 1',
        'example_input': '[6]',
        'example_output': 'true',
        'example_explanation': '6 = 2 × 3.',
        'function_signature': 'def is_ugly(n):',
        'starter_code': '''def is_ugly(n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[6]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[14]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[0]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '[8]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Word Pattern',
        'slug': 'word-pattern',
        'difficulty': 'easy',
        'description': '''Given a pattern and a string s, find if s follows the same pattern.

Here follow means a full match, such that there is a bijection between a letter in pattern and a non-empty word in s.''',
        'input_format': 'A pattern string and a string s with space-separated words.',
        'output_format': 'Return true if s follows the pattern, false otherwise.',
        'constraints': '''1 <= pattern.length <= 300
pattern contains only lower-case English letters.
1 <= s.length <= 3000
s contains only lowercase English letters and spaces.''',
        'example_input': '["abba", "dog cat cat dog"]',
        'example_output': 'true',
        'example_explanation': 'a->dog, b->cat forms a valid bijection.',
        'function_signature': 'def word_pattern(pattern, s):',
        'starter_code': '''def word_pattern(pattern, s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["abba", "dog cat cat dog"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '["abba", "dog cat cat fish"]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '["aaaa", "dog cat cat dog"]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '["abc", "b c a"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '["abba", "dog dog dog dog"]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Move Duplicates to End',
        'slug': 'move-duplicates-to-end',
        'difficulty': 'medium',
        'description': '''Given an array of integers, move all duplicate occurrences to the end of the array while maintaining the relative order of unique elements and duplicates.

Return the modified array.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the modified list.',
        'constraints': '''1 <= nums.length <= 10^4
-10^4 <= nums[i] <= 10^4''',
        'example_input': '[[1, 2, 2, 3, 3, 3, 4]]',
        'example_output': '[1, 2, 3, 4, 2, 3, 3]',
        'example_explanation': 'Unique elements first, then duplicates.',
        'function_signature': 'def move_duplicates(nums):',
        'starter_code': '''def move_duplicates(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 2, 3, 3, 3, 4]]', 'output': '[1, 2, 3, 4, 2, 3, 3]', 'hidden': False, 'sample': True},
            {'input': '[[1, 1, 1, 1]]', 'output': '[1, 1, 1, 1]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2, 3, 4]]', 'output': '[1, 2, 3, 4]', 'hidden': False, 'sample': False},
            {'input': '[[5, 5, 6, 6, 7]]', 'output': '[5, 6, 7, 5, 6]', 'hidden': True, 'sample': False},
            {'input': '[[1]]', 'output': '[1]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Group Anagrams',
        'slug': 'group-anagrams',
        'difficulty': 'medium',
        'description': '''Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once.''',
        'input_format': 'A list of strings strs.',
        'output_format': 'Return a list of lists, where each inner list contains anagrams.',
        'constraints': '''1 <= strs.length <= 10^4
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters.''',
        'example_input': '[["eat", "tea", "tan", "ate", "nat", "bat"]]',
        'example_output': '[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]',
        'example_explanation': 'Words are grouped by their sorted letters.',
        'function_signature': 'def group_anagrams(strs):',
        'starter_code': '''def group_anagrams(strs):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[["eat", "tea", "tan", "ate", "nat", "bat"]]', 'output': '[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]', 'hidden': False, 'sample': True},
            {'input': '[[""]]', 'output': '[[""]]', 'hidden': False, 'sample': True},
            {'input': '[["a"]]', 'output': '[["a"]]', 'hidden': False, 'sample': False},
            {'input': '[["abc", "bca", "cab", "xyz"]]', 'output': '[["xyz"], ["abc", "bca", "cab"]]', 'hidden': True, 'sample': False},
            {'input': '[["listen", "silent", "hello"]]', 'output': '[["hello"], ["listen", "silent"]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Spiral Matrix',
        'slug': 'spiral-matrix',
        'difficulty': 'medium',
        'description': '''Given an m x n matrix, return all elements of the matrix in spiral order.''',
        'input_format': 'A 2D list matrix.',
        'output_format': 'Return a list of elements in spiral order.',
        'constraints': '''m == matrix.length
n == matrix[i].length
1 <= m, n <= 10
-100 <= matrix[i][j] <= 100''',
        'example_input': '[[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]]',
        'example_output': '[1, 2, 3, 6, 9, 8, 7, 4, 5]',
        'example_explanation': 'Traverse the matrix in spiral order starting from top-left.',
        'function_signature': 'def spiral_order(matrix):',
        'starter_code': '''def spiral_order(matrix):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]]', 'output': '[1, 2, 3, 6, 9, 8, 7, 4, 5]', 'hidden': False, 'sample': True},
            {'input': '[[[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]]]', 'output': '[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]', 'hidden': False, 'sample': True},
            {'input': '[[[[1]]]]', 'output': '[1]', 'hidden': False, 'sample': False},
            {'input': '[[[[1, 2], [3, 4]]]]', 'output': '[1, 2, 4, 3]', 'hidden': True, 'sample': False},
            {'input': '[[[[1], [2], [3]]]]', 'output': '[1, 2, 3]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Jump Game',
        'slug': 'jump-game',
        'difficulty': 'medium',
        'description': '''You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return true if you can reach the last index, false otherwise.',
        'constraints': '''1 <= nums.length <= 10^4
0 <= nums[i] <= 10^5''',
        'example_input': '[[2, 3, 1, 1, 4]]',
        'example_output': 'true',
        'example_explanation': 'Jump 1 step from index 0 to 1, then 3 steps to the last index.',
        'function_signature': 'def can_jump(nums):',
        'starter_code': '''def can_jump(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[2, 3, 1, 1, 4]]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[3, 2, 1, 0, 4]]', 'output': 'false', 'hidden': False, 'sample': True},
            {'input': '[[0]]', 'output': 'true', 'hidden': False, 'sample': False},
            {'input': '[[2, 0, 0]]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '[[1, 1, 1, 1]]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Unique Paths',
        'slug': 'unique-paths',
        'difficulty': 'medium',
        'description': '''There is a robot on an m x n grid. The robot is initially located at the top-left corner. The robot tries to move to the bottom-right corner. The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.''',
        'input_format': 'Two integers m (rows) and n (columns).',
        'output_format': 'Return the number of unique paths.',
        'constraints': '1 <= m, n <= 100',
        'example_input': '[3, 7]',
        'example_output': '28',
        'example_explanation': 'From the top-left corner, there are 28 ways to reach the bottom-right corner.',
        'function_signature': 'def unique_paths(m, n):',
        'starter_code': '''def unique_paths(m, n):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[3, 7]', 'output': '28', 'hidden': False, 'sample': True},
            {'input': '[3, 2]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[1, 1]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[7, 3]', 'output': '28', 'hidden': True, 'sample': False},
            {'input': '[3, 3]', 'output': '6', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Set Matrix Zeroes',
        'slug': 'set-matrix-zeroes',
        'difficulty': 'medium',
        'description': '''Given an m x n integer matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.''',
        'input_format': 'A 2D list matrix.',
        'output_format': 'Return the modified matrix.',
        'constraints': '''m == matrix.length
n == matrix[0].length
1 <= m, n <= 200
-2^31 <= matrix[i][j] <= 2^31 - 1''',
        'example_input': '[[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]]]',
        'example_output': '[[1, 0, 1], [0, 0, 0], [1, 0, 1]]',
        'example_explanation': 'The element at [1][1] is 0, so row 1 and column 1 are set to 0.',
        'function_signature': 'def set_zeroes(matrix):',
        'starter_code': '''def set_zeroes(matrix):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]]]', 'output': '[[1, 0, 1], [0, 0, 0], [1, 0, 1]]', 'hidden': False, 'sample': True},
            {'input': '[[[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]]]', 'output': '[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]', 'hidden': False, 'sample': True},
            {'input': '[[[[1]]]]', 'output': '[[1]]', 'hidden': False, 'sample': False},
            {'input': '[[[[0]]]]', 'output': '[[0]]', 'hidden': True, 'sample': False},
            {'input': '[[[[1, 2], [3, 4]]]]', 'output': '[[1, 2], [3, 4]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Sort Colors',
        'slug': 'sort-colors',
        'difficulty': 'medium',
        'description': '''Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.''',
        'input_format': 'A list of integers nums containing only 0, 1, and 2.',
        'output_format': 'Return the sorted list.',
        'constraints': '''n == nums.length
1 <= n <= 300
nums[i] is either 0, 1, or 2.''',
        'example_input': '[[2, 0, 2, 1, 1, 0]]',
        'example_output': '[0, 0, 1, 1, 2, 2]',
        'example_explanation': 'Sort the colors: reds (0), whites (1), blues (2).',
        'function_signature': 'def sort_colors(nums):',
        'starter_code': '''def sort_colors(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[2, 0, 2, 1, 1, 0]]', 'output': '[0, 0, 1, 1, 2, 2]', 'hidden': False, 'sample': True},
            {'input': '[[2, 0, 1]]', 'output': '[0, 1, 2]', 'hidden': False, 'sample': True},
            {'input': '[[0]]', 'output': '[0]', 'hidden': False, 'sample': False},
            {'input': '[[1, 1, 1]]', 'output': '[1, 1, 1]', 'hidden': True, 'sample': False},
            {'input': '[[2, 2, 0, 0, 1, 1]]', 'output': '[0, 0, 1, 1, 2, 2]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Subsets',
        'slug': 'subsets',
        'difficulty': 'medium',
        'description': '''Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.''',
        'input_format': 'A list of unique integers nums.',
        'output_format': 'Return a list of all subsets.',
        'constraints': '''1 <= nums.length <= 10
-10 <= nums[i] <= 10
All the numbers of nums are unique.''',
        'example_input': '[[1, 2, 3]]',
        'example_output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]',
        'example_explanation': 'All possible subsets of [1, 2, 3].',
        'function_signature': 'def subsets(nums):',
        'starter_code': '''def subsets(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 2, 3]]', 'output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]', 'hidden': False, 'sample': True},
            {'input': '[[0]]', 'output': '[[], [0]]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2]]', 'output': '[[], [1], [2], [1, 2]]', 'hidden': False, 'sample': False},
            {'input': '[[1]]', 'output': '[[], [1]]', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3, 4]]', 'output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Word Search',
        'slug': 'word-search',
        'difficulty': 'medium',
        'description': '''Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.''',
        'input_format': 'A 2D list board and a string word.',
        'output_format': 'Return true if word exists, false otherwise.',
        'constraints': '''m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consists of only lowercase and uppercase English letters.''',
        'example_input': '[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"]',
        'example_output': 'true',
        'example_explanation': 'The word ABCCED can be found in the grid.',
        'function_signature': 'def exist(board, word):',
        'starter_code': '''def exist(board, word):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[[["A"]], "A"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '[[["A", "A"]], "AA"]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Coin Change',
        'slug': 'coin-change',
        'difficulty': 'medium',
        'description': '''You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.''',
        'input_format': 'A list of integers coins and an integer amount.',
        'output_format': 'Return the minimum number of coins, or -1.',
        'constraints': '''1 <= coins.length <= 12
1 <= coins[i] <= 2^31 - 1
0 <= amount <= 10^4''',
        'example_input': '[[1, 2, 5], 11]',
        'example_output': '3',
        'example_explanation': '11 = 5 + 5 + 1.',
        'function_signature': 'def coin_change(coins, amount):',
        'starter_code': '''def coin_change(coins, amount):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[1, 2, 5], 11]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[[2], 3]', 'output': '-1', 'hidden': False, 'sample': True},
            {'input': '[[1], 0]', 'output': '0', 'hidden': False, 'sample': False},
            {'input': '[[1, 2, 5], 100]', 'output': '20', 'hidden': True, 'sample': False},
            {'input': '[[1], 1]', 'output': '1', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Longest Increasing Subsequence',
        'slug': 'longest-increasing-subsequence',
        'difficulty': 'medium',
        'description': '''Given an integer array nums, return the length of the longest strictly increasing subsequence.''',
        'input_format': 'A list of integers nums.',
        'output_format': 'Return the length of the longest increasing subsequence.',
        'constraints': '''1 <= nums.length <= 2500
-10^4 <= nums[i] <= 10^4''',
        'example_input': '[[10, 9, 2, 5, 3, 7, 101, 18]]',
        'example_output': '4',
        'example_explanation': 'The longest increasing subsequence is [2, 3, 7, 101] with length 4.',
        'function_signature': 'def length_of_lis(nums):',
        'starter_code': '''def length_of_lis(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[10, 9, 2, 5, 3, 7, 101, 18]]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[0, 1, 0, 3, 2, 3]]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[7, 7, 7, 7, 7, 7, 7]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[1, 2, 3, 4, 5]]', 'output': '5', 'hidden': True, 'sample': False},
            {'input': '[[5, 4, 3, 2, 1]]', 'output': '1', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Merge Intervals',
        'slug': 'merge-intervals',
        'difficulty': 'medium',
        'description': '''Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.''',
        'input_format': 'A list of intervals, where each interval is [start, end].',
        'output_format': 'Return the merged intervals.',
        'constraints': '''1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= starti <= endi <= 10^4''',
        'example_input': '[[[[1, 3], [2, 6], [8, 10], [15, 18]]]]',
        'example_output': '[[1, 6], [8, 10], [15, 18]]',
        'example_explanation': 'Intervals [1,3] and [2,6] overlap, so merge them into [1,6].',
        'function_signature': 'def merge(intervals):',
        'starter_code': '''def merge(intervals):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[[[1, 3], [2, 6], [8, 10], [15, 18]]]]', 'output': '[[1, 6], [8, 10], [15, 18]]', 'hidden': False, 'sample': True},
            {'input': '[[[[1, 4], [4, 5]]]]', 'output': '[[1, 5]]', 'hidden': False, 'sample': True},
            {'input': '[[[[1, 4], [0, 4]]]]', 'output': '[[0, 4]]', 'hidden': False, 'sample': False},
            {'input': '[[[[1, 4], [2, 3]]]]', 'output': '[[1, 4]]', 'hidden': True, 'sample': False},
            {'input': '[[[[1, 2]]]]', 'output': '[[1, 2]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Number of Islands',
        'slug': 'number-of-islands',
        'difficulty': 'medium',
        'description': '''Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.''',
        'input_format': 'A 2D grid of characters "1" and "0".',
        'output_format': 'Return the number of islands.',
        'constraints': '''m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.''',
        'example_input': '[[[["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]]]',
        'example_output': '1',
        'example_explanation': 'There is one island formed by connected 1s.',
        'function_signature': 'def num_islands(grid):',
        'starter_code': '''def num_islands(grid):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[[["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]]]', 'output': '1', 'hidden': False, 'sample': True},
            {'input': '[[[["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]]]', 'output': '3', 'hidden': False, 'sample': True},
            {'input': '[[[["1"]]]]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[[["0"]]]]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[[[["1", "0"], ["0", "1"]]]]', 'output': '2', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Kth Largest Element in an Array',
        'slug': 'kth-largest-element',
        'difficulty': 'medium',
        'description': '''Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

You must solve it in O(n) time complexity.''',
        'input_format': 'A list of integers nums and an integer k.',
        'output_format': 'Return the kth largest element.',
        'constraints': '''1 <= k <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4''',
        'example_input': '[[3, 2, 1, 5, 6, 4], 2]',
        'example_output': '5',
        'example_explanation': 'The 2nd largest element is 5.',
        'function_signature': 'def find_kth_largest(nums, k):',
        'starter_code': '''def find_kth_largest(nums, k):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[3, 2, 1, 5, 6, 4], 2]', 'output': '5', 'hidden': False, 'sample': True},
            {'input': '[[3, 2, 3, 1, 2, 4, 5, 5, 6], 4]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[1], 1]', 'output': '1', 'hidden': False, 'sample': False},
            {'input': '[[7, 6, 5, 4, 3, 2, 1], 5]', 'output': '3', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3, 4, 5], 1]', 'output': '5', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Trapping Rain Water',
        'slug': 'trapping-rain-water',
        'difficulty': 'hard',
        'description': '''Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.''',
        'input_format': 'A list of non-negative integers height.',
        'output_format': 'Return the total water trapped.',
        'constraints': '''n == height.length
1 <= n <= 2 * 10^4
0 <= height[i] <= 10^5''',
        'example_input': '[[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]]',
        'example_output': '6',
        'example_explanation': 'The elevation map traps 6 units of rain water.',
        'function_signature': 'def trap(height):',
        'starter_code': '''def trap(height):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]]', 'output': '6', 'hidden': False, 'sample': True},
            {'input': '[[4, 2, 0, 3, 2, 5]]', 'output': '9', 'hidden': False, 'sample': True},
            {'input': '[[1, 2, 3, 4, 5]]', 'output': '0', 'hidden': False, 'sample': False},
            {'input': '[[5, 4, 3, 2, 1]]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[[3, 0, 3]]', 'output': '3', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Median of Two Sorted Arrays',
        'slug': 'median-two-sorted-arrays',
        'difficulty': 'hard',
        'description': '''Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).''',
        'input_format': 'Two sorted lists of integers nums1 and nums2.',
        'output_format': 'Return the median as a float.',
        'constraints': '''nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-10^6 <= nums1[i], nums2[i] <= 10^6''',
        'example_input': '[[1, 3], [2]]',
        'example_output': '2.0',
        'example_explanation': 'merged array = [1,2,3] and median is 2.',
        'function_signature': 'def find_median_sorted_arrays(nums1, nums2):',
        'starter_code': '''def find_median_sorted_arrays(nums1, nums2):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[1, 3], [2]]', 'output': '2.0', 'hidden': False, 'sample': True},
            {'input': '[[1, 2], [3, 4]]', 'output': '2.5', 'hidden': False, 'sample': True},
            {'input': '[[0, 0], [0, 0]]', 'output': '0.0', 'hidden': False, 'sample': False},
            {'input': '[[], [1]]', 'output': '1.0', 'hidden': True, 'sample': False},
            {'input': '[[2], []]', 'output': '2.0', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Longest Valid Parentheses',
        'slug': 'longest-valid-parentheses',
        'difficulty': 'hard',
        'description': '''Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.''',
        'input_format': 'A string s containing only "(" and ")".',
        'output_format': 'Return the length of the longest valid parentheses substring.',
        'constraints': '''0 <= s.length <= 3 * 10^4
s[i] is '(' or ')'.''',
        'example_input': '["(()"]',
        'example_output': '2',
        'example_explanation': 'The longest valid parentheses substring is "()".',
        'function_signature': 'def longest_valid_parentheses(s):',
        'starter_code': '''def longest_valid_parentheses(s):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["(()"]', 'output': '2', 'hidden': False, 'sample': True},
            {'input': '[")()())"]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[""]', 'output': '0', 'hidden': False, 'sample': False},
            {'input': '["()(()"]', 'output': '2', 'hidden': True, 'sample': False},
            {'input': '["(()())"]', 'output': '6', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Sudoku Solver',
        'slug': 'sudoku-solver',
        'difficulty': 'hard',
        'description': '''Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy all of the following rules:
1. Each of the digits 1-9 must occur exactly once in each row.
2. Each of the digits 1-9 must occur exactly once in each column.
3. Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.

The '.' character indicates empty cells.''',
        'input_format': 'A 9x9 2D list board.',
        'output_format': 'Return the solved board.',
        'constraints': '''board.length == 9
board[i].length == 9
board[i][j] is a digit or '.'.
It is guaranteed that the input board has only one solution.''',
        'example_input': '[[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]]',
        'example_output': '[["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]',
        'example_explanation': 'The solved Sudoku board.',
        'function_signature': 'def solve_sudoku(board):',
        'starter_code': '''def solve_sudoku(board):
    # Your code here
    pass''',
        'time_limit_seconds': 5.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]]', 'output': '[["5","3","4","6","7","8","9","1","2"],["6","7","2","1","9","5","3","4","8"],["1","9","8","3","4","2","5","6","7"],["8","5","9","7","6","1","4","2","3"],["4","2","6","8","5","3","7","9","1"],["7","1","3","9","2","4","8","5","6"],["9","6","1","5","3","7","2","8","4"],["2","8","7","4","1","9","6","3","5"],["3","4","5","2","8","6","1","7","9"]]', 'hidden': False, 'sample': True},
        ]
    },
    {
        'title': 'N-Queens',
        'slug': 'n-queens',
        'difficulty': 'hard',
        'description': '''The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.''',
        'input_format': 'An integer n.',
        'output_format': 'Return a list of all board configurations.',
        'constraints': '1 <= n <= 9',
        'example_input': '[4]',
        'example_output': '[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]',
        'example_explanation': 'There are 2 distinct solutions to the 4-queens puzzle.',
        'function_signature': 'def solve_n_queens(n):',
        'starter_code': '''def solve_n_queens(n):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[4]', 'output': '[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': '[["Q"]]', 'hidden': False, 'sample': True},
            {'input': '[2]', 'output': '[]', 'hidden': False, 'sample': False},
            {'input': '[3]', 'output': '[]', 'hidden': True, 'sample': False},
            {'input': '[5]', 'output': '[["Q....","..Q..","....Q",".Q...","...Q."],["Q....","...Q.",".Q...","....Q","..Q.."],["..Q..",".....","...Q.","Q....","....Q"],[".Q...","...Q.","Q....","..Q..","....Q"],[".Q...","....Q","..Q..","Q....","...Q."],["....Q",".Q...","...Q.","Q....","..Q.."],["....Q","..Q..","Q....","...Q.",".Q..."],["...Q.","Q....","..Q..","....Q",".Q..."],["...Q.",".Q...","....Q","..Q..","Q...."],["..Q..","....Q",".Q...","...Q.","Q...."]]', 'hidden': True, 'sample': False},
        ]
    },
    # New problems batch
    {
        'title': 'Linked List Cycle',
        'slug': 'linked-list-cycle',
        'difficulty': 'easy',
        'description': '''Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer.

Return true if there is a cycle in the linked list. Otherwise, return false.

For this problem, the input is given as a list representing the linked list values and an integer pos indicating where the tail connects to (0-indexed). If pos is -1, then there is no cycle.''',
        'input_format': 'A list representing the linked list and an integer pos for cycle position.',
        'output_format': 'Return true if cycle exists, false otherwise.',
        'constraints': '''The number of nodes is in the range [0, 10^4].
-10^5 <= Node.val <= 10^5
pos is -1 or a valid index in the linked-list.''',
        'example_input': '[[3, 2, 0, -4], 1]',
        'example_output': 'true',
        'example_explanation': 'There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).',
        'function_signature': 'def has_cycle(head, pos):',
        'starter_code': '''def has_cycle(head, pos):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[3, 2, 0, -4], 1]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[1, 2], 0]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[1], -1]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[[], -1]', 'output': 'false', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3, 4, 5], -1]', 'output': 'false', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Merge Intervals',
        'slug': 'merge-intervals',
        'difficulty': 'medium',
        'description': '''Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.''',
        'input_format': 'A list of intervals, where each interval is [start, end].',
        'output_format': 'Return a list of merged non-overlapping intervals.',
        'constraints': '''1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= starti <= endi <= 10^4''',
        'example_input': '[[[1, 3], [2, 6], [8, 10], [15, 18]]]',
        'example_output': '[[1, 6], [8, 10], [15, 18]]',
        'example_explanation': 'Since intervals [1,3] and [2,6] overlap, merge them into [1,6].',
        'function_signature': 'def merge(intervals):',
        'starter_code': '''def merge(intervals):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[[1, 3], [2, 6], [8, 10], [15, 18]]]', 'output': '[[1, 6], [8, 10], [15, 18]]', 'hidden': False, 'sample': True},
            {'input': '[[[1, 4], [4, 5]]]', 'output': '[[1, 5]]', 'hidden': False, 'sample': True},
            {'input': '[[[1, 4], [0, 4]]]', 'output': '[[0, 4]]', 'hidden': False, 'sample': False},
            {'input': '[[[1, 4], [2, 3]]]', 'output': '[[1, 4]]', 'hidden': True, 'sample': False},
            {'input': '[[[1, 4], [0, 0]]]', 'output': '[[0, 0], [1, 4]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Set Matrix Zeroes',
        'slug': 'set-matrix-zeroes',
        'difficulty': 'medium',
        'description': '''Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.''',
        'input_format': 'A 2D matrix of integers.',
        'output_format': 'Return the modified matrix.',
        'constraints': '''m == matrix.length
n == matrix[0].length
1 <= m, n <= 200
-2^31 <= matrix[i][j] <= 2^31 - 1''',
        'example_input': '[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]]',
        'example_output': '[[1, 0, 1], [0, 0, 0], [1, 0, 1]]',
        'example_explanation': 'The element at [1][1] is 0, so row 1 and column 1 are set to 0.',
        'function_signature': 'def set_zeroes(matrix):',
        'starter_code': '''def set_zeroes(matrix):
    # Modify matrix in-place and return it
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[[1, 1, 1], [1, 0, 1], [1, 1, 1]]]', 'output': '[[1, 0, 1], [0, 0, 0], [1, 0, 1]]', 'hidden': False, 'sample': True},
            {'input': '[[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]]', 'output': '[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]', 'hidden': False, 'sample': True},
            {'input': '[[[1, 2, 3], [4, 5, 6]]]', 'output': '[[1, 2, 3], [4, 5, 6]]', 'hidden': False, 'sample': False},
            {'input': '[[[0]]]', 'output': '[[0]]', 'hidden': True, 'sample': False},
            {'input': '[[[1, 0], [0, 1]]]', 'output': '[[0, 0], [0, 0]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Word Search',
        'slug': 'word-search',
        'difficulty': 'medium',
        'description': '''Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.''',
        'input_format': 'A 2D grid of characters and a word string.',
        'output_format': 'Return true if the word exists in the grid, false otherwise.',
        'constraints': '''m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consists of only lowercase and uppercase English letters.''',
        'example_input': '[[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"]',
        'example_output': 'true',
        'example_explanation': 'The word ABCCED can be found starting from A at [0][0].',
        'function_signature': 'def exist(board, word):',
        'starter_code': '''def exist(board, word):
    # Your code here
    pass''',
        'time_limit_seconds': 3.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE"]', 'output': 'true', 'hidden': False, 'sample': True},
            {'input': '[[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"]', 'output': 'false', 'hidden': False, 'sample': False},
            {'input': '[[["A"]], "A"]', 'output': 'true', 'hidden': True, 'sample': False},
            {'input': '[[["A","B"],["C","D"]], "ABDC"]', 'output': 'true', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Subsets',
        'slug': 'subsets',
        'difficulty': 'medium',
        'description': '''Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.''',
        'input_format': 'An array of unique integers.',
        'output_format': 'Return a list of all subsets.',
        'constraints': '''1 <= nums.length <= 10
-10 <= nums[i] <= 10
All the numbers of nums are unique.''',
        'example_input': '[[1, 2, 3]]',
        'example_output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]',
        'example_explanation': 'All possible subsets of [1,2,3] are listed.',
        'function_signature': 'def subsets(nums):',
        'starter_code': '''def subsets(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[1, 2, 3]]', 'output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]', 'hidden': False, 'sample': True},
            {'input': '[[0]]', 'output': '[[], [0]]', 'hidden': False, 'sample': True},
            {'input': '[[1, 2]]', 'output': '[[], [1], [2], [1, 2]]', 'hidden': False, 'sample': False},
            {'input': '[[1]]', 'output': '[[], [1]]', 'hidden': True, 'sample': False},
            {'input': '[[1, 2, 3, 4]]', 'output': '[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Permutations',
        'slug': 'permutations',
        'difficulty': 'medium',
        'description': '''Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.''',
        'input_format': 'An array of distinct integers.',
        'output_format': 'Return a list of all permutations.',
        'constraints': '''1 <= nums.length <= 6
-10 <= nums[i] <= 10
All the integers of nums are unique.''',
        'example_input': '[[1, 2, 3]]',
        'example_output': '[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]',
        'example_explanation': 'All 6 permutations of [1,2,3] are listed.',
        'function_signature': 'def permute(nums):',
        'starter_code': '''def permute(nums):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[1, 2, 3]]', 'output': '[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]', 'hidden': False, 'sample': True},
            {'input': '[[0, 1]]', 'output': '[[0, 1], [1, 0]]', 'hidden': False, 'sample': True},
            {'input': '[[1]]', 'output': '[[1]]', 'hidden': False, 'sample': False},
            {'input': '[[1, 2]]', 'output': '[[1, 2], [2, 1]]', 'hidden': True, 'sample': False},
            {'input': '[[-1, 0, 1]]', 'output': '[[-1, 0, 1], [-1, 1, 0], [0, -1, 1], [0, 1, -1], [1, -1, 0], [1, 0, -1]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Combination Sum',
        'slug': 'combination-sum',
        'difficulty': 'medium',
        'description': '''Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.''',
        'input_format': 'An array of distinct integers and a target integer.',
        'output_format': 'Return a list of all unique combinations that sum to target.',
        'constraints': '''1 <= candidates.length <= 30
2 <= candidates[i] <= 40
All elements of candidates are distinct.
1 <= target <= 40''',
        'example_input': '[[2, 3, 6, 7], 7]',
        'example_output': '[[2, 2, 3], [7]]',
        'example_explanation': '2 + 2 + 3 = 7 and 7 = 7 are the two combinations.',
        'function_signature': 'def combination_sum(candidates, target):',
        'starter_code': '''def combination_sum(candidates, target):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[[2, 3, 6, 7], 7]', 'output': '[[2, 2, 3], [7]]', 'hidden': False, 'sample': True},
            {'input': '[[2, 3, 5], 8]', 'output': '[[2, 2, 2, 2], [2, 3, 3], [3, 5]]', 'hidden': False, 'sample': True},
            {'input': '[[2], 1]', 'output': '[]', 'hidden': False, 'sample': False},
            {'input': '[[1], 1]', 'output': '[[1]]', 'hidden': True, 'sample': False},
            {'input': '[[1, 2], 4]', 'output': '[[1, 1, 1, 1], [1, 1, 2], [2, 2]]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Letter Combinations of a Phone Number',
        'slug': 'letter-combinations-phone',
        'difficulty': 'medium',
        'description': '''Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.

2: abc, 3: def, 4: ghi, 5: jkl, 6: mno, 7: pqrs, 8: tuv, 9: wxyz''',
        'input_format': 'A string containing digits from 2-9.',
        'output_format': 'Return a list of all possible letter combinations.',
        'constraints': '''0 <= digits.length <= 4
digits[i] is a digit in the range ['2', '9'].''',
        'example_input': '["23"]',
        'example_output': '["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]',
        'example_explanation': 'Digit 2 maps to abc, digit 3 maps to def. All combinations are listed.',
        'function_signature': 'def letter_combinations(digits):',
        'starter_code': '''def letter_combinations(digits):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '["23"]', 'output': '["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]', 'hidden': False, 'sample': True},
            {'input': '[""]', 'output': '[]', 'hidden': False, 'sample': True},
            {'input': '["2"]', 'output': '["a", "b", "c"]', 'hidden': False, 'sample': False},
            {'input': '["7"]', 'output': '["p", "q", "r", "s"]', 'hidden': True, 'sample': False},
            {'input': '["79"]', 'output': '["pw", "px", "py", "pz", "qw", "qx", "qy", "qz", "rw", "rx", "ry", "rz", "sw", "sx", "sy", "sz"]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Generate Parentheses',
        'slug': 'generate-parentheses',
        'difficulty': 'medium',
        'description': '''Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.''',
        'input_format': 'An integer n representing the number of pairs of parentheses.',
        'output_format': 'Return a list of all valid parentheses combinations.',
        'constraints': '1 <= n <= 8',
        'example_input': '[3]',
        'example_output': '["((()))", "(()())", "(())()", "()(())", "()()()"]',
        'example_explanation': 'All valid combinations of 3 pairs of parentheses.',
        'function_signature': 'def generate_parenthesis(n):',
        'starter_code': '''def generate_parenthesis(n):
    # Your code here
    pass''',
        'time_limit_seconds': 2.0,
        'memory_limit_mb': 256,
        'test_cases': [
            {'input': '[3]', 'output': '["((()))", "(()())", "(())()", "()(())", "()()()"]', 'hidden': False, 'sample': True},
            {'input': '[1]', 'output': '["()"]', 'hidden': False, 'sample': True},
            {'input': '[2]', 'output': '["(())", "()()"]', 'hidden': False, 'sample': False},
            {'input': '[4]', 'output': '["(((())))", "((()()))", "((())())", "((()))()", "(()(()))", "(()()())", "(()())()", "(())(())", "(())()()", "()((()))", "()(()())", "()(())()", "()()(())", "()()()()"]', 'hidden': True, 'sample': False},
            {'input': '[5]', 'output': '["((((()))))", "(((()())))", "(((())()))", "(((()))())", "(((())))()", "((()(())))", "((()()()))", "((()())())", "((()()))()", "((())(()))", "((())()())", "((())())()", "((()))(())", "((()))()()", "(()((())))", "(()(()()))", "(()(())())", "(()(()))()", "(()()(()))", "(()()()())", "(()()())()", "(()())(())", "(()())()()", "(())((()))", "(())(()())", "(())(())()", "(())()(())", "(())()()()", "()(((())))", "()((()()))", "()((())())", "()((()))()", "()(()(()))", "()(()()())", "()(()())()", "()(())(())", "()(())()()", "()()((()))", "()()(()())", "()()(())()", "()()()(())", "()()()()()"]', 'hidden': True, 'sample': False},
        ]
    },
    {
        'title': 'Search in Rotated Sorted Array',
        'slug': 'search-rotated-array',
        'difficulty': 'medium',
        'description': '''There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).

Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.''',
        'input_format': 'A rotated sorted array and a target integer.',
        'output_format': 'Return the index of target or -1 if not found.',
        'constraints': '''1 <= nums.length <= 5000
-10^4 <= nums[i] <= 10^4
All values of nums are unique.
nums is an ascending array that is possibly rotated.
-10^4 <= target <= 10^4''',
        'example_input': '[[4, 5, 6, 7, 0, 1, 2], 0]',
        'example_output': '4',
        'example_explanation': 'The target 0 is at index 4 in the rotated array.',
        'function_signature': 'def search(nums, target):',
        'starter_code': '''def search(nums, target):
    # Your code here
    pass''',
        'time_limit_seconds': 1.0,
        'memory_limit_mb': 128,
        'test_cases': [
            {'input': '[[4, 5, 6, 7, 0, 1, 2], 0]', 'output': '4', 'hidden': False, 'sample': True},
            {'input': '[[4, 5, 6, 7, 0, 1, 2], 3]', 'output': '-1', 'hidden': False, 'sample': True},
            {'input': '[[1], 0]', 'output': '-1', 'hidden': False, 'sample': False},
            {'input': '[[1], 1]', 'output': '0', 'hidden': True, 'sample': False},
            {'input': '[[3, 1], 1]', 'output': '1', 'hidden': True, 'sample': False},
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
