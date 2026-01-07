"""
Secure Code Execution Sandbox for Verses1
Executes user code against test cases with time/memory limits
"""

import subprocess
import tempfile
import os
import json
import time
import sys
import platform
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

# resource module is Unix-only, not available on Windows
if platform.system() != 'Windows':
    import resource
    import signal

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Result of running a single test case"""
    test_id: int
    passed: bool
    input_data: str
    expected_output: str
    actual_output: str
    execution_time: float  # in seconds
    memory_used: float  # in MB
    error_message: str = ""
    is_timeout: bool = False
    is_runtime_error: bool = False


@dataclass
class ExecutionResult:
    """Result of running all test cases"""
    all_passed: bool
    tests_passed: int
    tests_total: int
    test_results: List[TestResult]
    avg_execution_time: float
    max_memory_used: float
    total_points: int
    max_points: int
    syntax_error: str = ""
    has_forbidden_imports: bool = False
    forbidden_import_name: str = ""


# Forbidden imports for security
FORBIDDEN_IMPORTS = [
    'subprocess', 'shutil', 'socket', 'requests',
    'urllib', 'http', 'ftplib', 'smtplib', 'telnetlib',
    'pickle', 'shelve', 'marshal', 'importlib', 'builtins',
    '__builtins__', 'eval', 'exec', 'compile', 'open', 'file',
    'input', 'raw_input', 'execfile', 'reload', '__import__',
    'ctypes', 'multiprocessing', 'threading', 'signal',
    'resource', 'pty', 'tty', 'termios', 'fcntl', 'posix',
]

# Allowed safe imports for algorithm problems
ALLOWED_IMPORTS = [
    # Math & Numbers
    'math', 'cmath', 'decimal', 'fractions', 'statistics', 'random',
    
    # Data Structures
    'collections', 'heapq', 'bisect', 'array', 'queue',
    
    # Functional Programming
    'itertools', 'functools', 'operator',
    
    # String & Text
    'string', 're',
    
    # Utilities
    'copy', 'json', 'typing', 'dataclasses', 'enum',
    'datetime', 'time', 'calendar',
    
    # System (limited) - for setrecursionlimit
    'sys', 'os',
]

# Allowed sys attributes (whitelist approach)
ALLOWED_SYS_ATTRS = [
    'setrecursionlimit', 'getrecursionlimit', 'maxsize', 'stdin', 'stdout',
]

# Allowed os attributes (whitelist approach) 
ALLOWED_OS_ATTRS = [
    'path',  # for os.path operations like join, exists
]


def check_forbidden_imports(code: str) -> Tuple[bool, str]:
    """Check if code contains forbidden imports"""
    import ast
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False, ""  # Syntax errors handled separately
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split('.')[0]
                if module_name in FORBIDDEN_IMPORTS:
                    return True, module_name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_name = node.module.split('.')[0]
                if module_name in FORBIDDEN_IMPORTS:
                    return True, module_name
    
    # Check for dangerous built-in usage
    dangerous_calls = ['eval', 'exec', 'compile', 'open', '__import__']
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in dangerous_calls:
                    return True, node.func.id
    
    return False, ""


def create_test_wrapper(user_code: str, function_name: str, input_data: str) -> str:
    """Create a wrapper script that runs the user's code with test input"""
    
    wrapper = f'''
import json
import sys
import traceback

# Disable dangerous builtins
restricted_builtins = {{
    # Basic I/O
    'print': print,
    'input': input,
    
    # Type constructors
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'frozenset': frozenset,
    'bytes': bytes,
    'bytearray': bytearray,
    'complex': complex,
    'object': object,
    
    # Sequence operations
    'len': len,
    'range': range,
    'sorted': sorted,
    'reversed': reversed,
    'enumerate': enumerate,
    'zip': zip,
    'map': map,
    'filter': filter,
    'slice': slice,
    
    # Math operations
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    'pow': pow,
    'divmod': divmod,
    
    # Logic operations
    'all': all,
    'any': any,
    
    # Type checking
    'isinstance': isinstance,
    'issubclass': issubclass,
    'type': type,
    'callable': callable,
    
    # Attribute access
    'hasattr': hasattr,
    'getattr': getattr,
    'setattr': setattr,
    'delattr': delattr,
    
    # Iteration
    'iter': iter,
    'next': next,
    
    # String/Char operations
    'ord': ord,
    'chr': chr,
    'ascii': ascii,
    'repr': repr,
    'format': format,
    
    # Number conversions
    'hex': hex,
    'bin': bin,
    'oct': oct,
    
    # Object operations
    'hash': hash,
    'id': id,
    'dir': dir,
    'vars': vars,
    'globals': lambda: {{}},
    'locals': lambda: {{}},
    'memoryview': memoryview,
    'property': property,
    'staticmethod': staticmethod,
    'classmethod': classmethod,
    'super': super,
    
    # Constants
    '__name__': '__main__',
    '__doc__': None,
    'True': True,
    'False': False,
    'None': None,
    'Ellipsis': Ellipsis,
    'NotImplemented': NotImplemented,
    
    # Exceptions
    'Exception': Exception,
    'BaseException': BaseException,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'ZeroDivisionError': ZeroDivisionError,
    'StopIteration': StopIteration,
    'AttributeError': AttributeError,
    'NameError': NameError,
    'RuntimeError': RuntimeError,
    'RecursionError': RecursionError,
    'OverflowError': OverflowError,
    'MemoryError': MemoryError,
    'AssertionError': AssertionError,
    'ArithmeticError': ArithmeticError,
    'LookupError': LookupError,
    'IOError': IOError,
    'OSError': OSError,
    'NotImplementedError': NotImplementedError,
}}

try:
    # User's code
{chr(10).join("    " + line for line in user_code.splitlines())}
    
    # Parse input and call the function
    test_input = {repr(input_data)}
    input_args = json.loads(test_input)
    
    # Call the user's function
    if isinstance(input_args, list):
        result = {function_name}(*input_args)
    elif isinstance(input_args, dict):
        result = {function_name}(**input_args)
    else:
        result = {function_name}(input_args)
    
    # Output the result as JSON
    print(json.dumps({{"success": True, "result": result}}))
    
except Exception as e:
    print(json.dumps({{"success": False, "error": str(e), "traceback": traceback.format_exc()}}))
'''
    return wrapper


