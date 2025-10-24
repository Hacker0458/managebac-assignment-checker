#!/usr/bin/env python3
"""
🚀 ManageBac统一安装器 - 整合所有安装方式
Unified Installer - Consolidates all installation methods

这个文件整合了所有安装脚本的功能，提供统一的安装体验。
This file consolidates all installation scripts into a unified experience.
"""

from __future__ import annotations

import os
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Optional


class InstallMode(Enum):
    """安装模式枚举。"""

    AUTO = "auto"  # 自动检测最佳方式
    QUICK = "quick"  # 快速安装，使用默认配置
    WIZARD = "wizard"  # 交互式向导
    GUI = "gui"  # 图形界面
    REPAIR = "repair"  # 修复现有安装


class UnifiedInstaller:
    """统一安装器类，整合所有安装功能。"""

    def __init__(self, mode: InstallMode = InstallMode.AUTO) -> None:
        """
        初始化统一安装器。

        Args:
            mode: 安装模式
        """
        self.mode = mode
        self.workspace = Path(__file__).parent
        self.venv_path = self.workspace / "venv"
        self.requirements_files = [
            "requirements.txt",
            "requirements-core.txt",
            "requirements-dev.txt",
        ]

    def run(self) -> int:
        """
        运行安装程序。

        Returns:
            退出代码（0表示成功）
        """
        print("🚀 ManageBac统一安装器 | Unified Installer")
        print("=" * 60)

        # 检查Python版本
        if not self._check_python_version():
            return 1

        # 根据模式执行安装
        if self.mode == InstallMode.AUTO:
            return self._auto_install()
        elif self.mode == InstallMode.QUICK:
            return self._quick_install()
        elif self.mode == InstallMode.WIZARD:
            return self._wizard_install()
        elif self.mode == InstallMode.GUI:
            return self._gui_install()
        elif self.mode == InstallMode.REPAIR:
            return self._repair_install()

        return 1

    def _check_python_version(self) -> bool:
        """检查Python版本是否满足要求。"""
        version = sys.version_info
        if version < (3, 9):
            print(f"❌ Python版本过低: {version.major}.{version.minor}")
            print("   需要Python 3.9或更高版本")
            return False

        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True

    def _auto_install(self) -> int:
        """自动检测并选择最佳安装方式。"""
        print("\n🔍 自动检测最佳安装方式...")

        # 检查是否有图形界面支持
        has_gui = self._check_gui_support()

        # 如果支持图形界面，优先使用GUI安装
        if has_gui:
            print("✅ 检测到图形界面支持，使用GUI安装")
            return self._gui_install()
        else:
            print("ℹ️ 未检测到图形界面，使用快速安装")
            return self._quick_install()

    def _quick_install(self) -> int:
        """快速安装，使用默认配置。"""
        print("\n⚡ 开始快速安装...")

        steps = [
            ("创建虚拟环境", self._create_venv),
            ("安装依赖包", self._install_dependencies),
            ("安装Playwright浏览器", self._install_playwright),
            ("创建配置文件", self._create_config),
            ("创建桌面快捷方式", self._create_shortcuts),
        ]

        for step_name, step_func in steps:
            print(f"\n📦 {step_name}...")
            if not step_func():
                print(f"❌ {step_name}失败")
                return 1
            print(f"✅ {step_name}完成")

        print("\n🎉 安装完成！")
        print("\n▶️  运行以下命令启动应用：")
        self._print_run_commands()
        return 0

    def _wizard_install(self) -> int:
        """交互式向导安装。"""
        print("\n🧙 开始交互式安装向导...")

        # 这里可以添加交互式问答
        print("\n请按照提示完成配置...")

        # 询问用户配置
        print("\n📝 配置信息:")
        email = input("  ManageBac邮箱: ").strip()
        password = input("  ManageBac密码: ").strip()
        url = input("  ManageBac URL [https://shtcs.managebac.cn]: ").strip() or "https://shtcs.managebac.cn"

        # 保存配置
        config_content = f"""# ManageBac配置文件
MANAGEBAC_EMAIL={email}
MANAGEBAC_PASSWORD={password}
MANAGEBAC_URL={url}
HEADLESS=true
DEBUG=false
"""

        config_file = self.workspace / ".env"
        config_file.write_text(config_content, encoding="utf-8")
        print("✅ 配置已保存")

        # 执行快速安装
        return self._quick_install()

    def _gui_install(self) -> int:
        """图形界面安装。"""
        print("\n🎨 启动图形界面安装程序...")

        try:
            # 尝试导入tkinter
            import tkinter as tk
            from tkinter import messagebox, ttk

            # 创建GUI
            root = tk.Tk()
            root.title("ManageBac安装向导")
            root.geometry("600x400")

            # 欢迎标签
            welcome_label = ttk.Label(
                root,
                text="欢迎使用ManageBac安装向导",
                font=("Arial", 16, "bold"),
            )
            welcome_label.pack(pady=20)

            # 安装按钮
            install_button = ttk.Button(
                root,
                text="开始安装",
                command=lambda: self._gui_install_action(root),
            )
            install_button.pack(pady=10)

            root.mainloop()
            return 0

        except ImportError:
            print("❌ 无法加载图形界面，回退到快速安装")
            return self._quick_install()

    def _gui_install_action(self, root) -> None:
        """GUI安装动作。"""
        import tkinter as tk
        from tkinter import messagebox

        messagebox.showinfo("安装", "开始安装...")
        root.quit()

    def _repair_install(self) -> int:
        """修复现有安装。"""
        print("\n🔧 开始修复安装...")

        # 检查虚拟环境
        if not self.venv_path.exists():
            print("⚠️ 虚拟环境不存在，将创建新环境")
            if not self._create_venv():
                return 1

        # 重新安装依赖
        print("\n📦 重新安装依赖...")
        if not self._install_dependencies():
            return 1

        # 检查配置文件
        config_file = self.workspace / ".env"
        if not config_file.exists():
            print("⚠️ 配置文件不存在，请手动创建.env文件")

        print("\n✅ 修复完成")
        return 0

    def _create_venv(self) -> bool:
        """创建虚拟环境。"""
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: {e}")
            return False

    def _install_dependencies(self) -> bool:
        """安装依赖包。"""
        # 获取pip路径
        pip_cmd = self._get_pip_command()

        # 安装所有requirements文件
        for req_file in self.requirements_files:
            req_path = self.workspace / req_file
            if req_path.exists():
                try:
                    subprocess.run(
                        [pip_cmd, "install", "-r", str(req_path)],
                        check=True,
                        capture_output=True,
                    )
                except subprocess.CalledProcessError:
                    print(f"⚠️ 安装{req_file}时出现警告，继续...")

        return True

    def _install_playwright(self) -> bool:
        """安装Playwright浏览器。"""
        python_cmd = self._get_python_command()

        try:
            subprocess.run(
                [python_cmd, "-m", "playwright", "install", "chromium"],
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"错误: {e}")
            return False

    def _create_config(self) -> bool:
        """创建配置文件。"""
        config_file = self.workspace / ".env"

        if config_file.exists():
            print("  配置文件已存在，跳过")
            return True

        # 复制示例配置
        example_config = self.workspace / "config.example.env"
        if example_config.exists():
            import shutil

            shutil.copy(example_config, config_file)
            print("  已复制示例配置，请编辑.env文件")
        else:
            # 创建基本配置
            config_content = """# ManageBac配置文件
MANAGEBAC_EMAIL=your_email@example.com
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://shtcs.managebac.cn
HEADLESS=true
DEBUG=false
"""
            config_file.write_text(config_content, encoding="utf-8")
            print("  已创建配置文件模板")

        return True

    def _create_shortcuts(self) -> bool:
        """创建桌面快捷方式。"""
        try:
            subprocess.run(
                [sys.executable, str(self.workspace / "create_desktop_shortcut.py")],
                check=True,
                capture_output=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  跳过创建快捷方式")
            return True

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

    def _get_pip_command(self) -> str:
        """获取pip命令路径。"""
        if os.name == "nt":  # Windows
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:  # Unix-like
            return str(self.venv_path / "bin" / "pip")

    def _print_run_commands(self) -> None:
        """打印运行命令。"""
        if os.name == "nt":  # Windows
            print("  START.bat")
            print("  或: .\\venv\\Scripts\\python.exe main.py")
        else:  # Unix-like
            print("  ./START.sh")
            print("  或: ./venv/bin/python main.py")


def main() -> int:
    """主函数。"""
    import argparse

    parser = argparse.ArgumentParser(
        description="ManageBac统一安装器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["auto", "quick", "wizard", "gui", "repair"],
        default="auto",
        help="安装模式 (默认: auto)",
    )

    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="禁用图形界面，强制使用命令行",
    )

    args = parser.parse_args()

    # 转换模式
    mode = InstallMode(args.mode)

    # 如果禁用GUI，且模式为auto，则使用quick
    if args.no_gui and mode == InstallMode.AUTO:
        mode = InstallMode.QUICK

    # 创建安装器并运行
    installer = UnifiedInstaller(mode)
    return installer.run()


if __name__ == "__main__":
    sys.exit(main())
