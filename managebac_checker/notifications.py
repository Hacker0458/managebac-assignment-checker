"""邮件通知工具，兼容旧接口。"""

from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable, Optional

from .models import Assignment
from .logging_utils import BilingualLogger


def send_email_notification(
    *,
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    recipient: str,
    subject: str,
    urgent_assignments: Iterable[Assignment],
    total_count: int,
) -> None:
    assignments = list(urgent_assignments)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = recipient

    body_lines = ["<h3>紧急作业提醒</h3>"]
    if assignments:
        body_lines.append("<ul>")
        for item in assignments:
            body_lines.append(f"<li>{item.title} — 截止 {item.due_date}</li>")
        body_lines.append("</ul>")
    else:
        body_lines.append("<p>当前无紧急作业。</p>")

    body_lines.append(f"<p>共 {total_count} 个待办作业。</p>")
    html_part = MIMEText("\n".join(body_lines), "html", "utf-8")
    msg.attach(html_part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, recipient, msg.as_string())


class NotificationManager:
    """旧接口兼容的通知管理器。"""

    def __init__(self, config, logger: Optional[BilingualLogger] = None) -> None:
        self.config = config
        self.logger = logger

    async def send_email_notification(self, assignments, analysis) -> bool:
        if not getattr(self.config, "enable_notifications", False):
            return False

        urgent = analysis.get("assignments_by_urgency", {}).get("urgent", [])
        if not urgent:
            return False

        assignment_objs = [
            (
                assignment
                if isinstance(assignment, Assignment)
                else Assignment(
                    identifier=getattr(assignment, "identifier", "legacy"),
                    title=getattr(assignment, "title", "未命名作业"),
                    course=getattr(assignment, "course", "未知课程"),
                    status=getattr(assignment, "status", "Unknown"),
                    due_date=getattr(assignment, "due_date", "无截止日期"),
                    assignment_type=getattr(
                        assignment, "assignment_type", getattr(assignment, "type", "Unknown")
                    ),
                    priority=getattr(assignment, "priority", "low"),
                    submitted=getattr(assignment, "submitted", False),
                    overdue=getattr(assignment, "overdue", False),
                    link=getattr(assignment, "link", None),
                    description=getattr(assignment, "description", None),
                    raw_text=getattr(assignment, "raw_text", None),
                )
            )
            for assignment in urgent
        ]

        try:
            send_email_notification(
                smtp_server=self.config.smtp_server,
                smtp_port=self.config.smtp_port,
                username=self.config.email_user,
                password=self.config.email_password,
                recipient=self.config.notification_email,
                subject=f"ManageBac 作业提醒 - {len(assignment_objs)} 个紧急任务",
                urgent_assignments=assignment_objs,
                total_count=analysis.get("total_assignments", len(assignments)),
            )
            if self.logger:
                self.logger.notification_sent(self.config.notification_email)
            return True
        except Exception as exc:  # pragma: no cover - 网络异常
            if self.logger:
                self.logger.error(f"发送邮件失败: {exc}")
            return False
