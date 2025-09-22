"""
报告生成功能模块
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class ReportGenerator:
    """处理各种格式的报告生成"""
    
    def __init__(self, config):
        """初始化报告生成器"""
        self.config = config
        self.output_dir = config.output_dir
    
    def generate_reports(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> Dict[str, str]:
        """生成多种格式的报告"""
        report_data = {
            'assignments': assignments,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat(),
            'student_email': self.config.email
        }
        
        reports = {}
        
        for format_type in self.config.get_report_formats():
            if format_type == 'json':
                reports['json'] = self._generate_json_report(report_data)
            elif format_type == 'html':
                reports['html'] = self._generate_html_report(report_data)
            elif format_type == 'markdown':
                reports['markdown'] = self._generate_markdown_report(report_data)
            elif format_type == 'console':
                reports['console'] = self._generate_console_report(report_data)
        
        return reports
    
    def _generate_json_report(self, data: Dict[str, Any]) -> str:
        """生成JSON格式报告"""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            return f"{{\"error\": \"生成JSON报告失败: {e}\"}}"
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """生成HTML格式报告"""
        assignments = data['assignments']
        analysis = data['analysis']
        generated_at = data['generated_at']
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="light" />
    <title>ManageBac作业检查报告</title>
    <style>
        :root {{ color-scheme: light; }}
        html, body {{ background:#f7fafc; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 24px; color:#111827; }}
        a {{ color:#1d4ed8; text-decoration:none; }}
        a:hover {{ text-decoration:underline; }}
        .container {{ max-width: 1100px; margin: 0 auto; background-color: #ffffff; padding: 28px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border:1px solid #e5e7eb; }}
        h1 {{ color: #111827; border-bottom: 4px solid #2563eb; padding-bottom: 10px; margin-top:0; }}
        h2 {{ color: #111827; margin-top: 28px; }}
        h3 {{ color:#111827; }}
        .summary {{ background-color: #f3f4f6; padding: 18px; border-radius: 10px; margin: 18px 0; border:1px solid #e5e7eb; }}
        .urgent {{ background-color: #ef4444; color: #ffffff; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .soon {{ background-color: #f59e0b; color: #111827; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .later {{ background-color: #10b981; color: #ffffff; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .assignment {{ border-left: 6px solid #2563eb; padding: 14px; margin: 10px 0; background-color: #ffffff; border:1px solid #e5e7eb; border-radius:8px; color:#111827; }}
        .high-priority {{ border-left-color: #ef4444; }}
        .medium-priority {{ border-left-color: #f59e0b; }}
        .low-priority {{ border-left-color: #10b981; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 18px 0; }}
        .stat-item {{ text-align: center; padding: 16px; background-color: #2563eb; color: white; border-radius: 10px; box-shadow: inset 0 -4px 0 rgba(0,0,0,0.1); }}
        .kpi-bar {{ background:#e5e7eb; height:10px; border-radius:999px; overflow:hidden; }}
        .kpi-fill {{ height:10px; background:#2563eb; }}
        .kpi-fill.red {{ background:#ef4444; }}
        .kpi-fill.yellow {{ background:#f59e0b; }}
        .kpi-fill.green {{ background:#10b981; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size:14px; }}
        th, td {{ border: 1px solid #e5e7eb; padding: 10px; text-align: left; color:#111827; }}
        th {{ background-color: #2563eb; color: #ffffff; }}
        .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 12px; }}
        .badge {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; margin-left:6px; }}
        .badge.high {{ background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }}
        .badge.medium {{ background:#fef3c7; color:#92400e; border:1px solid #fde68a; }}
        .badge.low {{ background:#d1fae5; color:#065f46; border:1px solid #a7f3d0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 ManageBac作业检查报告</h1>
        
        <div class="summary">
            <h2>📈 概览统计</h2>
            <div class="stats">
                <div class="stat-item">
                    <h3>{analysis['total_assignments']}</h3>
                    <p>总任务</p>
                    <div class="kpi-bar" title="总任务">
                        <div class="kpi-fill" style="width:100%"></div>
                    </div>
                </div>
                <div class="stat-item">
                    <h3>{analysis['urgent_count']}</h3>
                    <p>紧急任务</p>
                    <div class="kpi-bar" title="紧急任务">
                        <div class="kpi-fill red" style="width:{(analysis['urgent_count'] / max(analysis['total_assignments'],1)) * 100:.0f}%"></div>
                    </div>
                </div>
                <div class="stat-item">
                    <h3>{len(analysis['by_course'])}</h3>
                    <p>涉及课程</p>
                    <div class="kpi-bar" title="课程覆盖">
                        <div class="kpi-fill green" style="width:{(len(analysis['by_course'])/max(len(analysis['by_course']),1)) * 100:.0f}%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <h2>😨 紧急作业</h2>
        <p>以下为近期（规则：按日期文本粗略判断）更紧急的任务：</p>
        """
        
        # 添加紧急作业
        for assignment in analysis['assignments_by_urgency']['urgent']:
            html += f'''
        <div class="assignment urgent">
            <strong>🔥 {assignment['title'][:100]}</strong><br>
            <em>截止日期: {assignment['due_date']}</em><br>
            <small>状态: {assignment['status']}</small>
        </div>
            '''
        
        # 添加课程统计
        html += """
        <h2>📚 课程统计</h2>
        <table>
            <tr><th>课程</th><th>作业数量</th></tr>
        """
        
        for course, count in analysis['by_course'].items():
            html += f"<tr><td>{course}</td><td>{count}</td></tr>"
        
        html += """
        </table>
        
        <h2>📋 作业分类</h2>
        <div>
            <h3>🟠 未提交（Pending） - {len(analysis['grouped_by_status']['pending'])} 个</h3>
        </div>
        
        """
        
        # Pending 列表
        for i, assignment in enumerate(analysis['grouped_by_status']['pending'], 1):
            priority = self._calculate_priority(assignment)
            priority_class = f"{priority}-priority"
            priority_text = {'high': '🔴 高', 'medium': '🟡 中', 'low': '🟢 低'}[priority]
            html += f'''
        <div class="assignment {priority_class}">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em> |
            <em>优先级: {priority_text}</em>
        </div>
            '''
        
        html += """
        <div style="margin-top:20px;">
            <h3>✅ 已提交（Submitted） - {len(analysis['grouped_by_status']['submitted'])} 个</h3>
        </div>
        """
        
        for i, assignment in enumerate(analysis['grouped_by_status']['submitted'], 1):
            html += f'''
        <div class="assignment low-priority">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em>
        </div>
            '''
        
        html += """
        <div style="margin-top:20px;">
            <h3>⛔ 逾期（Overdue） - {len(analysis['grouped_by_status']['overdue'])} 个</h3>
        </div>
        """
        
        for i, assignment in enumerate(analysis['grouped_by_status']['overdue'], 1):
            html += f'''
        <div class="assignment urgent">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em>
        </div>
            '''
        
        html += f"""
        <div class="footer">
            <p>报告生成时间: {generated_at}</p>
            <p>由 ManageBac Assignment Checker 自动生成</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """生成Markdown格式报告"""
        assignments = data['assignments']
        analysis = data['analysis']
        generated_at = data['generated_at']
        
        md = f"""# 📚 ManageBac作业检查报告