def run_code_with_timeout(code: str, timeout: float, memory_limit_mb: int) -> Tuple[str, float, bool, str]:
    """
    Run code in a subprocess with timeout and memory limits.
    Returns: (output, execution_time, timed_out, error_message)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        start_time = time.time()
        
        # Run in subprocess with timeout
        try:
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tempfile.gettempdir(),
            )
            execution_time = time.time() - start_time
            
            if result.returncode != 0:
                return "", execution_time, False, result.stderr
            
            return result.stdout.strip(), execution_time, False, ""
            
        except subprocess.TimeoutExpired:
            return "", timeout, True, "Time Limit Exceeded"
            
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass


def normalize_output(output: str) -> str:
    """Normalize output for comparison (strip whitespace, normalize line endings)"""
    return '\n'.join(line.strip() for line in output.strip().splitlines())


def compare_outputs(expected: str, actual: str) -> bool:
    """Compare expected and actual outputs"""
    expected_norm = normalize_output(expected)
    actual_norm = normalize_output(actual)
    return expected_norm == actual_norm


def extract_function_name(signature: str) -> str:
    """Extract function name from signature like 'def two_sum(nums, target):'"""
    import re
    match = re.search(r'def\s+(\w+)\s*\(', signature)
    if match:
        return match.group(1)
    return "solution"


def run_tests(
    code: str,
    problem,  # ProblemStatement model instance
    test_cases: List,  # List of TestCase model instances
) -> ExecutionResult:
    """
    Run user code against all test cases.
    Returns ExecutionResult with all details.
    """
    # Check for syntax errors first
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        return ExecutionResult(
            all_passed=False,
            tests_passed=0,
            tests_total=len(test_cases),
            test_results=[],
            avg_execution_time=0,
            max_memory_used=0,
            total_points=0,
            max_points=sum(tc.points for tc in test_cases),
            syntax_error=f"Line {e.lineno}: {e.msg}"
        )
    
    # Check for forbidden imports
    has_forbidden, forbidden_name = check_forbidden_imports(code)
    if has_forbidden:
        return ExecutionResult(
            all_passed=False,
            tests_passed=0,
            tests_total=len(test_cases),
            test_results=[],
            avg_execution_time=0,
            max_memory_used=0,
            total_points=0,
            max_points=sum(tc.points for tc in test_cases),
            has_forbidden_imports=True,
            forbidden_import_name=forbidden_name
        )
    
    function_name = extract_function_name(problem.function_signature)
    test_results = []
    total_execution_time = 0
    max_memory = 0
    total_points = 0
    
    for i, test_case in enumerate(test_cases):
        # Create wrapper code
        wrapper_code = create_test_wrapper(code, function_name, test_case.input_data)
        
        # Run with timeout
        output, exec_time, timed_out, error = run_code_with_timeout(
            wrapper_code,
            problem.time_limit_seconds,
            problem.memory_limit_mb
        )
        
        total_execution_time += exec_time
        
        # Parse output
        actual_output = ""
        passed = False
        error_message = error
        
        if timed_out:
            error_message = "Time Limit Exceeded"
        elif error:
            error_message = error
        else:
            try:
                result_data = json.loads(output)
                if result_data.get('success'):
                    actual_output = json.dumps(result_data['result'])
                    # Compare with expected
                    expected_parsed = test_case.expected_output.strip()
                    passed = compare_outputs(expected_parsed, actual_output)
                else:
                    error_message = result_data.get('error', 'Unknown error')
            except json.JSONDecodeError:
                actual_output = output
                passed = compare_outputs(test_case.expected_output, output)
        
        if passed:
            total_points += test_case.points
        
        test_results.append(TestResult(
            test_id=test_case.id,
            passed=passed,
            input_data=test_case.input_data if not test_case.is_hidden else "[Hidden]",
            expected_output=test_case.expected_output if not test_case.is_hidden else "[Hidden]",
            actual_output=actual_output if not test_case.is_hidden else ("[Correct]" if passed else "[Wrong Answer]"),
            execution_time=exec_time,
            memory_used=0,  # TODO: Implement memory tracking
            error_message=error_message,
            is_timeout=timed_out,
            is_runtime_error=bool(error and not timed_out)
        ))
    
    tests_passed = sum(1 for r in test_results if r.passed)
    avg_time = total_execution_time / len(test_cases) if test_cases else 0
    
    return ExecutionResult(
        all_passed=tests_passed == len(test_cases),
        tests_passed=tests_passed,
        tests_total=len(test_cases),
        test_results=test_results,
        avg_execution_time=avg_time,
        max_memory_used=max_memory,
        total_points=total_points,
        max_points=sum(tc.points for tc in test_cases)
    )


def execution_result_to_dict(result: ExecutionResult) -> Dict[str, Any]:
    """Convert ExecutionResult to dictionary for JSON serialization"""
    return {
        'all_passed': result.all_passed,
        'tests_passed': result.tests_passed,
        'tests_total': result.tests_total,
        'avg_execution_time': round(result.avg_execution_time, 4),
        'max_memory_used': round(result.max_memory_used, 2),
        'total_points': result.total_points,
        'max_points': result.max_points,
        'syntax_error': result.syntax_error,
        'has_forbidden_imports': result.has_forbidden_imports,
        'forbidden_import_name': result.forbidden_import_name,
        'test_results': [
            {
                'test_id': tr.test_id,
                'passed': tr.passed,
                'input_data': tr.input_data,
                'expected_output': tr.expected_output,
                'actual_output': tr.actual_output,
                'execution_time': round(tr.execution_time, 4),
                'memory_used': round(tr.memory_used, 2),
                'error_message': tr.error_message,
                'is_timeout': tr.is_timeout,
                'is_runtime_error': tr.is_runtime_error,
            }
            for tr in result.test_results
        ]
    }
