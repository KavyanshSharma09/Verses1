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
        
        # Simple complexity score based on code structure
        score = 100 - (num_functions * 5 + num_classes * 10 + num_lines * 0.5)
        return max(0, min(score, 100))
    except:
        return 0

def analyze_code_complexity(code):
    """Analyze code complexity using basic metrics."""
    return count_complexity_metrics(code)

def analyze_code_performance(code):
    """Analyze code performance by running it with sample inputs."""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_file.flush()
        # Use subprocess with timeout to avoid long-running code
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
            execution_time = 10.0  # penalize long-running code
        finally:
            try:
                os.unlink(tmp_file.name)
            except Exception:
                pass

        # Convert execution time to a score (lower is better)
        return max(0, 100 - (execution_time * 10))
    except:
        return 0

def analyze_code_readability(code):
    """Analyze code readability using basic metrics."""
    try:
        # Check for common readability indicators
        lines = code.splitlines()
        total_lines = len(lines)
        if total_lines == 0:
            return 0
            
        # Calculate scores for different readability aspects
        scores = [
            # Line length score
            sum(1 for line in lines if len(line.strip()) <= 79) / total_lines * 100,
            
            # Comment ratio score
            len([line for line in lines if line.strip().startswith('#')]) / total_lines * 50,
            
            # Indentation consistency score
            len([line for line in lines if line.startswith('    ')]) / total_lines * 50,
            
            # Empty lines ratio score
            len([line for line in lines if not line.strip()]) / total_lines * 30
        ]
        
        return sum(scores) / len(scores)
    except:
        return 0

def calculate_total_score(complexity_score, performance_score, readability_score):
    """Calculate total score with weighted components."""
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
    """Compare two code submissions and return detailed comparison."""
    comparisons = {
        'complexity': 'Code Complexity:\n',
        'performance': 'Performance:\n',
        'readability': 'Code Readability:\n'
    }
    
    # Compare complexity
    if submission1.complexity_score != submission2.complexity_score:
        winner = submission1 if submission1.complexity_score > submission2.complexity_score else submission2
        comparisons['complexity'] += f"{winner.user.username}'s code is less complex."
    else:
        comparisons['complexity'] += "Both submissions have similar complexity."
    
    # Compare performance
    if submission1.performance_score != submission2.performance_score:
        winner = submission1 if submission1.performance_score > submission2.performance_score else submission2
        comparisons['performance'] += f"{winner.user.username}'s code performs better."
    else:
        comparisons['performance'] += "Both submissions have similar performance."
    
    # Compare readability
    if submission1.readability_score != submission2.readability_score:
        winner = submission1 if submission1.readability_score > submission2.readability_score else submission2
        comparisons['readability'] += f"{winner.user.username}'s code is more readable."
    else:
        comparisons['readability'] += "Both submissions have similar readability."
    
    return comparisons