生成时间: {generated_at}

## 📈 概览统计

- 待办作业总数: {analysis['total_assignments']}
- 紧急作业: {analysis['urgent_count']}
- 已提交: {analysis['submitted_count']} | 未提交: {analysis['pending_count']} | 逾期: {analysis['overdue_count']}
- 涉及课程: {len(analysis['by_course'])}

### 优先级分布
- 🔴 高: {analysis['by_priority']['high']}
- 🟡 中: {analysis['by_priority']['medium']}
- 🟢 低: {analysis['by_priority']['low']}

## 😨 紧急作业

"""
        
        if analysis['assignments_by_urgency']['urgent']:
            for assignment in analysis['assignments_by_urgency']['urgent']:
                md += f"- 🔥 {assignment['title'][:100]} — {assignment['due_date']}\n"
        else:
            md += "暂无紧急作业\n"
        
        md += "\n## 📚 课程统计\n\n"
        for course, count in analysis['by_course'].items():
            md += f"- {course}: {count} 个作业\n"
        
        md += "\n## 📋 作业分类\n\n### 🟠 未提交（Pending）\n\n"
        
        for i, assignment in enumerate(analysis['grouped_by_status']['pending'], 1):
            priority = self._calculate_priority(assignment)
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
            md += f"- {i}. {assignment['title'][:100]}\n  - 课程: {assignment.get('course','未知')}\n  - 类型: {assignment.get('type','Unknown')}\n  - 截止日期: {assignment['due_date']}\n  - 状态: {assignment['status']}\n  - 优先级: {priority_emoji} {priority.upper()}\n"
        
        md += "\n### ✅ 已提交（Submitted）\n\n"
        for i, assignment in enumerate(analysis['grouped_by_status']['submitted'], 1):
            md += f"- {i}. {assignment['title'][:100]} — {assignment['due_date']} (课程: {assignment.get('course','未知')}, 类型: {assignment.get('type','Unknown')})\n"
        
        md += "\n### ⛔ 逾期（Overdue）\n\n"
        for i, assignment in enumerate(analysis['grouped_by_status']['overdue'], 1):
            md += f"- {i}. {assignment['title'][:100]} — {assignment['due_date']} (课程: {assignment.get('course','未知')}, 类型: {assignment.get('type','Unknown')})\n"
        
        md += "\n---\n*报告由 ManageBac Assignment Checker 自动生成*"
        
        return md
    
    def _generate_console_report(self, data: Dict[str, Any]) -> str:
        """生成控制台格式报告"""
        return "console_output_handled_in_main_method"
    
    def _calculate_priority(self, assignment: Dict[str, Any]) -> str:
        """计算作业优先级"""
        title = assignment.get('title', '').lower()
        status = assignment.get('status', '').lower()
        
        # 高优先级关键词
        high_priority_keywords = ['summative', 'exam', 'test', 'project', 'essay', 'final']
        if any(keyword in title or keyword in status for keyword in high_priority_keywords):
            return 'high'
        
        # 中优先级关键词
        medium_priority_keywords = ['homework', 'assignment', 'quiz']
        if any(keyword in title or keyword in status for keyword in medium_priority_keywords):
            return 'medium'
        
        return 'low'
    
    def save_reports(self, reports: Dict[str, str]) -> Dict[str, str]:
        """保存报告到文件"""
        saved_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type, content in reports.items():
            if format_type == 'console':
                continue
                
            file_extension = {
                'json': 'json',
                'html': 'html',
                'markdown': 'md'
            }.get(format_type, 'txt')
            
            filename = f"managebac_report_{timestamp}.{file_extension}"
            filepath = self.output_dir / filename
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files[format_type] = str(filepath)
                print(f"\n💾 {format_type.upper()}报告已保存: {filepath}")
            except Exception as e:
                print(f"\n⚠️  保存{format_type}报告失败: {e}")
        
        return saved_files
