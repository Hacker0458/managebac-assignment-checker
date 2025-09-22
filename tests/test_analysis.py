"""
分析模块的单元测试
"""

import unittest
from datetime import datetime
from managebac_checker.analyzer import AssignmentAnalyzer
from managebac_checker.config import Config


class TestAssignmentAnalyzer(unittest.TestCase):
    """AssignmentAnalyzer的测试类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建模拟配置
        self.config = Config()
        self.analyzer = AssignmentAnalyzer(self.config)
    
    def test_empty_assignments(self):
        """测试空作业列表"""
        assignments = []
        analysis = self.analyzer.analyze_assignments(assignments)
        
        self.assertEqual(analysis['total_assignments'], 0)
        self.assertEqual(analysis['urgent_count'], 0)
        self.assertEqual(analysis['submitted_count'], 0)
        self.assertEqual(analysis['pending_count'], 0)
        self.assertEqual(analysis['overdue_count'], 0)
    
    def test_single_assignment(self):
        """测试单个作业"""
        assignments = [{
            'title': 'Math Homework',
            'course': 'Mathematics',
            'type': 'Formative',
            'due_date': 'Monday',
            'status': 'Pending',
            'submitted': False,
            'overdue': False
        }]
        
        analysis = self.analyzer.analyze_assignments(assignments)
        
        self.assertEqual(analysis['total_assignments'], 1)
        self.assertEqual(analysis['pending_count'], 1)
        self.assertEqual(analysis['by_course']['Mathematics'], 1)
        self.assertEqual(analysis['by_type']['Formative'], 1)
    
    def test_priority_calculation(self):
        """测试优先级计算"""
        # 高优先级作业
        high_priority = {
            'title': 'Final Exam',
            'status': 'Pending'
        }
        self.assertEqual(self.analyzer._calculate_priority(high_priority), 'high')
        
        # 中优先级作业
        medium_priority = {
            'title': 'Math Homework',
            'status': 'Pending'
        }
        self.assertEqual(self.analyzer._calculate_priority(medium_priority), 'medium')
        
        # 低优先级作业
        low_priority = {
            'title': 'Reading Assignment',
            'status': 'Pending'
        }
        self.assertEqual(self.analyzer._calculate_priority(low_priority), 'low')
    
    def test_course_extraction(self):
        """测试课程名称提取"""
        # AP课程
        ap_title = "AP Computer Science Assignment"
        self.assertEqual(self.analyzer._extract_course_name(ap_title), "AP Computer Science Assignment")
        
        # 数学课程
        math_title = "Calculus BC Homework"
        self.assertEqual(self.analyzer._extract_course_name(math_title), "Mathematics")
        
        # 未知课程
        unknown_title = "Random Assignment"
        self.assertEqual(self.analyzer._extract_course_name(unknown_title), "未知课程")
    
    def test_urgency_calculation(self):
        """测试紧急程度计算"""
        now = datetime.now()
        
        # 紧急作业
        urgent_assignment = {'due_date': 'Monday'}
        self.assertEqual(self.analyzer._calculate_urgency(urgent_assignment, now), 'urgent')
        
        # 较急作业
        soon_assignment = {'due_date': 'Tuesday'}
        self.assertEqual(self.analyzer._calculate_urgency(soon_assignment, now), 'soon')
        
        # 不急作业
        later_assignment = {'due_date': 'Friday'}
        self.assertEqual(self.analyzer._calculate_urgency(later_assignment, now), 'later')


if __name__ == '__main__':
    unittest.main()