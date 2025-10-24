#!/usr/bin/env python3
"""
🚀 ManageBac统一启动器 - 整合所有启动方式
Unified Launcher - Consolidates all launch methods
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


class UnifiedLauncher:
    """统一启动器，整合所有启动功能。"""

    def __init__(self) -> None:
        """初始化统一启动器。"""
        self.workspace = Path(__file__).parent.parent
        self.venv_path = self.workspace / "venv"

    def run(self, mode: str = "auto") -> int:
        """
        运行应用程序。

        Args:
            mode: 运行模式 (auto/cli/gui)

        Returns:
            退出代码
        """
        print("🚀 ManageBac统一启动器 | Unified Launcher")
        print("=" * 60)

        # 检查环境
        if not self._check_environment():
            return 1

        # 根据模式启动
        if mode == "auto":
            return self._auto_launch()
        elif mode == "cli":
            return self._launch_cli()
        elif mode == "gui":
            return self._launch_gui()
        else:
            print(f"❌ 未知模式: {mode}")
            return 1

    def _check_environment(self) -> bool:
        """检查运行环境。"""
        # 检查虚拟环境
        if not self.venv_path.exists():
            print("❌ 虚拟环境不存在")
            print("   请先运行安装程序:")
            print("   python unified_installer.py")
            return False

        # 检查配置文件
        config_file = self.workspace / ".env"
        if not config_file.exists():
            print("⚠️ 配置文件不存在")
            print("   请创建.env文件或复制config.example.env")
            return False

        print("✅ 环境检查通过")
        return True

    def _auto_launch(self) -> int:
        """自动选择最佳启动方式。"""
        print("\n🔍 自动检测最佳启动方式...")

        # 检查是否有图形界面支持
        if self._check_gui_support():
            print("✅ 检测到图形界面支持，启动GUI")
            return self._launch_gui()
        else:
            print("ℹ️ 未检测到图形界面，启动CLI")
            return self._launch_cli()

    def _launch_cli(self) -> int:
        """启动命令行界面。"""
        print("\n💻 启动命令行界面...")

        python_cmd = self._get_python_command()
        main_script = self.workspace / "main.py"

        try:
            result = subprocess.run([python_cmd, str(main_script)], check=False)
            return result.returncode
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return 1

    def _launch_gui(self) -> int:
        """启动图形界面。"""
        print("\n🎨 启动图形界面...")

        python_cmd = self._get_python_command()
        gui_script = self.workspace / "gui_launcher.py"

        if not gui_script.exists():
            print("⚠️ GUI启动器不存在，回退到CLI")
            return self._launch_cli()

        try:
            result = subprocess.run([python_cmd, str(gui_script)], check=False)
            return result.returncode
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return 1

    def _check_gui_support(self) -> bool:
        """检查是否支持图形界面。"""
        try:
            import tkinter

            root = tkinter.Tk()
            root.withdraw()
            root.destroy()
            return True
        except Exception:
            return False

    def _get_python_command(self) -> str:
        """获取Python命令路径。"""
        if os.name == "nt":  # Windows
            return str(self.venv_path / "Scripts" / "python.exe")
        else:  # Unix-like
            return str(self.venv_path / "bin" / "python")


def main() -> int:
    """主函数。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="ManageBac统一启动器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["auto", "cli", "gui"],
        default="auto",
        help="启动模式 (默认: auto)",
    )

    args = parser.parse_args()

    launcher = UnifiedLauncher()
    return launcher.run(args.mode)


if __name__ == "__main__":
    sys.exit(main())
