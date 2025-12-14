"""
Advanced Code Analysis Engine for Verses1
Uses AST, pattern analysis, and heuristics for accurate code evaluation
"""

import ast
import re
import math
import tokenize
import io
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    total_score: float = 0.0
    complexity_score: float = 0.0
    performance_score: float = 0.0
    readability_score: float = 0.0
    security_score: float = 0.0
    style_score: float = 0.0
    cyclomatic_complexity: int = 0
    cognitive_complexity: int = 0
    maintainability_index: float = 0.0
    lines_of_code: int = 0
    logical_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    functions_count: int = 0
    classes_count: int = 0
    imports_count: int = 0
    nested_depth: int = 0
    avg_function_length: float = 0.0
    halstead_vocabulary: int = 0
    halstead_length: int = 0
    halstead_volume: float = 0.0
    halstead_difficulty: float = 0.0
    halstead_effort: float = 0.0
    halstead_bugs: float = 0.0
    time_complexity: str = "O(1)"
    space_complexity: str = "O(1)"
    
    issues: List[Dict[str, Any]] = field(default_factory=list)
    security_issues: List[Dict[str, Any]] = field(default_factory=list)
    
    is_valid: bool = True
    syntax_error: str = ""


class ASTAnalyzer(ast.NodeVisitor):
    """AST-based code analyzer"""
    
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.variables = set()
        self.loops = []
        self.conditionals = []
        self.calls = []
        self.nested_depth = 0
        self.max_depth = 0
        self.current_function = None
        self.function_complexities = {}
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)
        
    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'lineno': node.lineno,
            'args': len(node.args.args),
            'decorators': len(node.decorator_list),
            'body_lines': len(node.body),
            'has_docstring': ast.get_docstring(node) is not None,
            'returns': node.returns is not None,
            'complexity': self._calculate_function_complexity(node)
        }
        self.functions.append(func_info)
        
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
        
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
        
    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'lineno': node.lineno,
            'bases': len(node.bases),
            'methods': len([n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
            'has_docstring': ast.get_docstring(node) is not None
        }
        self.classes.append(class_info)
        self.generic_visit(node)
        
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({'name': alias.name, 'type': 'import'})
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        module = node.module or ''
        for alias in node.names:
            self.imports.append({'name': f"{module}.{alias.name}", 'type': 'from'})
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.loops.append({'type': 'for', 'lineno': node.lineno, 'depth': self.nested_depth})
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1
        
    def visit_While(self, node):
        self.loops.append({'type': 'while', 'lineno': node.lineno, 'depth': self.nested_depth})
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1
        
    def visit_If(self, node):
        self.conditionals.append({'lineno': node.lineno, 'depth': self.nested_depth})
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1
        
    def visit_Call(self, node):
        call_info = {'lineno': node.lineno}
        if isinstance(node.func, ast.Name):
            call_info['name'] = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_info['name'] = node.func.attr
        self.calls.append(call_info)
        self.generic_visit(node)
        
    def visit_Name(self, node):
        self.operands[node.id] += 1
        self.variables.add(node.id)
        self.generic_visit(node)
        
    def visit_Constant(self, node):
        self.operands[str(node.value)] += 1
        self.generic_visit(node)
        
    def visit_BinOp(self, node):
        self.operators[type(node.op).__name__] += 1
        self.generic_visit(node)
        
    def visit_UnaryOp(self, node):
        self.operators[type(node.op).__name__] += 1
        self.generic_visit(node)
        
    def visit_BoolOp(self, node):
        self.operators[type(node.op).__name__] += len(node.values) - 1
        self.generic_visit(node)
        
    def visit_Compare(self, node):
        for op in node.ops:
            self.operators[type(op).__name__] += 1
        self.generic_visit(node)
        
    def _calculate_function_complexity(self, node) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.Assert, ast.comprehension)):
                complexity += 1
        return complexity


