#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚨 Comprehensive Error Handler | 综合错误处理器
Advanced error handling and user feedback system
高级错误处理和用户反馈系统
"""

import os
import sys
import traceback
import logging
import json
import time
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

class Colors:
    """Console colors"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ErrorCategory:
    """错误分类"""
    SYSTEM = "system"
    NETWORK = "network"
    DEPENDENCY = "dependency"
    CONFIGURATION = "configuration"
    USER_INPUT = "user_input"
    PERMISSION = "permission"
    FILE_IO = "file_io"
    UNKNOWN = "unknown"

class ErrorSeverity:
    """错误严重程度"""
    CRITICAL = "critical"  # 应用无法继续运行
    HIGH = "high"         # 主要功能受影响
    MEDIUM = "medium"     # 部分功能受影响
    LOW = "low"          # 轻微问题，不影响主要功能
    INFO = "info"        # 仅为信息提示

class ComprehensiveErrorHandler:
    """综合错误处理器"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.error_log_file = self.project_root / "logs" / "error.log"

        # 确保日志目录存在
        self.error_log_file.parent.mkdir(exist_ok=True)

        # 配置日志
        self.setup_logging()

        # 错误统计
        self.error_stats = {
            'total_errors': 0,
            'by_category': {},
            'by_severity': {},
            'resolved_count': 0,
            'session_start': time.time()
        }

        # 解决方案数据库
        self.solutions_db = self.load_solutions_database()

    def setup_logging(self):
        """设置日志系统"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.error_log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_solutions_database(self) -> Dict:
        """加载解决方案数据库"""
        return {
            # 依赖相关错误
            "ModuleNotFoundError": {
                "category": ErrorCategory.DEPENDENCY,
                "severity": ErrorSeverity.HIGH,
                "solutions": [
                    "运行: python 优化安装器.py",
                    "运行: python ultimate_installer.py",
                    "手动安装依赖: pip install -r requirements.txt",
                    "检查Python环境: python --version",
                    "使用虚拟环境: python -m venv venv && source venv/bin/activate"
                ],
                "auto_fix": self.fix_missing_module
            },

            # 网络相关错误
            "ConnectionError": {
                "category": ErrorCategory.NETWORK,
                "severity": ErrorSeverity.MEDIUM,
                "solutions": [
                    "检查网络连接",
                    "尝试使用VPN",
                    "检查防火墙设置",
                    "使用离线模式: --offline"
                ]
            },

            # 权限相关错误
            "PermissionError": {
                "category": ErrorCategory.PERMISSION,
                "severity": ErrorSeverity.HIGH,
                "solutions": [
                    "使用管理员权限运行",
                    "macOS: sudo python script.py",
                    "Windows: 以管理员身份运行命令提示符",
                    "检查文件权限: ls -la"
                ],
                "auto_fix": self.fix_permission_error
            },

            # 配置相关错误
            "FileNotFoundError": {
                "category": ErrorCategory.CONFIGURATION,
                "severity": ErrorSeverity.MEDIUM,
                "solutions": [
                    "检查文件路径是否正确",
                    "运行初始化: python 优化安装器.py",
                    "复制示例配置: cp config.example.env .env",
                    "手动创建缺失文件"
                ],
                "auto_fix": self.fix_missing_file
            },

            # 用户输入错误
            "ValueError": {
                "category": ErrorCategory.USER_INPUT,
                "severity": ErrorSeverity.LOW,
                "solutions": [
                    "检查输入格式",
                    "查看帮助文档: --help",
                    "使用默认值",
                    "重新输入正确的值"
                ]
            }
        }

    def handle_exception(self, exc_type, exc_value, exc_traceback,
                        context: Optional[str] = None,
                        user_action: Optional[str] = None) -> bool:
        """处理异常"""
        # 生成错误ID
        error_id = f"ERR_{int(time.time())}"

        # 获取错误信息
        error_info = {
            'id': error_id,
            'timestamp': datetime.now().isoformat(),
            'type': exc_type.__name__ if exc_type else 'Unknown',
            'message': str(exc_value) if exc_value else 'No message',
            'traceback': ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)) if exc_traceback else 'No traceback',
            'context': context or 'Unknown context',
            'user_action': user_action or 'Unknown action',
            'system_info': self.get_system_info(),
            'resolved': False
        }

        # 记录错误
        self.log_error(error_info)

        # 分析错误
        analysis = self.analyze_error(error_info)

        # 尝试自动修复
        auto_fixed = self.attempt_auto_fix(error_info, analysis)

        if auto_fixed:
            print(f"{Colors.GREEN}✅ 错误已自动修复{Colors.END}")
            return True

        # 控制台输出
        self.print_error_summary(error_info, analysis)

        return False

    def analyze_error(self, error_info: Dict) -> Dict:
        """分析错误"""
        error_type = error_info['type']
        error_message = error_info['message']

        # 查找解决方案
        solution_info = None
        for pattern, info in self.solutions_db.items():
            if pattern in error_type or pattern in error_message:
                solution_info = info
                break

        if not solution_info:
            solution_info = {
                "category": ErrorCategory.UNKNOWN,
                "severity": ErrorSeverity.MEDIUM,
                "solutions": ["请查看错误日志获取更多信息", "尝试重新启动应用程序"]
            }

        # 更新统计
        self.update_error_stats(solution_info)

        return {
            'category': solution_info['category'],
            'severity': solution_info['severity'],
            'solutions': solution_info['solutions'],
            'auto_fix_available': 'auto_fix' in solution_info,
            'auto_fix_func': solution_info.get('auto_fix')
        }

    def attempt_auto_fix(self, error_info: Dict, analysis: Dict) -> bool:
        """尝试自动修复"""
        if not analysis.get('auto_fix_available'):
            return False

        auto_fix_func = analysis.get('auto_fix_func')
        if not auto_fix_func:
            return False

        try:
            print(f"{Colors.BLUE}🔧 尝试自动修复...{Colors.END}")
            success = auto_fix_func(error_info)

            if success:
                error_info['resolved'] = True
                self.error_stats['resolved_count'] += 1
                self.logger.info(f"Error {error_info['id']} auto-fixed successfully")

            return success
        except Exception as e:
            self.logger.error(f"Auto-fix failed for {error_info['id']}: {e}")
            return False

    def print_error_summary(self, error_info: Dict, analysis: Dict):
        """打印错误摘要"""
        print(f"\n{Colors.RED}{'='*80}{Colors.END}")
        print(f"{Colors.RED}💥 ERROR REPORT | 错误报告{Colors.END}")
        print(f"{Colors.RED}{'='*80}{Colors.END}")

        print(f"{Colors.YELLOW}🆔 Error ID | 错误ID:{Colors.END} {error_info['id']}")
        print(f"{Colors.YELLOW}📅 Time | 时间:{Colors.END} {error_info['timestamp']}")
        print(f"{Colors.YELLOW}🏷️  Type | 类型:{Colors.END} {error_info['type']}")
        print(f"{Colors.YELLOW}📂 Category | 类别:{Colors.END} {analysis['category']}")
        print(f"{Colors.YELLOW}⚠️  Severity | 严重程度:{Colors.END} {analysis['severity']}")
        print(f"{Colors.YELLOW}💬 Message | 消息:{Colors.END} {error_info['message']}")

        if error_info.get('context'):
            print(f"{Colors.YELLOW}📍 Context | 上下文:{Colors.END} {error_info['context']}")

        print(f"\n{Colors.CYAN}🔧 SOLUTIONS | 解决方案:{Colors.END}")
        for i, solution in enumerate(analysis['solutions'], 1):
            print(f"   {i}. {solution}")

        if analysis.get('auto_fix_available'):
            print(f"\n{Colors.GREEN}🤖 Auto-fix available | 可自动修复{Colors.END}")

        print(f"\n{Colors.BLUE}📊 Session Stats | 会话统计:{Colors.END}")
        print(f"   Total errors: {self.error_stats['total_errors']}")
        print(f"   Resolved: {self.error_stats['resolved_count']}")

        print(f"\n{Colors.CYAN}💡 Need help? | 需要帮助？{Colors.END}")
        print(f"   • Check logs: {self.error_log_file}")
        print(f"   • Run installer: python 优化安装器.py")
        print(f"   • Use intelligent launcher: python intelligent_launcher.py")

        print(f"{Colors.RED}{'='*80}{Colors.END}\n")

    def log_error(self, error_info: Dict):
        """记录错误到日志"""
        self.logger.error(f"[{error_info['id']}] {error_info['type']}: {error_info['message']}")
        self.logger.debug(f"[{error_info['id']}] Context: {error_info['context']}")
        self.logger.debug(f"[{error_info['id']}] Traceback:\n{error_info['traceback']}")

    def update_error_stats(self, solution_info: Dict):
        """更新错误统计"""
        self.error_stats['total_errors'] += 1

        category = solution_info['category']
        severity = solution_info['severity']

        self.error_stats['by_category'][category] = self.error_stats['by_category'].get(category, 0) + 1
        self.error_stats['by_severity'][severity] = self.error_stats['by_severity'].get(severity, 0) + 1

    def get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'python_version': sys.version,
            'python_executable': sys.executable,
            'working_directory': str(Path.cwd()),
            'project_root': str(self.project_root)
        }

    # 自动修复函数
    def fix_missing_module(self, error_info: Dict) -> bool:
        """修复缺失模块"""
        try:
            # 尝试自动安装缺失的模块
            module_name = self.extract_module_name(error_info['message'])
            if module_name:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', module_name
                ], check=True, capture_output=True)
                return True
        except:
            pass
        return False

    def fix_permission_error(self, error_info: Dict) -> bool:
        """修复权限错误"""
        try:
            # 尝试修改文件权限
            file_path = self.extract_file_path(error_info['message'])
            if file_path and Path(file_path).exists():
                os.chmod(file_path, 0o755)
                return True
        except:
            pass
        return False

    def fix_missing_file(self, error_info: Dict) -> bool:
        """修复缺失文件"""
        try:
            # 尝试创建缺失的配置文件
            if '.env' in error_info['message']:
                config_example = self.project_root / 'config.example.env'
                env_file = self.project_root / '.env'
                if config_example.exists() and not env_file.exists():
                    import shutil
                    shutil.copy2(config_example, env_file)
                    return True
        except:
            pass
        return False

    def extract_module_name(self, error_message: str) -> Optional[str]:
        """从错误消息中提取模块名"""
        import re
        match = re.search(r"No module named '([^']+)'", error_message)
        if match:
            return match.group(1)
        return None

    def extract_file_path(self, error_message: str) -> Optional[str]:
        """从错误消息中提取文件路径"""
        import re
        match = re.search(r"['\"]([^'\"]+)['\"]", error_message)
        if match:
            return match.group(1)
        return None

def setup_global_exception_handler():
    """设置全局异常处理器"""
    error_handler = ComprehensiveErrorHandler()

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_handler.handle_exception(
            exc_type, exc_value, exc_traceback,
            context="Global exception handler",
            user_action="Application execution"
        )

    sys.excepthook = handle_exception
    return error_handler

def with_error_handling(context: str = "Unknown"):
    """装饰器：为函数添加错误处理"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = ComprehensiveErrorHandler()
                error_handler.handle_exception(
                    type(e), e, e.__traceback__,
                    context=context,
                    user_action=f"Calling {func.__name__}"
                )
                return None
        return wrapper
    return decorator

if __name__ == "__main__":
    # 测试错误处理器
    error_handler = ComprehensiveErrorHandler()
    print("Error handler initialized and ready to use!")
    print("Use setup_global_exception_handler() to enable global error handling.")