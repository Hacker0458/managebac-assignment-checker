"""Report generation utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from .analysis import analyse_assignments
from .models import Assignment


class ReportBuilder:
    """Builds reports in various formats (console/html/markdown/json)."""

    def __init__(self, *, output_dir: Path, report_formats: List[str]) -> None:
        self.output_dir = output_dir
        self.report_formats = [fmt.strip().lower() for fmt in report_formats if fmt.strip()]

    def build(self, assignments: List[Assignment], analysis: Dict[str, object]) -> Dict[str, str]:
        generated_at = datetime.now(timezone.utc).isoformat()
        report_payload = {
            "assignments": [item.to_dict() for item in assignments],
            "analysis": _serialise_analysis(analysis),
            "generated_at": generated_at,
        }

        reports: Dict[str, str] = {}
        for fmt in self.report_formats:
            if fmt == "json":
                reports["json"] = self._render_json(report_payload)
            elif fmt == "markdown":
                reports["markdown"] = self._render_markdown(assignments, analysis, generated_at)
            elif fmt == "html":
                reports["html"] = self._render_html(assignments, analysis, generated_at)
            elif fmt == "console":
                reports["console"] = self._render_console(assignments, analysis, generated_at)
        return reports

    def persist(self, reports: Dict[str, str]) -> Dict[str, str]:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        saved: Dict[str, str] = {}

        extension_map = {"json": "json", "html": "html", "markdown": "md"}
        self.output_dir.mkdir(parents=True, exist_ok=True)

        for fmt, content in reports.items():
            if fmt == "console":
                continue
            extension = extension_map.get(fmt, fmt)
            filename = self.output_dir / f"managebac_report_{timestamp}.{extension}"
            filename.write_text(content, encoding="utf-8")
            saved[fmt] = str(filename)
        return saved

    def _render_json(self, payload: Dict[str, object]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def _render_console(
        self,
        assignments: List[Assignment],
        analysis: Dict[str, object],
        generated_at: str,
    ) -> str:
        lines: List[str] = []
        lines.append("=" * 80)
        lines.append(f"ManageBac 作业检查报告 - {generated_at}")
        lines.append("=" * 80)
        lines.append(
            f"总任务: {analysis['total_assignments']} | 紧急: {analysis['urgent_count']} | 逾期: {analysis['overdue_count']}"
        )
        lines.append("\n未提交任务:")
        for item in analysis["grouped_by_status"]["pending"][:10]:
            lines.append(f" - {item.title} (due: {item.due_date}, course: {item.course})")
        if not analysis["grouped_by_status"]["pending"]:
            lines.append(" - 无")
        lines.append("\n逾期任务:")
        for item in analysis["grouped_by_status"]["overdue"][:10]:
            lines.append(f" - {item.title} (due: {item.due_date})")
        if not analysis["grouped_by_status"]["overdue"]:
            lines.append(" - 无")
        return "\n".join(lines)

    def _render_markdown(
        self,
        assignments: List[Assignment],
        analysis: Dict[str, object],
        generated_at: str,
    ) -> str:
        lines: List[str] = []
        lines.append("# 📚 ManageBac 作业检查报告")
        lines.append("")
        lines.append(f"生成时间: {generated_at}")
        lines.append("")
        lines.append("## 概览")
        lines.append(f"- 总任务: {analysis['total_assignments']}")
        lines.append(f"- 紧急任务: {analysis['urgent_count']}")
        lines.append(
            f"- 未提交: {analysis['pending_count']} | 已提交: {analysis['submitted_count']} | 逾期: {analysis['overdue_count']}"
        )
        lines.append("")
        lines.append("## 未提交任务")
        if analysis["grouped_by_status"]["pending"]:
            for item in analysis["grouped_by_status"]["pending"]:
                lines.append(f"- {item.title} — 截止: {item.due_date} （课程: {item.course}）")
        else:
            lines.append("- 无")

        lines.append("")
        lines.append("## 逾期任务")
        if analysis["grouped_by_status"]["overdue"]:
            for item in analysis["grouped_by_status"]["overdue"]:
                lines.append(f"- {item.title} — 截止: {item.due_date}")
        else:
            lines.append("- 无")

        lines.append("")
        lines.append("## 所有任务")
        for idx, assignment in enumerate(assignments, start=1):
            lines.append(f"### {idx}. {assignment.title}")
            lines.append(f"- 课程: {assignment.course}")
            lines.append(f"- 截止: {assignment.due_date}")
            lines.append(f"- 状态: {assignment.status}")
            lines.append(f"- 优先级: {assignment.priority}")
            if assignment.link:
                lines.append(f"- 链接: {assignment.link}")
            lines.append("")

        lines.append("---")
        lines.append("由 ManageBac Assignment Checker 自动生成")
        return "\n".join(lines)

    def _render_html(
        self,
        assignments: List[Assignment],
        analysis: Dict[str, object],
        generated_at: str,
    ) -> str:
        # Keep HTML inline for portability; it's intentionally simple to avoid extra deps.
        def _rows(items: List[Assignment]) -> str:
            cells = []
            for assignment in items:
                link_html = (
                    f'<a href="{assignment.link}">{assignment.title}</a>'
                    if assignment.link
                    else assignment.title
                )
                cells.append(
                    f"<tr><td>{link_html}</td><td>{assignment.course}</td><td>{assignment.due_date}</td><td>{assignment.status}</td><td>{assignment.priority}</td></tr>"
                )
            return "".join(cells)

        return f"""<!DOCTYPE html>