class CodeAnalysisEngine:
    """Main analysis engine combining multiple analysis methods"""
    
    def __init__(self):
        self.security_patterns = {
            'sql_injection': {
                'patterns': [
                    r'execute\s*\(\s*["\'].*%.*["\']',
                    r'execute\s*\(\s*f["\']',
                    r'\.format\s*\(.*\).*execute',
                ],
                'severity': 'high',
                'message': 'Potential SQL injection vulnerability'
            },
            'command_injection': {
                'patterns': [
                    r'os\.system\s*\(',
                    r'subprocess\.call\s*\([^,\]]*shell\s*=\s*True',
                    r'eval\s*\(',
                    r'exec\s*\(',
                ],
                'severity': 'critical',
                'message': 'Potential command injection vulnerability'
            },
            'hardcoded_secrets': {
                'patterns': [
                    r'password\s*=\s*["\'][^"\']{4,}["\']',
                    r'api_key\s*=\s*["\'][^"\']{8,}["\']',
                    r'secret\s*=\s*["\'][^"\']{4,}["\']',
                    r'token\s*=\s*["\'][^"\']{8,}["\']',
                ],
                'severity': 'high',
                'message': 'Hardcoded secret detected'
            },
            'weak_crypto': {
                'patterns': [
                    r'import\s+md5',
                    r'hashlib\.md5',
                    r'import\s+sha1',
                    r'hashlib\.sha1',
                ],
                'severity': 'medium',
                'message': 'Weak cryptographic algorithm detected'
            }
        }
        
        self.style_rules = {
            'line_length': 79,
            'max_function_length': 50,
            'max_complexity': 10,
            'min_docstring_coverage': 0.5,
        }
    
    def analyze(self, code: str) -> AnalysisResult:
        """Perform comprehensive code analysis"""
        result = AnalysisResult()
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            result.is_valid = False
            result.syntax_error = f"Line {e.lineno}: {e.msg}"
            result.total_score = 0
            return result
        
        ast_analyzer = ASTAnalyzer()
        ast_analyzer.visit(tree)
        
        lines = code.splitlines()
        result.lines_of_code = len(lines)
        result.blank_lines = sum(1 for line in lines if not line.strip())
        result.comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        result.logical_lines = result.lines_of_code - result.blank_lines - result.comment_lines
        
        result.functions_count = len(ast_analyzer.functions)
        result.classes_count = len(ast_analyzer.classes)
        result.imports_count = len(ast_analyzer.imports)
        result.nested_depth = ast_analyzer.max_depth
        
        if ast_analyzer.functions:
            result.avg_function_length = sum(f['body_lines'] for f in ast_analyzer.functions) / len(ast_analyzer.functions)
        
        result.cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)
        result.cognitive_complexity = self._calculate_cognitive_complexity(tree)
        result.maintainability_index = self._calculate_maintainability_index(
            result.lines_of_code, 
            result.cyclomatic_complexity,
            ast_analyzer
        )
        
        halstead = self._calculate_halstead_metrics(ast_analyzer)
        result.halstead_vocabulary = halstead['vocabulary']
        result.halstead_length = halstead['length']
        result.halstead_volume = halstead['volume']
        result.halstead_difficulty = halstead['difficulty']
        result.halstead_effort = halstead['effort']
        result.halstead_bugs = halstead['bugs']
        
        result.time_complexity = self._estimate_time_complexity(tree, ast_analyzer)
        result.space_complexity = self._estimate_space_complexity(tree, ast_analyzer)
        
        result.security_issues = self._analyze_security(code)
        
        result.issues = self._analyze_style(code, lines, ast_analyzer)
        
        result.complexity_score = self._score_complexity(result)
        result.performance_score = self._score_performance(result, ast_analyzer)
        result.readability_score = self._score_readability(result, lines, ast_analyzer)
        result.security_score = self._score_security(result)
        result.style_score = self._score_style(result, lines, ast_analyzer)
        
        result.total_score = (
            result.complexity_score * 0.20 +
            result.performance_score * 0.25 +
            result.readability_score * 0.25 +
            result.security_score * 0.15 +
            result.style_score * 0.15
        )
        
        return result
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.Assert)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.comprehension):
                complexity += 1
                if node.ifs:
                    complexity += len(node.ifs)
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        
        complexity = 0
        nesting_level = 0
        
        class CognitiveVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 0
                self.nesting = 0
                
            def visit_If(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1
                
            def visit_For(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1
                
            def visit_While(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1
                
            def visit_ExceptHandler(self, node):
                self.complexity += 1 + self.nesting
                self.nesting += 1
                self.generic_visit(node)
                self.nesting -= 1
                
            def visit_BoolOp(self, node):
                self.complexity += len(node.values) - 1
                self.generic_visit(node)
                
            def visit_Lambda(self, node):
                self.complexity += 1
                self.generic_visit(node)
        
        visitor = CognitiveVisitor()
        visitor.visit(tree)
        return visitor.complexity
    
    def _calculate_maintainability_index(self, loc: int, cc: int, ast_analyzer: ASTAnalyzer) -> float:
       
        if loc == 0:
            return 100.0
        
        halstead = self._calculate_halstead_metrics(ast_analyzer)
        volume = max(halstead['volume'], 1)
        
        mi = 171 - 5.2 * math.log(volume) - 0.23 * cc - 16.2 * math.log(loc)
        
        mi = max(0, min(100, mi * 100 / 171))
        
        return round(mi, 2)
    
    def _calculate_halstead_metrics(self, ast_analyzer: ASTAnalyzer) -> Dict[str, float]:
        
        n1 = len(ast_analyzer.operators)
        n2 = len(ast_analyzer.operands)
        N1 = sum(ast_analyzer.operators.values())
        N2 = sum(ast_analyzer.operands.values())
        
        n1 = max(n1, 1)
        n2 = max(n2, 1)
        N1 = max(N1, 1)
        N2 = max(N2, 1)
        
        vocabulary = n1 + n2
        length = N1 + N2
        volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
        difficulty = (n1 / 2) * (N2 / n2)
        effort = difficulty * volume
        bugs = volume / 3000
        
        return {
            'vocabulary': vocabulary,
            'length': length,
            'volume': round(volume, 2),
            'difficulty': round(difficulty, 2),
            'effort': round(effort, 2),
            'bugs': round(bugs, 4)
        }
    
    def _estimate_time_complexity(self, tree: ast.AST, ast_analyzer: ASTAnalyzer) -> str:
        """Estimate time complexity based on loop analysis"""
        loops = ast_analyzer.loops
        
        if not loops:
            return "O(1)"
        
        max_nesting = max(loop['depth'] for loop in loops) + 1
        
        has_recursion = self._detect_recursion(tree, ast_analyzer)
        
        has_sort = any(
            call.get('name') in ['sort', 'sorted', 'heapify', 'heappush', 'heappop']
            for call in ast_analyzer.calls
        )
        
        has_binary_search = self._detect_binary_search(tree)
        
        if has_recursion and max_nesting >= 2:
            return "O(2^n)"
        elif has_recursion:
            return "O(n)"
        elif max_nesting >= 3:
            return "O(n³)"
        elif max_nesting == 2:
            return "O(n²)"
        elif has_sort:
            return "O(n log n)"
        elif has_binary_search:
            return "O(log n)"
        elif max_nesting == 1:
            return "O(n)"
        else:
            return "O(1)"
    
    def _estimate_space_complexity(self, tree: ast.AST, ast_analyzer: ASTAnalyzer) -> str:
        """Estimate space complexity"""
        comprehensions = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)))
        
        has_recursion = self._detect_recursion(tree, ast_analyzer)
        
        creates_in_loop = self._detect_allocation_in_loop(tree)
        
        if has_recursion and creates_in_loop:
            return "O(n²)"
        elif has_recursion or creates_in_loop:
            return "O(n)"
        elif comprehensions > 0:
            return "O(n)"
        else:
            return "O(1)"
    
    def _detect_recursion(self, tree: ast.AST, ast_analyzer: ASTAnalyzer) -> bool:
        """Detect if code contains recursive function calls"""
        function_names = {f['name'] for f in ast_analyzer.functions}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name) and child.func.id == node.name:
                            return True
        return False
    
    def _detect_binary_search(self, tree: ast.AST) -> bool:
        """Detect binary search pattern"""
        code = ast.unparse(tree)
        patterns = [
            r'mid\s*=.*//\s*2',
            r'left.*right.*mid',
            r'bisect',
        ]
        return any(re.search(p, code) for p in patterns)
    
    def _detect_allocation_in_loop(self, tree: ast.AST) -> bool:
        """Detect data structure allocation inside loops"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.List, ast.Dict, ast.Set)):
                        return True
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            if child.func.id in ['list', 'dict', 'set', 'array']:
                                return True
        return False
    
    def _analyze_security(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for security vulnerabilities"""
        issues = []
        
        for category, config in self.security_patterns.items():
            for pattern in config['patterns']:
                matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_no = code[:match.start()].count('\n') + 1
                    issues.append({
                        'category': category,
                        'severity': config['severity'],
                        'message': config['message'],
                        'line': line_no,
                        'match': match.group()[:50]
                    })
        
        return issues
    
    def _analyze_style(self, code: str, lines: List[str], ast_analyzer: ASTAnalyzer) -> List[Dict[str, Any]]:
        """Analyze code style and quality"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            if len(line) > self.style_rules['line_length']:
                issues.append({
                    'type': 'line_length',
                    'severity': 'low',
                    'message': f'Line exceeds {self.style_rules["line_length"]} characters',
                    'line': i
                })
        
        for func in ast_analyzer.functions:
            if func['body_lines'] > self.style_rules['max_function_length']:
                issues.append({
                    'type': 'function_length',
                    'severity': 'medium',
                    'message': f'Function "{func["name"]}" exceeds {self.style_rules["max_function_length"]} lines',
                    'line': func['lineno']
                })
        
        for func in ast_analyzer.functions:
            if func['complexity'] > self.style_rules['max_complexity']:
                issues.append({
                    'type': 'complexity',
                    'severity': 'medium',
                    'message': f'Function "{func["name"]}" has high complexity ({func["complexity"]})',
                    'line': func['lineno']
                })
        
        for func in ast_analyzer.functions:
            if not func['has_docstring']:
                issues.append({
                    'type': 'missing_docstring',
                    'severity': 'low',
                    'message': f'Function "{func["name"]}" lacks a docstring',
                    'line': func['lineno']
                })
        
        for cls in ast_analyzer.classes:
            if not cls['has_docstring']:
                issues.append({
                    'type': 'missing_docstring',
                    'severity': 'low',
                    'message': f'Class "{cls["name"]}" lacks a docstring',
                    'line': cls['lineno']
                })
        
        return issues
    
    def _score_complexity(self, result: AnalysisResult) -> float:
        """Score based on complexity metrics"""
        score = 100.0
        
        if result.cyclomatic_complexity > 20:
            score -= 30
        elif result.cyclomatic_complexity > 10:
            score -= 15
        elif result.cyclomatic_complexity > 5:
            score -= 5
        
        if result.cognitive_complexity > 30:
            score -= 25
        elif result.cognitive_complexity > 15:
            score -= 10
        
        score = score * (result.maintainability_index / 100)
        
        return max(0, min(100, score))
    
    def _score_performance(self, result: AnalysisResult, ast_analyzer: ASTAnalyzer) -> float:
        """Score based on performance characteristics"""
        score = 100.0
        
        complexity_penalties = {
            'O(1)': 0,
            'O(log n)': 5,
            'O(n)': 10,
            'O(n log n)': 20,
            'O(n²)': 35,
            'O(n³)': 50,
            'O(2^n)': 70,
        }
        score -= complexity_penalties.get(result.time_complexity, 20)
        
        if result.nested_depth > 4:
            score -= 20
        elif result.nested_depth > 3:
            score -= 10
        
        call_count = len(ast_analyzer.calls)
        if call_count > 50:
            score -= 15
        elif call_count > 30:
            score -= 5
        
        return max(0, min(100, score))
    
    def _score_readability(self, result: AnalysisResult, lines: List[str], ast_analyzer: ASTAnalyzer) -> float:
        """Score based on readability"""
        score = 100.0
        
        if result.lines_of_code > 0:
            comment_ratio = result.comment_lines / result.lines_of_code
            if comment_ratio < 0.05:
                score -= 15
            elif comment_ratio > 0.4:
                score -= 10
        
        if ast_analyzer.functions:
            doc_ratio = sum(1 for f in ast_analyzer.functions if f['has_docstring']) / len(ast_analyzer.functions)
            score = score * (0.5 + doc_ratio * 0.5)
        
        if result.avg_function_length > 50:
            score -= 20
        elif result.avg_function_length > 30:
            score -= 10
        
        short_names = sum(1 for v in ast_analyzer.variables if len(v) == 1 and v not in 'ijkxyn')
        if short_names > 5:
            score -= 15
        
        return max(0, min(100, score))
    
    def _score_security(self, result: AnalysisResult) -> float:
        """Score based on security issues"""
        score = 100.0
        
        severity_penalties = {
            'critical': 40,
            'high': 25,
            'medium': 10,
            'low': 5,
        }
        
        for issue in result.security_issues:
            score -= severity_penalties.get(issue['severity'], 10)
        
        return max(0, min(100, score))
    
    def _score_style(self, result: AnalysisResult, lines: List[str], ast_analyzer: ASTAnalyzer) -> float:
        """Score based on code style"""
        score = 100.0
        
        for issue in result.issues:
            if issue['severity'] == 'high':
                score -= 10
            elif issue['severity'] == 'medium':
                score -= 5
            elif issue['severity'] == 'low':
                score -= 2
        
        indent_counts = defaultdict(int)
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                indent_counts[indent % 4] += 1
        
        if indent_counts and indent_counts[0] < sum(indent_counts.values()) * 0.8:
            score -= 10
        
        return max(0, min(100, score))
    
    def compare(self, result1: AnalysisResult, result2: AnalysisResult) -> Dict[str, Any]:
        """Compare two analysis results"""
        comparison = {
            'winner': None,
            'score_diff': abs(result1.total_score - result2.total_score),
            'categories': {}
        }
        
        categories = [
            ('complexity', 'complexity_score'),
            ('performance', 'performance_score'),
            ('readability', 'readability_score'),
            ('security', 'security_score'),
            ('style', 'style_score'),
        ]
        
        for name, attr in categories:
            s1 = getattr(result1, attr)
            s2 = getattr(result2, attr)
            comparison['categories'][name] = {
                'score1': s1,
                'score2': s2,
                'winner': 1 if s1 > s2 else (2 if s2 > s1 else 0),
                'diff': abs(s1 - s2)
            }
        
        if result1.total_score > result2.total_score:
            comparison['winner'] = 1
        elif result2.total_score > result1.total_score:
            comparison['winner'] = 2
        else:
            comparison['winner'] = 0
        
        return comparison


_analyzer = None

def get_analyzer() -> CodeAnalysisEngine:
    global _analyzer
    if _analyzer is None:
        _analyzer = CodeAnalysisEngine()
    return _analyzer


def analyze_code(code: str) -> AnalysisResult:
    """Convenience function to analyze code"""
    return get_analyzer().analyze(code)


def compare_code(code1: str, code2: str) -> Tuple[AnalysisResult, AnalysisResult, Dict[str, Any]]:
    """Analyze and compare two code submissions"""
    analyzer = get_analyzer()
    result1 = analyzer.analyze(code1)
    result2 = analyzer.analyze(code2)
    comparison = analyzer.compare(result1, result2)
    return result1, result2, comparison
