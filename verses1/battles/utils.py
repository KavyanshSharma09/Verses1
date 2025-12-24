import ast
import time
import tempfile
import os

def count_complexity_metrics(code):
    """Count basic complexity metrics like number of functions, classes, and lines."""
    try:
        tree = ast.parse(code)
        num_functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        num_classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        num_lines = len(code.splitlines())
        score = 100 - (num_functions * 5 + num_classes * 10 + num_lines * 0.5)
        return max(0, min(score, 100))
    except (SyntaxError, ValueError, TypeError):
        return 0

def analyze_code_complexity(code):
    return count_complexity_metrics(code)

def analyze_code_performance(code):
    """
    Analyze code performance using static analysis only (no execution).
    Scores based on algorithmic patterns and code structure.
    """
    try:
        tree = ast.parse(code)
        score = 100.0
        
        # Count nested loops (indicates potential O(n²) or worse)
        nested_loops = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)) and child is not node:
                        nested_loops += 1
        score -= nested_loops * 15
        
        # Check for recursion (can be expensive)
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name) and child.func.id == node.name:
                            score -= 10  # Recursive call detected
        
        # Count total loops
        loop_count = len([n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))])
        score -= loop_count * 3
        
        # Check for efficient built-ins usage
        efficient_calls = ['map', 'filter', 'sorted', 'enumerate', 'zip']
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in efficient_calls:
                    score += 2  # Bonus for using efficient built-ins
        
        return max(0, min(score, 100))
    except (SyntaxError, ValueError, TypeError):
        return 0

def analyze_code_readability(code):

    try:
        lines = code.splitlines()
        total_lines = len(lines)
        if total_lines == 0:
            return 0
            
        scores = [
            sum(1 for line in lines if len(line.strip()) <= 79) / total_lines * 100,
            len([line for line in lines if line.strip().startswith('#')]) / total_lines * 50,
            len([line for line in lines if line.startswith('    ')]) / total_lines * 50,
            len([line for line in lines if not line.strip()]) / total_lines * 30
        ]
        
        return sum(scores) / len(scores)
    except (ZeroDivisionError, TypeError):
        return 0

def calculate_total_score(complexity_score, performance_score, readability_score):
    weights = {
        'complexity': 0.3,
        'performance': 0.4,
        'readability': 0.3
    }
    
    return (
        complexity_score * weights['complexity'] +
        performance_score * weights['performance'] +
        readability_score * weights['readability']
    )

def compare_submissions(submission1, submission2):
    comparisons = {
        'complexity': 'Code Complexity:\n',
        'performance': 'Performance:\n',
        'readability': 'Code Readability:\n'
    }
    if submission1.complexity_score != submission2.complexity_score:
        winner = submission1 if submission1.complexity_score > submission2.complexity_score else submission2
        comparisons['complexity'] += f"{winner.user.username}'s code is less complex."
    else:
        comparisons['complexity'] += "Both submissions have similar complexity."
    
    if submission1.performance_score != submission2.performance_score:
        winner = submission1 if submission1.performance_score > submission2.performance_score else submission2
        comparisons['performance'] += f"{winner.user.username}'s code performs better."
    else:
        comparisons['performance'] += "Both submissions have similar performance."

    if submission1.readability_score != submission2.readability_score:
        winner = submission1 if submission1.readability_score > submission2.readability_score else submission2
        comparisons['readability'] += f"{winner.user.username}'s code is more readable."
    else:
        comparisons['readability'] += "Both submissions have similar readability."
    
    return comparisons
