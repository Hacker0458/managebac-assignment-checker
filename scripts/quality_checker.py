#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Code Quality Checker for ManageBac Assignment Checker
ManageBac作业检查器代码质量检查器
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import time

class QualityChecker:
    """Code quality checking utilities | 代码质量检查工具"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = {}
        self.start_time = time.time()
        
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all quality checks | 运行所有质量检查"""
        print("🔍 Running comprehensive code quality checks...")
        print("🔍 运行全面的代码质量检查...")
        
        checks = [
            ("black", self._check_black_formatting),
            ("flake8", self._check_flake8_linting),
            ("mypy", self._check_mypy_types),
            ("bandit", self._check_bandit_security),
            ("safety", self._check_safety_dependencies),
            ("pytest", self._check_pytest_tests),
            ("coverage", self._check_coverage),
            ("complexity", self._check_complexity),
            ("duplicates", self._check_duplicates),
            ("imports", self._check_imports)
        ]
        
        for name, check_func in checks:
            print(f"\n🔍 Running {name} check...")
            try:
                result = check_func()
                self.results[name] = result
                status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
                print(f"  {status} - {result.get('message', 'No message')}")
            except Exception as e:
                self.results[name] = {
                    'success': False,
                    'error': str(e),
                    'message': f"Check failed with error: {e}"
                }
                print(f"  ❌ ERROR - {e}")
        
        # Generate summary
        self.results['summary'] = self._generate_summary()
        
        return self.results
    
    def _check_black_formatting(self) -> Dict[str, Any]:
        """Check code formatting with black | 使用black检查代码格式"""
        try:
            result = subprocess.run(
                ['black', '--check', '--diff', 'managebac_checker/', 'tests/'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'Code is properly formatted',
                    'details': 'All files follow black formatting standards'
                }
            else:
                return {
                    'success': False,
                    'message': 'Code formatting issues found',
                    'details': result.stdout,
                    'suggestion': 'Run: black managebac_checker/ tests/'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'black not found',
                'message': 'Black formatter not installed',
                'suggestion': 'Install with: pip install black'
            }
    
    def _check_flake8_linting(self) -> Dict[str, Any]:
        """Check code linting with flake8 | 使用flake8检查代码规范"""
        try:
            result = subprocess.run(
                ['flake8', 'managebac_checker/', 'tests/'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'No linting issues found',
                    'details': 'Code follows PEP 8 standards'
                }
            else:
                issues = result.stdout.strip().split('\n')
                return {
                    'success': False,
                    'message': f'{len(issues)} linting issues found',
                    'details': result.stdout,
                    'suggestion': 'Fix issues or configure flake8'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'flake8 not found',
                'message': 'Flake8 linter not installed',
                'suggestion': 'Install with: pip install flake8'
            }
    
    def _check_mypy_types(self) -> Dict[str, Any]:
        """Check type hints with mypy | 使用mypy检查类型提示"""
        try:
            result = subprocess.run(
                ['mypy', 'managebac_checker/'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'No type errors found',
                    'details': 'All type hints are correct'
                }
            else:
                return {
                    'success': False,
                    'message': 'Type checking issues found',
                    'details': result.stdout,
                    'suggestion': 'Fix type annotations'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'mypy not found',
                'message': 'MyPy type checker not installed',
                'suggestion': 'Install with: pip install mypy'
            }
    
    def _check_bandit_security(self) -> Dict[str, Any]:
        """Check security issues with bandit | 使用bandit检查安全问题"""
        try:
            result = subprocess.run(
                ['bandit', '-r', 'managebac_checker/', '-f', 'json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'No security issues found',
                    'details': 'Code passed security checks'
                }
            else:
                try:
                    issues = json.loads(result.stdout)
                    return {
                        'success': False,
                        'message': f'{len(issues.get("results", []))} security issues found',
                        'details': result.stdout,
                        'suggestion': 'Review and fix security issues'
                    }
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'message': 'Security issues found',
                        'details': result.stdout,
                        'suggestion': 'Review bandit output'
                    }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'bandit not found',
                'message': 'Bandit security checker not installed',
                'suggestion': 'Install with: pip install bandit'
            }
    
    def _check_safety_dependencies(self) -> Dict[str, Any]:
        """Check dependency vulnerabilities with safety | 使用safety检查依赖漏洞"""
        try:
            result = subprocess.run(
                ['safety', 'check', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'No dependency vulnerabilities found',
                    'details': 'All dependencies are secure'
                }
            else:
                try:
                    vulnerabilities = json.loads(result.stdout)
                    return {
                        'success': False,
                        'message': f'{len(vulnerabilities)} vulnerabilities found',
                        'details': result.stdout,
                        'suggestion': 'Update vulnerable dependencies'
                    }
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'message': 'Dependency vulnerabilities found',
                        'details': result.stdout,
                        'suggestion': 'Review safety output'
                    }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'safety not found',
                'message': 'Safety dependency checker not installed',
                'suggestion': 'Install with: pip install safety'
            }
    
    def _check_pytest_tests(self) -> Dict[str, Any]:
        """Check test execution with pytest | 使用pytest检查测试执行"""
        try:
            result = subprocess.run(
                ['pytest', 'tests/', '-v', '--tb=short'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'All tests passed',
                    'details': 'Test suite is healthy'
                }
            else:
                return {
                    'success': False,
                    'message': 'Some tests failed',
                    'details': result.stdout,
                    'suggestion': 'Fix failing tests'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'pytest not found',
                'message': 'Pytest test runner not installed',
                'suggestion': 'Install with: pip install pytest'
            }
    
    def _check_coverage(self) -> Dict[str, Any]:
        """Check test coverage | 检查测试覆盖率"""
        try:
            result = subprocess.run(
                ['pytest', 'tests/', '--cov=managebac_checker', '--cov-report=term-missing'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Extract coverage percentage from output
            coverage_line = [line for line in result.stdout.split('\n') if 'TOTAL' in line]
            if coverage_line:
                coverage_percent = coverage_line[0].split()[-1].replace('%', '')
                try:
                    coverage_float = float(coverage_percent)
                    if coverage_float >= 80:
                        return {
                            'success': True,
                            'message': f'Coverage: {coverage_float}%',
                            'details': 'Good test coverage achieved'
                        }
                    else:
                        return {
                            'success': False,
                            'message': f'Coverage: {coverage_float}% (target: 80%)',
                            'details': 'Test coverage is below target',
                            'suggestion': 'Add more tests to improve coverage'
                        }
                except ValueError:
                    pass
            
            return {
                'success': True,
                'message': 'Coverage check completed',
                'details': result.stdout
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'pytest-cov not found',
                'message': 'Coverage plugin not installed',
                'suggestion': 'Install with: pip install pytest-cov'
            }
    
    def _check_complexity(self) -> Dict[str, Any]:
        """Check code complexity | 检查代码复杂度"""
        try:
            result = subprocess.run(
                ['radon', 'cc', 'managebac_checker/', '-a'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Count complexity issues
            lines = result.stdout.strip().split('\n')
            high_complexity = [line for line in lines if any(level in line for level in ['C', 'D', 'E', 'F'])]
            
            if not high_complexity:
                return {
                    'success': True,
                    'message': 'No complexity issues found',
                    'details': 'Code complexity is acceptable'
                }
            else:
                return {
                    'success': False,
                    'message': f'{len(high_complexity)} complexity issues found',
                    'details': result.stdout,
                    'suggestion': 'Refactor complex functions'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'radon not found',
                'message': 'Radon complexity checker not installed',
                'suggestion': 'Install with: pip install radon'
            }
    
    def _check_duplicates(self) -> Dict[str, Any]:
        """Check for code duplicates | 检查代码重复"""
        try:
            result = subprocess.run(
                ['flake8', '--select=D', 'managebac_checker/'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'No duplicate code found',
                    'details': 'Code is DRY (Don\'t Repeat Yourself)'
                }
            else:
                duplicates = result.stdout.strip().split('\n')
                return {
                    'success': False,
                    'message': f'{len(duplicates)} duplicate code issues found',
                    'details': result.stdout,
                    'suggestion': 'Refactor duplicate code'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'flake8 not found',
                'message': 'Flake8 linter not installed',
                'suggestion': 'Install with: pip install flake8'
            }
    
    def _check_imports(self) -> Dict[str, Any]:
        """Check import organization | 检查导入组织"""
        try:
            result = subprocess.run(
                ['isort', '--check-only', '--diff', 'managebac_checker/', 'tests/'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'Imports are properly organized',
                    'details': 'All imports follow isort standards'
                }
            else:
                return {
                    'success': False,
                    'message': 'Import organization issues found',
                    'details': result.stdout,
                    'suggestion': 'Run: isort managebac_checker/ tests/'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'isort not found',
                'message': 'Import sort tool not installed',
                'suggestion': 'Install with: pip install isort'
            }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate quality check summary | 生成质量检查摘要"""
        total_checks = len(self.results) - 1  # Exclude summary itself
        passed_checks = sum(1 for result in self.results.values() 
                          if isinstance(result, dict) and result.get('success', False))
        failed_checks = total_checks - passed_checks
        
        runtime = time.time() - self.start_time
        
        return {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': failed_checks,
            'success_rate': round((passed_checks / total_checks) * 100, 2) if total_checks > 0 else 0,
            'runtime_seconds': round(runtime, 2),
            'overall_status': 'PASS' if failed_checks == 0 else 'FAIL'
        }
    
    def save_report(self, filename: str = "quality_report.json"):
        """Save quality report to file | 保存质量报告到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"📊 Quality report saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save quality report: {e}")
            return False

def main():
    """Main quality check function | 主质量检查函数"""
    print("🔍 ManageBac Assignment Checker Quality Checker")
    print("🔍 ManageBac作业检查器质量检查器")
    print("=" * 60)
    
    checker = QualityChecker()
    
    try:
        # Run all checks
        results = checker.run_all_checks()
        
        # Display summary
        summary = results.get('summary', {})
        print(f"\n📊 Quality Check Summary:")
        print(f"  Total Checks: {summary.get('total_checks', 0)}")
        print(f"  Passed: {summary.get('passed_checks', 0)}")
        print(f"  Failed: {summary.get('failed_checks', 0)}")
        print(f"  Success Rate: {summary.get('success_rate', 0)}%")
        print(f"  Runtime: {summary.get('runtime_seconds', 0)}s")
        print(f"  Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
        
        # Save report
        checker.save_report()
        
        if summary.get('overall_status') == 'PASS':
            print("\n✅ All quality checks passed!")
        else:
            print("\n⚠️ Some quality checks failed. Review the report for details.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Quality check interrupted by user")
    except Exception as e:
        print(f"\n❌ Quality check failed: {e}")

if __name__ == "__main__":
    main()
