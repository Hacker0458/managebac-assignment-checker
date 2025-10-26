#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Integration Test Script | AI集成测试脚本
Test the AI Assistant functionality with a sample API key
测试AI助手功能与示例API密钥
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from managebac_checker.config import Config
from managebac_checker.ai_assistant import AIAssistant
from managebac_checker.models import Assignment
from datetime import datetime, timedelta


def test_ai_assistant():
    """Test AI Assistant with provided API key"""
    
    # Set test API key
    test_api_key = "sk-CtUYzSvFIDu0yoANa5Kpj8ulTzkySCpatTgrc1tUDS6tYaTl"
    
    print("=" * 60)
    print("🤖 Testing AI Assistant Integration | 测试AI助手集成")
    print("=" * 60)
    
    # Test both languages
    for language in ['en', 'zh']:
        print(f"\n📝 Testing in {language.upper()} | 测试{language.upper()}语言")
        print("-" * 40)
        
        # Initialize AI Assistant
        ai = AIAssistant(
            api_key=test_api_key,
            language=language,
            enable_ai=True,
            model="gpt-3.5-turbo"
        )
        
        # Create sample assignments
        assignments = [
            Assignment(
                identifier="1",
                title="Math Homework Chapter 5",
                course="Mathematics",
                due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                status="pending",
                assignment_type="Homework",
                priority="high"
            ),
            Assignment(
                identifier="2",
                title="Physics Lab Report",
                course="Physics",
                due_date=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                status="pending",
                assignment_type="Lab Report",
                priority="medium"
            ),
            Assignment(
                identifier="3",
                title="English Essay Draft",
                course="English",
                due_date=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                status="overdue",
                assignment_type="Essay",
                priority="high"
            ),
            Assignment(
                identifier="4",
                title="History Reading",
                course="History",
                due_date=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                status="pending",
                assignment_type="Reading",
                priority="low"
            )
        ]
        
        # Create analysis data
        analysis_data = {
            'overdue_count': 1,
            'due_this_week': 3,
            'priority_distribution': {
                'high': 2,
                'medium': 1,
                'low': 1
            },
            'course_distribution': {
                'Mathematics': 1,
                'Physics': 1,
                'English': 1,
                'History': 1
            }
        }
        
        # Test AI analysis
        print("\n🔍 Running AI Analysis... | 运行AI分析...")
        try:
            results = ai.analyze_assignments(assignments, analysis_data)
            
            if results['enabled']:
                print("✅ AI Analysis Successful! | AI分析成功！")
                
                # Display insights
                if 'insights' in results:
                    print("\n💡 Insights | 洞察:")
                    for key, value in results['insights'].items():
                        print(f"  • {key}: {value}")
                
                # Display recommendations
                if 'recommendations' in results:
                    print("\n📋 Recommendations | 建议:")
                    for i, rec in enumerate(results['recommendations'], 1):
                        print(f"  {i}. {rec}")
                
                # Display time plan
                if 'time_plan' in results:
                    print("\n⏰ Time Management Plan | 时间管理计划:")
                    if isinstance(results['time_plan'], dict):
                        for key, value in results['time_plan'].items():
                            print(f"  • {key}: {value}")
                    else:
                        print(f"  {results['time_plan']}")
                
                # Display summary
                if 'summary' in results:
                    print("\n📊 Summary | 总结:")
                    print(results['summary'])
                
            else:
                print(f"⚠️ AI Analysis Disabled: {results.get('message', 'Unknown reason')}")
                
        except Exception as e:
            print(f"❌ Error during AI analysis: {e}")
        
        # Test quick suggestions
        print("\n💭 Testing Quick Suggestions | 测试快速建议:")
        for assignment in assignments[:2]:
            try:
                suggestion = ai.get_quick_suggestion(assignment)
                if suggestion:
                    print(f"\n📚 {assignment.title}:")
                    print(f"   💡 {suggestion}")
                else:
                    print(f"\n📚 {assignment.title}: No suggestion available")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ AI Integration Test Complete! | AI集成测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    # Run the test
    test_ai_assistant()
    
    print("\n📝 Note: This test uses a sample API key for demonstration.")
    print("   Please replace with your own API key in production.")
    print("\n📝 注意：此测试使用示例API密钥进行演示。")
    print("   请在生产环境中替换为您自己的API密钥。")
