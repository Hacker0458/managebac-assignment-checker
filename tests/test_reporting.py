"""
报告生成模块的单元测试
"""

import unittest
import tempfile
import os
from pathlib import Path
from managebac_checker.reporter import ReportGenerator
from managebac_checker.config import Config


class TestReportGenerator(unittest.TestCase):
    """ReportGenerator的测试类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录作为输出目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 创建模拟配置
        self.config = Config()
        self.config.output_dir = Path(self.temp_dir)
        self.config.email = "test@example.com"
        
        self.reporter = ReportGenerator(self.config)
    
    def tearDown(self):
        """清理测试环境"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_json_report_generation(self):
        """测试JSON报告生成"""
        assignments = [{
            'title': 'Test Assignment',
            'course': 'Mathematics',
            'type': 'Formative',
            'due_date': 'Monday',
            'status': 'Pending',
            'submitted': False,
            'overdue': False
        }]
        
        analysis = {
            'total_assignments': 1,
            'urgent_count': 0,
            'submitted_count': 0,
            'pending_count': 1,
            'overdue_count': 0,
            'by_course': {'Mathematics': 1},
            'by_type': {'Formative': 1},
            'by_priority': {'high': 0, 'medium': 1, 'low': 0},
            'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
            'grouped_by_status': {'submitted': [], 'pending': assignments, 'overdue': [], 'unknown': []}
        }
        
        reports = self.reporter.generate_reports(assignments, analysis)
        
        self.assertIn('json', reports)
        json_content = reports['json']
        
        # 验证JSON内容包含必要字段
        self.assertIn('assignments', json_content)
        self.assertIn('analysis', json_content)
        self.assertIn('generated_at', json_content)
        self.assertIn('student_email', json_content)
    
    def test_html_report_generation(self):
        """测试HTML报告生成"""
        assignments = [{
            'title': 'Test Assignment',
            'course': 'Mathematics',
            'type': 'Formative',
            'due_date': 'Monday',
            'status': 'Pending',
            'submitted': False,
            'overdue': False
        }]
        
        analysis = {
            'total_assignments': 1,
            'urgent_count': 0,
            'submitted_count': 0,
            'pending_count': 1,
            'overdue_count': 0,
            'by_course': {'Mathematics': 1},
            'by_type': {'Formative': 1},
            'by_priority': {'high': 0, 'medium': 1, 'low': 0},
            'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
            'grouped_by_status': {'submitted': [], 'pending': assignments, 'overdue': [], 'unknown': []}
        }
        
        reports = self.reporter.generate_reports(assignments, analysis)
        
        self.assertIn('html', reports)
        html_content = reports['html']
        
        # 验证HTML内容包含必要元素
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('ManageBac作业检查报告', html_content)
        self.assertIn('Test Assignment', html_content)
        self.assertIn('Mathematics', html_content)
    
    def test_markdown_report_generation(self):
        """测试Markdown报告生成"""
        assignments = [{
            'title': 'Test Assignment',
            'course': 'Mathematics',
            'type': 'Formative',
            'due_date': 'Monday',
            'status': 'Pending',
            'submitted': False,
            'overdue': False
        }]
        
        analysis = {
            'total_assignments': 1,
            'urgent_count': 0,
            'submitted_count': 0,
            'pending_count': 1,
            'overdue_count': 0,
            'by_course': {'Mathematics': 1},
            'by_type': {'Formative': 1},
            'by_priority': {'high': 0, 'medium': 1, 'low': 0},
            'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
            'grouped_by_status': {'submitted': [], 'pending': assignments, 'overdue': [], 'unknown': []}
        }
        
        reports = self.reporter.generate_reports(assignments, analysis)
        
        self.assertIn('markdown', reports)
        md_content = reports['markdown']
        
        # 验证Markdown内容包含必要元素
        self.assertIn('# 📚 ManageBac作业检查报告', md_content)
        self.assertIn('Test Assignment', md_content)
        self.assertIn('Mathematics', md_content)
    
    def test_priority_calculation(self):
        """测试优先级计算"""
        # 高优先级
        high_priority = {'title': 'Final Exam', 'status': 'Pending'}
        self.assertEqual(self.reporter._calculate_priority(high_priority), 'high')
        
        # 中优先级
        medium_priority = {'title': 'Math Homework', 'status': 'Pending'}
        self.assertEqual(self.reporter._calculate_priority(medium_priority), 'medium')
        
        # 低优先级
        low_priority = {'title': 'Reading Assignment', 'status': 'Pending'}
        self.assertEqual(self.reporter._calculate_priority(low_priority), 'low')
    
    def test_report_saving(self):
        """测试报告保存功能"""
        assignments = [{
            'title': 'Test Assignment',
            'course': 'Mathematics',
            'type': 'Formative',
            'due_date': 'Monday',
            'status': 'Pending',
            'submitted': False,
            'overdue': False
        }]
        
        analysis = {
            'total_assignments': 1,
            'urgent_count': 0,
            'submitted_count': 0,
            'pending_count': 1,
            'overdue_count': 0,
            'by_course': {'Mathematics': 1},
            'by_type': {'Formative': 1},
            'by_priority': {'high': 0, 'medium': 1, 'low': 0},
            'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
            'grouped_by_status': {'submitted': [], 'pending': assignments, 'overdue': [], 'unknown': []}
        }
        
        reports = self.reporter.generate_reports(assignments, analysis)
        saved_files = self.reporter.save_reports(reports)
        
        # 验证文件已保存
        self.assertIn('json', saved_files)
        self.assertTrue(os.path.exists(saved_files['json']))
        
        # 验证文件内容
        with open(saved_files['json'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('Test Assignment', content)


if __name__ == '__main__':
    unittest.main()