<html lang=\"zh\">
<head>
<meta charset=\"utf-8\" />
<title>ManageBac 作业检查报告</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 24px; background: #f9fafb; color: #111827; }}
.container {{ max-width: 980px; margin: 0 auto; background: white; padding: 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1); }}
h1 {{ margin-top: 0; }}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
th {{ background: #2563eb; color: white; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; background: #eff6ff; color: #1d4ed8; margin-right: 8px; }}
section {{ margin-top: 28px; }}
</style>
</head>
<body>
<div class=\"container\">
<h1>📚 ManageBac 作业检查报告</h1>
<p>生成时间: {generated_at}</p>
<section>
<h2>概要</h2>
<p class=\"badge\">总任务: {analysis['total_assignments']}</p>
<p class=\"badge\">紧急: {analysis['urgent_count']}</p>
<p class=\"badge\">未提交: {analysis['pending_count']}</p>
<p class=\"badge\">逾期: {analysis['overdue_count']}</p>
</section>
<section>
<h2>未提交任务</h2>
<table>
<thead><tr><th>作业</th><th>课程</th><th>截止</th><th>状态</th><th>优先级</th></tr></thead>
<tbody>{_rows(analysis['grouped_by_status']['pending']) or '<tr><td colspan="5">无</td></tr>'}</tbody>
</table>
</section>
<section>
<h2>逾期任务</h2>
<table>
<thead><tr><th>作业</th><th>课程</th><th>截止</th><th>状态</th><th>优先级</th></tr></thead>
<tbody>{_rows(analysis['grouped_by_status']['overdue']) or '<tr><td colspan="5">无</td></tr>'}</tbody>
</table>
</section>
<section>
<h2>所有任务</h2>
<table>
<thead><tr><th>作业</th><th>课程</th><th>截止</th><th>状态</th><th>优先级</th></tr></thead>
<tbody>{_rows(assignments)}</tbody>
</table>
</section>
<footer><small>报告由 ManageBac Assignment Checker 自动生成。</small></footer>
</div>
</body>
</html>"""


def _serialise_analysis(analysis: Dict[str, object]) -> Dict[str, object]:
    serialised: Dict[str, object] = {}
    for key, value in analysis.items():
        if key in {"grouped_by_status", "assignments_by_urgency"}:
            serialised[key] = {
                inner_key: [assignment.to_dict() for assignment in assignments]
                for inner_key, assignments in value.items()
            }
        elif isinstance(value, dict):
            serialised[key] = value
        else:
            serialised[key] = value
    return serialised
