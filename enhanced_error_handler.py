#!/usr/bin/env python3
"""
Enhanced Error Handler and Logging System
增强的错误处理和日志系统
"""

import os
import sys
import logging
import traceback
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import platform


class EnhancedErrorHandler:
    """Enhanced error handling with comprehensive logging and user feedback"""

    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create logger
        self.logger = self._setup_logger(log_level)

        # Error statistics
        self.error_stats = {
            "total_errors": 0,
            "error_types": {},
            "session_start": datetime.now().isoformat(),
            "last_error": None
        }

        # Load previous error history
        self._load_error_history()

    def _setup_logger(self, log_level: str) -> logging.Logger:
        """Setup comprehensive logging system"""
        logger = logging.getLogger("managebac_checker")
        logger.setLevel(getattr(logging, log_level.upper()))

        # Clear existing handlers
        logger.handlers.clear()

        # File handler for general logs
        log_file = self.log_dir / f"managebac_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Error-specific file handler
        error_file = self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Apply formatters
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console_handler)

        return logger

    def _load_error_history(self):
        """Load error history from previous sessions"""
        history_file = self.log_dir / "error_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    self.error_stats.update(history)
            except Exception as e:
                self.logger.warning(f"Could not load error history: {e}")

    def _save_error_history(self):
        """Save error history for future sessions"""
        history_file = self.log_dir / "error_history.json"
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.error_stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.warning(f"Could not save error history: {e}")

    def handle_error(self, error: Exception, context: str = "",
                    severity: str = "ERROR", user_friendly: bool = True) -> Dict[str, Any]:
        """
        Handle errors with comprehensive logging and user feedback

        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            severity: Error severity level (ERROR, CRITICAL, WARNING)
            user_friendly: Whether to show user-friendly messages

        Returns:
            Dictionary with error information and suggested actions
        """
        error_type = type(error).__name__
        error_msg = str(error)
        timestamp = datetime.now().isoformat()

        # Update statistics
        self.error_stats["total_errors"] += 1
        self.error_stats["error_types"][error_type] = self.error_stats["error_types"].get(error_type, 0) + 1
        self.error_stats["last_error"] = timestamp

        # Get system info
        system_info = {
            "platform": platform.system(),
            "platform_version": platform.platform(),
            "python_version": sys.version,
            "working_directory": os.getcwd()
        }

        # Create comprehensive error record
        error_record = {
            "timestamp": timestamp,
            "error_type": error_type,
            "error_message": error_msg,
            "context": context,
            "severity": severity,
            "traceback": traceback.format_exc(),
            "system_info": system_info
        }

        # Log the error
        log_message = f"[{context}] {error_type}: {error_msg}"
        if severity == "CRITICAL":
            self.logger.critical(log_message)
        elif severity == "ERROR":
            self.logger.error(log_message)
        elif severity == "WARNING":
            self.logger.warning(log_message)

        # Log detailed traceback at debug level
        self.logger.debug(f"Full traceback for {error_type}:\n{traceback.format_exc()}")

        # Generate user-friendly response
        response = self._generate_user_response(error_record, user_friendly)

        # Save error history
        self._save_error_history()

        return response

    def _generate_user_response(self, error_record: Dict[str, Any], user_friendly: bool) -> Dict[str, Any]:
        """Generate user-friendly error response with suggestions"""
        error_type = error_record["error_type"]
        error_msg = error_record["error_message"]
        context = error_record["context"]

        # Known error patterns and solutions
        error_solutions = {
            "ModuleNotFoundError": {
                "description": "Missing Python package",
                "solutions": [
                    "Install missing package: pip install <package_name>",
                    "Check if you're using the correct Python environment",
                    "Run: pip install -r requirements.txt"
                ]
            },
            "FileNotFoundError": {
                "description": "Required file is missing",
                "solutions": [
                    "Check if the file path is correct",
                    "Ensure the file exists and has proper permissions",
                    "Try running from the correct directory"
                ]
            },
            "PermissionError": {
                "description": "Insufficient permissions",
                "solutions": [
                    "Run with administrator/sudo privileges",
                    "Check file/directory permissions",
                    "Ensure you have write access to the target location"
                ]
            },
            "ConnectionError": {
                "description": "Network connection issue",
                "solutions": [
                    "Check your internet connection",
                    "Verify ManageBac URL and credentials",
                    "Try again in a few minutes"
                ]
            },
            "AttributeError": {
                "description": "Object attribute access issue",
                "solutions": [
                    "Check if the object is properly initialized",
                    "Verify the attribute name is correct",
                    "Update to the latest version"
                ]
            }
        }

        # Get specific solution or use generic one
        solution_info = error_solutions.get(error_type, {
            "description": "An unexpected error occurred",
            "solutions": [
                "Try restarting the application",
                "Check the log files for more details",
                "Report this issue if it persists"
            ]
        })

        response = {
            "error_type": error_type,
            "error_message": error_msg,
            "context": context,
            "timestamp": error_record["timestamp"],
            "severity": error_record["severity"],
            "description": solution_info["description"],
            "solutions": solution_info["solutions"],
            "log_file": str(self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log")
        }

        if user_friendly:
            # Print user-friendly error message
            print(f"\n{'='*60}")
            print(f"❌ {solution_info['description']}")
            print(f"📍 Context: {context}")
            print(f"🔍 Error: {error_type} - {error_msg}")
            print(f"\n💡 Suggested solutions:")
            for i, solution in enumerate(solution_info['solutions'], 1):
                print(f"   {i}. {solution}")
            print(f"\n📋 Full details logged to: {response['log_file']}")
            print(f"{'='*60}\n")

        return response

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get comprehensive error statistics"""
        return {
            **self.error_stats,
            "session_duration": str(datetime.now() - datetime.fromisoformat(self.error_stats["session_start"])),
            "log_directory": str(self.log_dir)
        }

    def create_error_report(self, include_logs: bool = False) -> str:
        """Create a comprehensive error report"""
        stats = self.get_error_statistics()

        report = f"""
📊 ManageBac Checker Error Report
================================

📅 Session Start: {stats['session_start']}
⏱️  Session Duration: {stats['session_duration']}
🔢 Total Errors: {stats['total_errors']}
📝 Log Directory: {stats['log_directory']}

📋 Error Types:
"""

        for error_type, count in stats['error_types'].items():
            percentage = (count / stats['total_errors'] * 100) if stats['total_errors'] > 0 else 0
            report += f"   • {error_type}: {count} ({percentage:.1f}%)\n"

        if include_logs:
            report += "\n📂 Recent Log Files:\n"
            for log_file in self.log_dir.glob("*.log"):
                size = log_file.stat().st_size
                report += f"   • {log_file.name}: {size:,} bytes\n"

        return report

    def cleanup_old_logs(self, days: int = 30):
        """Clean up log files older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cleaned_count = 0

        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    cleaned_count += 1
                    self.logger.info(f"Cleaned up old log file: {log_file.name}")
                except Exception as e:
                    self.logger.warning(f"Could not clean up {log_file.name}: {e}")

        self.logger.info(f"Cleaned up {cleaned_count} old log files")
        return cleaned_count


# Global error handler instance
_global_error_handler: Optional[EnhancedErrorHandler] = None

def get_error_handler() -> EnhancedErrorHandler:
    """Get the global error handler instance"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = EnhancedErrorHandler()
    return _global_error_handler

def handle_error(error: Exception, context: str = "", severity: str = "ERROR", user_friendly: bool = True) -> Dict[str, Any]:
    """Convenience function to handle errors using the global handler"""
    return get_error_handler().handle_error(error, context, severity, user_friendly)

def log_info(message: str):
    """Log info message"""
    get_error_handler().logger.info(message)

def log_warning(message: str):
    """Log warning message"""
    get_error_handler().logger.warning(message)

def log_error(message: str):
    """Log error message"""
    get_error_handler().logger.error(message)

def log_debug(message: str):
    """Log debug message"""
    get_error_handler().logger.debug(message)


if __name__ == "__main__":
    # Test the error handler
    print("🧪 Testing Enhanced Error Handler...")

    handler = EnhancedErrorHandler()

    # Test different types of errors
    try:
        raise ModuleNotFoundError("test_module not found")
    except Exception as e:
        handler.handle_error(e, "Testing module error", "ERROR")

    try:
        raise FileNotFoundError("test_file.txt not found")
    except Exception as e:
        handler.handle_error(e, "Testing file error", "WARNING")

    try:
        raise ConnectionError("Cannot connect to server")
    except Exception as e:
        handler.handle_error(e, "Testing connection error", "CRITICAL")

    # Show statistics
    print("\n📊 Error Statistics:")
    stats = handler.get_error_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Show error report
    print(handler.create_error_report(include_logs=True))

    print("✅ Error handler testing complete!")