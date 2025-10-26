#!/usr/bin/env python3
"""
Configuration Helper
配置助手

Helps users set up their .env file correctly
帮助用户正确设置.env文件
"""

import os
import sys
from pathlib import Path
import getpass


class ConfigHelper:
    """Interactive configuration helper"""

    def __init__(self):
        self.env_file = Path('.env')
        self.backup_file = Path('.env.backup')

    def display_welcome(self):
        """Display welcome message"""
        print("="*60)
        print("🎓 ManageBac Assignment Checker - Configuration Helper")
        print("🎓 ManageBac作业检查器 - 配置助手")
        print("="*60)
        print()
        print("This tool will help you set up your .env configuration file.")
        print("此工具将帮助您设置.env配置文件。")
        print()

    def check_existing_config(self):
        """Check existing configuration"""
        if self.env_file.exists():
            with open(self.env_file, 'r', encoding='utf-8') as f:
                content = f.read()

            print("📄 Current .env file found:")
            print("📄 发现当前.env文件：")
            print("-" * 40)

            for line in content.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.split('=', 1)
                    if 'PASSWORD' in key.upper():
                        print(f"{key}=***")
                    elif 'example.com' in value:
                        print(f"{key}={value} ⚠️ (example credential)")
                    else:
                        print(f"{key}={value}")

            print("-" * 40)

            if 'example.com' in content:
                print("⚠️ You are currently using example credentials!")
                print("⚠️ 您当前使用的是示例凭据！")
                print("   This is why login works but no assignments are found.")
                print("   这就是为什么登录成功但找不到作业的原因。")
                return False
            else:
                print("✅ Real credentials appear to be configured.")
                print("✅ 看起来已配置真实凭据。")
                return True
        else:
            print("❌ No .env file found.")
            print("❌ 未找到.env文件。")
            return False

    def backup_existing_config(self):
        """Backup existing configuration"""
        if self.env_file.exists():
            try:
                import shutil
                shutil.copy2(self.env_file, self.backup_file)
                print(f"✅ Backed up existing .env to {self.backup_file}")
                print(f"✅ 已将现有.env备份到{self.backup_file}")
            except Exception as e:
                print(f"⚠️ Could not backup .env file: {e}")

    def get_user_input(self):
        """Get user input for configuration"""
        print("\n🔐 Please provide your ManageBac credentials:")
        print("🔐 请提供您的ManageBac凭据：")
        print()

        # Get ManageBac URL
        print("1️⃣ ManageBac URL (e.g., https://yourschool.managebac.cn)")
        print("   ManageBac网址 (例如：https://yourschool.managebac.cn)")
        url = input("   URL: ").strip()

        if not url:
            url = "https://shtcs.managebac.cn"
            print(f"   Using default: {url}")

        if not url.startswith('http'):
            url = 'https://' + url

        # Get email
        print("\n2️⃣ Your ManageBac email")
        print("   您的ManageBac邮箱")
        email = input("   Email: ").strip()

        while not email or '@' not in email:
            print("   ⚠️ Please enter a valid email address")
            print("   ⚠️ 请输入有效的邮箱地址")
            email = input("   Email: ").strip()

        # Get password (hidden input)
        print("\n3️⃣ Your ManageBac password (input will be hidden)")
        print("   您的ManageBac密码 (输入将被隐藏)")
        password = getpass.getpass("   Password: ")

        while not password:
            print("   ⚠️ Password cannot be empty")
            print("   ⚠️ 密码不能为空")
            password = getpass.getpass("   Password: ")

        # Optional settings
        print("\n4️⃣ Optional settings (press Enter for defaults)")
        print("   可选设置 (按回车使用默认值)")

        print("\n   Report format [html,console]: ", end="")
        report_format = input().strip() or "html,console"

        print("   Output directory [reports]: ", end="")
        output_dir = input().strip() or "reports"

        print("   Language [zh/en]: ", end="")
        language = input().strip() or "zh"

        print("   Headless mode [true/false]: ", end="")
        headless = input().strip() or "true"

        return {
            'MANAGEBAC_URL': url,
            'MANAGEBAC_EMAIL': email,
            'MANAGEBAC_PASSWORD': password,
            'REPORT_FORMAT': report_format,
            'OUTPUT_DIR': output_dir,
            'LANGUAGE': language,
            'HEADLESS': headless,
            'DEBUG': 'false'
        }

    def create_env_file(self, config):
        """Create .env file with user configuration"""
        env_content = f"""# ManageBac Assignment Checker Configuration
# ManageBac作业检查器配置

# === Required Settings 必需设置 ===
MANAGEBAC_URL={config['MANAGEBAC_URL']}
MANAGEBAC_EMAIL={config['MANAGEBAC_EMAIL']}
MANAGEBAC_PASSWORD={config['MANAGEBAC_PASSWORD']}

# === Optional Settings 可选设置 ===
REPORT_FORMAT={config['REPORT_FORMAT']}
OUTPUT_DIR={config['OUTPUT_DIR']}
LANGUAGE={config['LANGUAGE']}
HEADLESS={config['HEADLESS']}
DEBUG={config['DEBUG']}

# === AI Features (Optional) AI功能 (可选) ===
# AI_ENABLED=false
# OPENAI_API_KEY=your_openai_api_key_here
# AI_MODEL=gpt-3.5-turbo

# === Email Notifications (Optional) 邮件通知 (可选) ===
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# EMAIL_USER=your_email@gmail.com
# EMAIL_PASSWORD=your_app_password
# NOTIFICATION_EMAIL=notify@example.com
"""

        try:
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)

            print(f"\n✅ Created .env file successfully!")
            print(f"✅ 成功创建.env文件！")
            return True

        except Exception as e:
            print(f"\n❌ Failed to create .env file: {e}")
            print(f"❌ 创建.env文件失败：{e}")
            return False

    def test_configuration(self):
        """Test the configuration"""
        print("\n🧪 Testing configuration...")
        print("🧪 测试配置...")

        try:
            # Test config loading
            from managebac_checker.config import Config
            config = Config.from_environment()

            print("✅ Configuration loaded successfully")
            print("✅ 配置加载成功")

            print(f"   📧 Email: {config.email[:15]}...")
            print(f"   🌐 URL: {config.url}")
            print(f"   📁 Output: {config.output_dir}")

            return True

        except Exception as e:
            print(f"❌ Configuration test failed: {e}")
            print(f"❌ 配置测试失败：{e}")
            return False

    def show_next_steps(self):
        """Show next steps"""
        print("\n" + "="*60)
        print("🎉 Configuration Complete!")
        print("🎉 配置完成！")
        print("="*60)

        print("\n📋 Next steps:")
        print("📋 下一步：")
        print()
        print("1. Test assignment detection:")
        print("   测试作业检测：")
        print("   python3 fixed_assignment_test.py")
        print()
        print("2. Launch the application:")
        print("   启动应用程序：")
        print("   python3 intelligent_launcher.py")
        print()
        print("3. Or use the GUI:")
        print("   或使用GUI：")
        print("   python3 non_hanging_gui.py")
        print()
        print("🔧 If you encounter issues:")
        print("🔧 如果遇到问题：")
        print("   - Check your credentials are correct")
        print("   - 检查您的凭据是否正确")
        print("   - Try: python3 comprehensive_diagnostic.py")
        print("   - 尝试：python3 comprehensive_diagnostic.py")

    def run(self):
        """Run the configuration helper"""
        self.display_welcome()

        # Check existing config
        has_valid_config = self.check_existing_config()

        if has_valid_config:
            print("\n✅ Your configuration appears to be correct!")
            print("✅ 您的配置看起来是正确的！")
            print("\nIf you're still having issues, try:")
            print("如果仍有问题，请尝试：")
            print("  python3 fixed_assignment_test.py")
            return True

        # Ask if user wants to reconfigure
        print("\n🔧 Would you like to update your configuration? (y/n)")
        print("🔧 您想要更新配置吗？(y/n)")

        response = input(">>> ").strip().lower()

        if response not in ['y', 'yes', 'Y', 'YES', '是', 'y']:
            print("Configuration unchanged.")
            print("配置未更改。")
            return False

        # Backup existing config
        self.backup_existing_config()

        # Get user input
        config = self.get_user_input()

        # Create .env file
        if not self.create_env_file(config):
            return False

        # Test configuration
        if not self.test_configuration():
            print("\n⚠️ Configuration test failed, but file was created.")
            print("⚠️ 配置测试失败，但文件已创建。")
            print("You may need to check your credentials.")
            print("您可能需要检查您的凭据。")

        # Show next steps
        self.show_next_steps()

        return True


def main():
    """Main function"""
    try:
        helper = ConfigHelper()
        success = helper.run()
        return success
    except KeyboardInterrupt:
        print("\n\n🛑 Configuration cancelled by user")
        print("🛑 用户取消配置")
        return False
    except Exception as e:
        print(f"\n❌ Configuration helper failed: {e}")
        print(f"❌ 配置助手失败：{e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)