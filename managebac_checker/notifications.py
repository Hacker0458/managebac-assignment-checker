"""
邮件通知功能模块
"""

import smtplib
from datetime import datetime
from typing import List, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationManager:
    """处理邮件通知功能"""
    
    def __init__(self, config):
        """初始化通知管理器"""
        self.config = config
    
    async def send_email_notification(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> bool:
        """发送邮件通知"""
        if not self.config.is_notification_enabled():
            return False
        
        try:
            # 创建邮件内容
            subject = f"📚 ManageBac作业提醒 - {analysis['total_assignments']}个待办作业"
            
            # 生成简单的HTML邮件内容
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #2c3e50;">📚 ManageBac作业提醒</h2>
                    <p>您好！以下是您的作业总结：</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>📈 概览统计</h3>
                        <ul>
                            <li><strong>待办作业</strong>: {analysis['total_assignments']} 个</li>
                            <li><strong>紧急作业</strong>: {analysis['urgent_count']} 个</li>
                            <li><strong>涉及课程</strong>: {len(analysis['by_course'])} 个</li>
                        </ul>
                    </div>
            """
            
            if analysis['urgent_count'] > 0:
                html_content += """
                    <div style="background-color: #e74c3c; color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>😨 紧急作业</h3>
                        <ul>
                """
                
                for assignment in analysis['assignments_by_urgency']['urgent'][:5]:  # 只显示前5个
                    html_content += f"<li><strong>{assignment['title'][:50]}...</strong> - {assignment['due_date']}</li>"
                
                html_content += "</ul></div>"
            
            html_content += f"""
                    <p style="margin-top: 20px; font-size: 14px; color: #7f8c8d;">
                        请及时登录ManageBac查看详情并完成作业。
                    </p>
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #95a5a6;">
                        此邮件由 ManageBac Assignment Checker 自动发送<br>
                        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </body>
            </html>
            """
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config.email_user
            msg['To'] = self.config.notification_email
            
            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 发送邮件
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.email_user, self.config.email_password)
                server.sendmail(self.config.email_user, self.config.notification_email, msg.as_string())
            
            print(f"\n📧 邮件通知已发送到: {self.config.notification_email}")
            return True
            
        except Exception as e:
            print(f"\n⚠️  发送邮件通知失败: {e}")
            return False