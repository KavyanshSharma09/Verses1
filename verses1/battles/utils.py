import ast
import time
import tempfile
import os
import subprocess
import shlex

def count_complexity_metrics(code):
    """Count basic complexity metrics like number of functions, classes, and lines."""
    try:
        tree = ast.parse(code)
        num_functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        num_classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        num_lines = len(code.splitlines())
        score = 100 - (num_functions * 5 + num_classes * 10 + num_lines * 0.5)
        return max(0, min(score, 100))
    except:
        return 0

def analyze_code_complexity(code):
    return count_complexity_metrics(code)

def analyze_code_performance(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file.flush()
        start_time = time.time()
        try:
            completed = subprocess.run(
                ["python", tmp_file.name],
                capture_output=True,
                text=True,
                timeout=3
            )
            execution_time = time.time() - start_time
        except subprocess.TimeoutExpired:
            execution_time = 10.0  
        finally:
            try:
                os.unlink(tmp_file.name)
            except Exception:
                pass

        return max(0, 100 - (execution_time * 10))
    except:
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
    except:
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
