#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Professional GUI Module | 测试专业GUI模块
Comprehensive tests for the professional GUI application
专业GUI应用程序的综合测试
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from managebac_checker.professional_gui import (
        ProfessionalTheme,
        ProfessionalButton,
        ProfessionalCard,
        ProfessionalStatusBar,
        ProfessionalManageBacGUI
    )
    from managebac_checker.improved_system_tray import (
        ImprovedSystemTrayManager,
        ImprovedNotificationManager
    )
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ GUI modules not available: {e}")
    GUI_AVAILABLE = False


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestProfessionalTheme(unittest.TestCase):
    """Test ProfessionalTheme class | 测试ProfessionalTheme类"""
    
    def setUp(self):
        self.theme = ProfessionalTheme('professional_light')
    
    def test_theme_initialization(self):
        """Test theme initialization | 测试主题初始化"""
        self.assertEqual(self.theme.current_theme, 'professional_light')
        self.assertIsInstance(self.theme.colors, dict)
        self.assertIsInstance(self.theme.fonts, dict)
    
    def test_get_color(self):
        """Test color retrieval | 测试颜色获取"""
        primary_color = self.theme.get_color('primary')
        self.assertIsInstance(primary_color, str)
        self.assertTrue(primary_color.startswith('#'))
    
    def test_get_font(self):
        """Test font retrieval | 测试字体获取"""
        heading_font = self.theme.get_font('heading')
        self.assertIsInstance(heading_font, tuple)
        self.assertEqual(len(heading_font), 3)
    
    def test_dark_theme(self):
        """Test dark theme | 测试深色主题"""
        dark_theme = ProfessionalTheme('professional_dark')
        self.assertEqual(dark_theme.current_theme, 'professional_dark')
        self.assertNotEqual(dark_theme.get_color('background'), self.theme.get_color('background'))


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestProfessionalButton(unittest.TestCase):
    """Test ProfessionalButton class | 测试ProfessionalButton类"""
    
    def setUp(self):
        self.theme = ProfessionalTheme('professional_light')
        # Mock tkinter for testing
        with patch('tkinter.Button'):
            self.button = ProfessionalButton(None, self.theme, style='primary')
    
    def test_button_initialization(self):
        """Test button initialization | 测试按钮初始化"""
        self.assertIsNotNone(self.button)
        self.assertEqual(self.button.style, 'primary')
    
    def test_button_styles(self):
        """Test different button styles | 测试不同按钮样式"""
        styles = ['primary', 'secondary', 'success', 'warning', 'danger']
        for style in styles:
            with patch('tkinter.Button'):
                button = ProfessionalButton(None, self.theme, style=style)
                self.assertEqual(button.style, style)


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestProfessionalCard(unittest.TestCase):
    """Test ProfessionalCard class | 测试ProfessionalCard类"""
    
    def setUp(self):
        self.theme = ProfessionalTheme('professional_light')
        self.assignment_data = {
            'identifier': '1',
            'title': 'Test Assignment',
            'course': 'Test Course',
            'due_date': '2024-12-31',
            'status': 'pending',
            'priority': 'high',
            'assignment_type': 'Homework',
            'description': 'Test description',
            'link': 'https://example.com',
            'fetched_at': '2024-01-01T00:00:00'
        }
    
    def test_card_initialization(self):
        """Test card initialization | 测试卡片初始化"""
        with patch('tkinter.Frame'):
            card = ProfessionalCard(None, self.theme, self.assignment_data)
            self.assertIsNotNone(card)
            self.assertEqual(card.assignment, self.assignment_data)


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestProfessionalStatusBar(unittest.TestCase):
    """Test ProfessionalStatusBar class | 测试ProfessionalStatusBar类"""
    
    def setUp(self):
        self.theme = ProfessionalTheme('professional_light')
        with patch('tkinter.Frame'):
            self.status_bar = ProfessionalStatusBar(None, self.theme)
    
    def test_status_bar_initialization(self):
        """Test status bar initialization | 测试状态栏初始化"""
        self.assertIsNotNone(self.status_bar)
    
    def test_set_status(self):
        """Test status setting | 测试状态设置"""
        self.status_bar.set_status("Test status", "✅", False)
        # Status should be set (we can't easily test the actual UI update)


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestImprovedSystemTrayManager(unittest.TestCase):
    """Test ImprovedSystemTrayManager class | 测试ImprovedSystemTrayManager类"""
    
    def setUp(self):
        self.tray_manager = ImprovedSystemTrayManager(language='zh')
    
    def test_tray_manager_initialization(self):
        """Test tray manager initialization | 测试托盘管理器初始化"""
        self.assertIsNotNone(self.tray_manager)
        self.assertEqual(self.tray_manager.language, 'zh')
    
    def test_get_message(self):
        """Test message retrieval | 测试消息获取"""
        message = self.tray_manager.get_message('app_name')
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
    
    def test_notify_assignments(self):
        """Test assignment notification | 测试作业通知"""
        # Test with no assignments
        self.tray_manager.notify_assignments(0, 0)
        
        # Test with assignments
        self.tray_manager.notify_assignments(5, 2)


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestImprovedNotificationManager(unittest.TestCase):
    """Test ImprovedNotificationManager class | 测试ImprovedNotificationManager类"""
    
    def setUp(self):
        self.notification_manager = ImprovedNotificationManager('zh')
    
    def test_notification_manager_initialization(self):
        """Test notification manager initialization | 测试通知管理器初始化"""
        self.assertIsNotNone(self.notification_manager)
        self.assertEqual(self.notification_manager.language, 'zh')
    
    def test_is_available(self):
        """Test availability check | 测试可用性检查"""
        self.assertTrue(self.notification_manager.is_available())
    
    def test_send_notification(self):
        """Test notification sending | 测试通知发送"""
        # This should not raise an exception
        self.notification_manager.send_notification("Test", "Test message")
    
    def test_notify_assignment_reminder(self):
        """Test assignment reminder notification | 测试作业提醒通知"""
        assignments = [
            {'status': 'overdue', 'priority': 'high'},
            {'status': 'pending', 'priority': 'medium'}
        ]
        # This should not raise an exception
        self.notification_manager.notify_assignment_reminder(assignments)


