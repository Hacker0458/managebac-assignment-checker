"""
🎓 ManageBac Assignment Checker Reporter | ManageBac作业检查器报告生成器
========================================================================

Report generation functionality for ManageBac Assignment Checker.
ManageBac作业检查器的报告生成功能模块。
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from .logging_utils import BilingualLogger


class ReportGenerator:
    """
    Handles various format report generation.
    处理各种格式的报告生成。
    """

    def __init__(self, config, logger: Optional[BilingualLogger] = None):
        """
        Initialize report generator.
        初始化报告生成器。

        Args:
            config: Configuration instance
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.output_dir = config.output_dir
        self.language = config.language

        # Bilingual text templates | 双语文本模板
        self.texts = self._get_bilingual_texts()

    def _get_bilingual_texts(self) -> Dict[str, Dict[str, str]]:
        """Get bilingual text templates."""
        return {
            "title": {
                "en": "ManageBac Assignment Report",
                "zh": "ManageBac作业检查报告",
            },
            "header_title": {
                "en": "📚 ManageBac Assignment Report",
                "zh": "📚 ManageBac作业检查报告",
            },
            "header_subtitle": {
                "en": f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "zh": f"生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            },
            "total_label": {"en": "Total Assignments", "zh": "总作业数"},
            "urgent_label": {"en": "Urgent Assignments", "zh": "紧急作业"},
            "courses_label": {"en": "Courses Involved", "zh": "涉及课程"},
            "high_priority_label": {"en": "High Priority", "zh": "高优先级"},
            "charts_title": {"en": "Data Analysis", "zh": "数据分析"},
            "priority_chart_title": {"en": "Priority Distribution", "zh": "优先级分布"},
            "course_chart_title": {"en": "Course Distribution", "zh": "课程分布"},
            "urgency_chart_title": {"en": "Urgency Distribution", "zh": "紧急程度分布"},
            "urgent_section_title": {
                "en": "Urgent Assignments - Immediate Attention Required",
                "zh": "紧急作业 - 需要立即关注",
            },
            "all_assignments_title": {
                "en": "All Assignment Details",
                "zh": "所有作业详情",
            },
            "course_summary_title": {"en": "Course Summary", "zh": "课程汇总"},
            "assignments_text": {"en": "assignments", "zh": "个作业"},
            "documentation_text": {"en": "Documentation", "zh": "文档"},
            "report_issue_text": {"en": "Report Issue", "zh": "报告问题"},
            "footer_text": {
                "en": "🚀 ManageBac Assignment Checker - Making assignment management easier!",
                "zh": "🚀 ManageBac作业检查器 - 让作业管理更简单！",
            },
            "generated_text": {"en": "Generated at", "zh": "生成时间："},
            "priority_high": {"en": "High", "zh": "高"},
            "priority_medium": {"en": "Medium", "zh": "中"},
            "priority_low": {"en": "Low", "zh": "低"},
            "urgency_urgent": {"en": "Urgent", "zh": "紧急"},
            "urgency_soon": {"en": "Soon", "zh": "即将到期"},
            "urgency_later": {"en": "Later", "zh": "稍后"},
        }

    def get_text(self, key: str) -> str:
        """Get localized text."""
        return self.texts.get(key, {}).get(
            self.language, self.texts.get(key, {}).get("en", key)
        )

    def generate_reports(
        self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate reports in multiple formats.
        生成多种格式的报告。
        """
        report_data = {
            "assignments": assignments,
            "analysis": analysis,
            "generated_at": datetime.now().isoformat(),
            "student_email": self.config.email,
            "language": self.language,
            "config": {
                "url": self.config.url,
                "total_assignments": analysis.get("total_assignments", 0),
                "urgent_count": analysis.get("urgent_count", 0),
                "courses_count": len(analysis.get("by_course", {})),
                "high_priority_count": analysis.get("by_priority", {}).get("high", 0),
            },
        }

        reports = {}

        for format_type in self.config.get_report_formats():
            if format_type == "json":
                reports["json"] = self._generate_json_report(report_data)
            elif format_type == "html":
                reports["html"] = self._generate_html_report(report_data)
            elif format_type == "markdown":
                reports["markdown"] = self._generate_markdown_report(report_data)
            elif format_type == "console":
                reports["console"] = self._generate_console_report(report_data)

        return reports

    def _generate_json_report(self, data: Dict[str, Any]) -> str:
        """Generate JSON format report."""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            error_msg = (
                f"生成JSON报告失败: {e}"
                if self.language == "zh"
                else f"Failed to generate JSON report: {e}"
            )
            return json.dumps({"error": error_msg})

    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """Generate HTML format report using template."""
        try:
            # Prepare template data
            template_data = self._prepare_html_template_data(data)

            # Try to use Jinja2 template if available
            try:
                from jinja2 import Environment, FileSystemLoader

                template_dir = Path(__file__).parent / "templates"
                env = Environment(loader=FileSystemLoader(template_dir))
                template = env.get_template("report.html")

                return template.render(**template_data)

            except ImportError:
                # Fallback to simple string replacement
                return self._generate_simple_html_report(template_data)

        except Exception as e:
            error_msg = (
                f"生成HTML报告失败: {e}"
                if self.language == "zh"
                else f"Failed to generate HTML report: {e}"
            )
            if self.logger:
                self.logger.error_occurred(error_msg)
            return self._generate_fallback_html(data, error_msg)

    def _prepare_html_template_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for HTML template."""
        analysis = data["analysis"]
        assignments = data["assignments"]

        # Process assignments for display
        processed_assignments = []
        for assignment in assignments:
            processed_assignment = assignment.copy()
            processed_assignment["priority_text"] = self.get_text(
                f"priority_{assignment.get('priority', 'low')}"
            )
            processed_assignment["urgency_text"] = self.get_text(
                f"urgency_{assignment.get('urgency', 'later')}"
            )
            processed_assignments.append(processed_assignment)

        # Get urgent assignments
        urgent_assignments = [
            a for a in processed_assignments if a.get("urgency") == "urgent"
        ][
            :10
        ]  # Limit to top 10

        # Course summary
        course_summary = list(analysis.get("by_course", {}).items())
        course_summary.sort(key=lambda x: x[1], reverse=True)

        return {
            "language": self.language,
            "theme": getattr(self.config, "html_theme", "auto"),
            "title": self.get_text("title"),
            "header_title": self.get_text("header_title"),
            "header_subtitle": self.get_text("header_subtitle"),
            "total_assignments": analysis.get("total_assignments", 0),
            "urgent_count": analysis.get("urgent_count", 0),
            "courses_count": len(analysis.get("by_course", {})),
            "high_priority_count": analysis.get("by_priority", {}).get("high", 0),
            "total_label": self.get_text("total_label"),
            "urgent_label": self.get_text("urgent_label"),
            "courses_label": self.get_text("courses_label"),
            "high_priority_label": self.get_text("high_priority_label"),
            "include_charts": getattr(self.config, "include_charts", True),
            "charts_title": self.get_text("charts_title"),
            "priority_chart_title": self.get_text("priority_chart_title"),
            "course_chart_title": self.get_text("course_chart_title"),
            "urgency_chart_title": self.get_text("urgency_chart_title"),
            "urgent_section_title": self.get_text("urgent_section_title"),
            "all_assignments_title": self.get_text("all_assignments_title"),
            "course_summary_title": self.get_text("course_summary_title"),
            "assignments": processed_assignments,
            "urgent_assignments": urgent_assignments,
            "course_summary": course_summary,
            "assignments_text": self.get_text("assignments_text"),
            "documentation_text": self.get_text("documentation_text"),
            "report_issue_text": self.get_text("report_issue_text"),
            "footer_text": self.get_text("footer_text"),
            "generated_text": self.get_text("generated_text"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Chart data
            "priority_labels": json.dumps(
                [
                    self.get_text("priority_high"),
                    self.get_text("priority_medium"),
                    self.get_text("priority_low"),
                ]
            ),
            "priority_data": json.dumps(
                [
                    analysis.get("by_priority", {}).get("high", 0),
                    analysis.get("by_priority", {}).get("medium", 0),
                    analysis.get("by_priority", {}).get("low", 0),
                ]
            ),
            "course_labels": json.dumps(list(analysis.get("by_course", {}).keys())),
            "course_data": json.dumps(list(analysis.get("by_course", {}).values())),
            "urgency_labels": json.dumps(
                [
                    self.get_text("urgency_urgent"),
                    self.get_text("urgency_soon"),
                    self.get_text("urgency_later"),
                ]
            ),
            "urgency_data": json.dumps(
                [
                    len([a for a in assignments if a.get("urgency") == "urgent"]),
                    len([a for a in assignments if a.get("urgency") == "soon"]),
                    len([a for a in assignments if a.get("urgency") == "later"]),
                ]
            ),
        }

    def _generate_simple_html_report(self, template_data: Dict[str, Any]) -> str:
        """Generate HTML report without Jinja2."""
        # Read template file
        template_path = Path(__file__).parent / "templates" / "report.html"

        if not template_path.exists():
            return self._generate_fallback_html(
                template_data, "Template file not found"
            )

        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Simple template variable replacement
        for key, value in template_data.items():
            placeholder = f"{{{{ {key} }}}}"
            template_content = template_content.replace(placeholder, str(value))

        # Remove Jinja2 specific syntax that wasn't replaced
        import re

        template_content = re.sub(r"{%.*?%}", "", template_content, flags=re.DOTALL)
        template_content = re.sub(r"{{.*?}}", "", template_content)

        return template_content

    def _generate_fallback_html(self, data: Any, error: str = "") -> str:
        """Generate a simple fallback HTML report."""
        assignments = data.get("assignments", []) if isinstance(data, dict) else []
        analysis = data.get("analysis", {}) if isinstance(data, dict) else {}

        html = f"""
        <!DOCTYPE html>
        <html lang="{self.language}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.get_text("title")}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; line-height: 1.6; }}
                .header {{ background: #3b82f6; color: white; padding: 2rem; border-radius: 8px; text-align: center; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }}
                .stat {{ background: #f8fafc; padding: 1rem; border-radius: 8px; text-align: center; }}
                .assignment {{ border: 1px solid #e2e8f0; padding: 1rem; margin: 1rem 0; border-radius: 8px; }}
                .urgent {{ border-left: 4px solid #ef4444; }}
                .error {{ background: #fee2e2; color: #991b1b; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{self.get_text("header_title")}</h1>
                <p>{self.get_text("header_subtitle")}</p>
            </div>
        """

        if error:
            html += f'<div class="error">⚠️ {error}</div>'

        # Statistics
        html += f"""
            <div class="stats">
                <div class="stat">
                    <h3>{analysis.get("total_assignments", 0)}</h3>
                    <p>{self.get_text("total_label")}</p>
                </div>
                <div class="stat">
                    <h3>{analysis.get("urgent_count", 0)}</h3>
                    <p>{self.get_text("urgent_label")}</p>
                </div>
                <div class="stat">
                    <h3>{len(analysis.get("by_course", {}))}</h3>
                    <p>{self.get_text("courses_label")}</p>
                </div>
            </div>
        """

        # Assignments
        html += f'<h2>{self.get_text("all_assignments_title")}</h2>'

        for assignment in assignments:
            urgency_class = "urgent" if assignment.get("urgency") == "urgent" else ""
            html += f"""
                <div class="assignment {urgency_class}">
                    <h3>{assignment.get("title", "")}</h3>
                    <p>⏰ {assignment.get("due_date", "")}</p>
                    <p>📚 {assignment.get("course", "")}</p>
                    <p>📊 {assignment.get("status", "")}</p>
                </div>
            """

        html += f"""
            <footer style="text-align: center; margin-top: 2rem; color: #666;">
                <p>{self.get_text("footer_text")}</p>
                <p><small>{self.get_text("generated_text")} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
            </footer>
        </body>
        </html>
        """

        return html

    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """Generate Markdown format report."""
        analysis = data["analysis"]
        assignments = data["assignments"]

        if self.language == "zh":
            md = f"""# 📚 ManageBac作业检查报告

**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}  
**学生邮箱**: {data["student_email"]}  
**ManageBac网址**: {self.config.url}

## 📈 概览统计

| 指标 | 数量 |
|------|------|
| 📋 总作业数 | {analysis.get("total_assignments", 0)} |
| 😨 紧急作业 | {analysis.get("urgent_count", 0)} |
| 📚 涉及课程 | {len(analysis.get("by_course", {}))} |
| 🔴 高优先级 | {analysis.get("by_priority", {}).get("high", 0)} |
| 🟡 中优先级 | {analysis.get("by_priority", {}).get("medium", 0)} |
| 🟢 低优先级 | {analysis.get("by_priority", {}).get("low", 0)} |

"""
        else:
            md = f"""# 📚 ManageBac Assignment Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Student Email**: {data["student_email"]}  
**ManageBac URL**: {self.config.url}

## 📈 Overview Statistics

| Metric | Count |
|--------|-------|
| 📋 Total Assignments | {analysis.get("total_assignments", 0)} |
| 😨 Urgent Assignments | {analysis.get("urgent_count", 0)} |
| 📚 Courses Involved | {len(analysis.get("by_course", {}))} |
| 🔴 High Priority | {analysis.get("by_priority", {}).get("high", 0)} |
| 🟡 Medium Priority | {analysis.get("by_priority", {}).get("medium", 0)} |
| 🟢 Low Priority | {analysis.get("by_priority", {}).get("low", 0)} |

"""

        # Urgent assignments
        urgent_assignments = [a for a in assignments if a.get("urgency") == "urgent"]
        if urgent_assignments:
            section_title = (
                "## 🔥 紧急作业"
                if self.language == "zh"
                else "## 🔥 Urgent Assignments"
            )
            md += f"{section_title}\n\n"

            for i, assignment in enumerate(urgent_assignments[:10], 1):
                md += f"{i}. **{assignment['title']}**\n"
                md += f"   - ⏰ {assignment['due_date']}\n"
                md += f"   - 📚 {assignment['course']}\n"
                md += f"   - 📊 {assignment['status']}\n\n"

        # All assignments
        section_title = (
            "## 📋 所有作业详情"
            if self.language == "zh"
            else "## 📋 All Assignment Details"
        )
        md += f"{section_title}\n\n"

        for i, assignment in enumerate(assignments, 1):
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                assignment.get("priority", "low"), "🟢"
            )
            urgency_emoji = {"urgent": "🔥", "soon": "⚠️", "later": "🟢"}.get(
                assignment.get("urgency", "later"), "🟢"
            )

            md += f"{i}. {urgency_emoji} **{assignment['title']}**\n"
            md += f"   - ⏰ {assignment['due_date']}\n"
            md += f"   - 📚 {assignment['course']}\n"
            md += f"   - 📊 {assignment['status']}\n"
            md += (
                f"   - {priority_emoji} {assignment.get('priority', 'low').upper()}\n\n"
            )

        # Course summary
        if analysis.get("by_course"):
            section_title = (
                "## 📚 课程分布"
                if self.language == "zh"
                else "## 📚 Course Distribution"
            )
            md += f"{section_title}\n\n"

            for course, count in sorted(
                analysis["by_course"].items(), key=lambda x: x[1], reverse=True
            ):
                count_text = (
                    f"{count} 个作业"
                    if self.language == "zh"
                    else f"{count} assignments"
                )
                md += f"- **{course}**: {count_text}\n"

        footer_text = (
            "🚀 ManageBac作业检查器 - 让作业管理更简单！"
            if self.language == "zh"
            else "🚀 ManageBac Assignment Checker - Making assignment management easier!"
        )
        md += f"\n---\n\n*{footer_text}*\n"

        return md

    def _generate_console_report(self, data: Dict[str, Any]) -> str:
        """Generate console format report."""
        # This is handled by the checker class directly
        return "Console report generated in real-time"

    def save_reports(self, reports: Dict[str, str]) -> Dict[str, str]:
        """
        Save generated reports to files.
        保存生成的报告到文件。
        """
        saved_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for format_type, content in reports.items():
            if format_type == "console":
                continue  # Skip console format for file saving

            filename = f"managebac_report_{timestamp}.{format_type}"
            filepath = self.output_dir / filename

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                saved_files[format_type] = str(filepath)

                if self.logger:
                    self.logger.report_saved(str(filepath))

            except Exception as e:
                error_msg = (
                    f"保存{format_type}报告失败: {e}"
                    if self.language == "zh"
                    else f"Failed to save {format_type} report: {e}"
                )
                if self.logger:
                    self.logger.error_occurred(error_msg)

        return saved_files