@unittest.skipUnless(GUI_AVAILABLE, "GUI modules not available")
class TestProfessionalManageBacGUI(unittest.TestCase):
    """Test ProfessionalManageBacGUI class | 测试ProfessionalManageBacGUI类"""
    
    def setUp(self):
        # Mock tkinter components
        with patch('tkinter.Tk'), \
             patch('tkinter.Menu'), \
             patch('tkinter.Frame'), \
             patch('tkinter.Label'), \
             patch('tkinter.Button'), \
             patch('tkinter.Entry'), \
             patch('tkinter.Canvas'), \
             patch('tkinter.PanedWindow'):
            
            self.gui = ProfessionalManageBacGUI()
    
    def test_gui_initialization(self):
        """Test GUI initialization | 测试GUI初始化"""
        self.assertIsNotNone(self.gui)
        self.assertIsNotNone(self.gui.theme)
    
    def test_generate_sample_assignments(self):
        """Test sample assignment generation | 测试示例作业生成"""
        assignments = self.gui._generate_sample_assignments()
        self.assertIsInstance(assignments, list)
        self.assertGreater(len(assignments), 0)
        
        # Check assignment structure
        if assignments:
            assignment = assignments[0]
            required_keys = ['identifier', 'title', 'course', 'due_date', 'status', 'priority']
            for key in required_keys:
                self.assertIn(key, assignment)
    
    def test_update_stats(self):
        """Test statistics update | 测试统计更新"""
        # Set up some test assignments
        self.gui.assignments = [
            {'status': 'overdue', 'priority': 'high'},
            {'status': 'pending', 'priority': 'medium'},
            {'status': 'completed', 'priority': 'low'}
        ]
        
        # This should not raise an exception
        self.gui._update_stats()
    
    def test_apply_filters(self):
        """Test filter application | 测试筛选应用"""
        # Set up test assignments
        self.gui.assignments = [
            {'status': 'overdue', 'priority': 'high'},
            {'status': 'pending', 'priority': 'medium'},
            {'status': 'completed', 'priority': 'low'}
        ]
        
        # Initialize filter variables
        self.gui.filter_vars = {
            'show_overdue': Mock(value=False),
            'show_high_priority': Mock(value=False),
            'show_pending': Mock(value=False),
            'show_completed': Mock(value=True)
        }
        
        # This should not raise an exception
        self.gui._apply_filters()


class TestGUIIntegration(unittest.TestCase):
    """Test GUI integration | 测试GUI集成"""
    
    def test_gui_imports(self):
        """Test GUI module imports | 测试GUI模块导入"""
        try:
            from managebac_checker.professional_gui import main
            from managebac_checker.improved_system_tray import ImprovedSystemTrayManager
            self.assertTrue(True, "GUI modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import GUI modules: {e}")
    
    def test_gui_launcher_import(self):
        """Test GUI launcher import | 测试GUI启动器导入"""
        try:
            import gui_launcher
            self.assertTrue(True, "GUI launcher imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import GUI launcher: {e}")


if __name__ == '__main__':
    # Set up test environment
    os.environ['MANAGEBAC_EMAIL'] = 'test@example.com'
    os.environ['MANAGEBAC_PASSWORD'] = 'testpassword'
    os.environ['MANAGEBAC_URL'] = 'https://test.managebac.com'
    os.environ['HEADLESS'] = 'true'
    os.environ['DEBUG'] = 'false'
    
    # Run tests
    unittest.main(verbosity=2)
