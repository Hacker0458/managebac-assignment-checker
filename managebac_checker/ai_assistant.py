#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Assistant Module | AI助手模块
Enhanced with OpenAI integration for intelligent analysis and suggestions
增强的OpenAI集成，提供智能分析和建议
"""

import os
import json
from typing import Dict, List, Optional, Any

# from datetime import datetime  # Unused import
import openai
from .models import Assignment
from .logging_utils import get_logger

logger = get_logger(__name__)


class AIAssistant:
    """AI Assistant for intelligent analysis | 智能分析AI助手"""

    # Bilingual messages | 双语消息
    MESSAGES = {
        "en": {
            "init": "🤖 Initializing AI Assistant...",
            "enabled": "✅ AI Assistant enabled with API key",
            "disabled": "❌ AI Assistant disabled (no API key provided)",
            "analyzing": "🔍 Analyzing assignments with AI...",
            "generating": "💡 Generating intelligent suggestions...",
            "error": "❌ AI analysis error: {}",
            "no_key": "⚠️ No OpenAI API key provided. AI features disabled.",
            "invalid_key": "❌ Invalid OpenAI API key. Please check your configuration.",
            "success": "✅ AI analysis completed successfully",
            "suggestion": "💡 AI Suggestion: {}",
            "priority_advice": "📊 Priority Management Advice",
            "study_plan": "📚 Recommended Study Plan",
            "time_management": "⏰ Time Management Tips",
        },
        "zh": {
            "init": "🤖 正在初始化AI助手...",
            "enabled": "✅ AI助手已启用（已提供API密钥）",
            "disabled": "❌ AI助手已禁用（未提供API密钥）",
            "analyzing": "🔍 正在使用AI分析作业...",
            "generating": "💡 正在生成智能建议...",
            "error": "❌ AI分析错误：{}",
            "no_key": "⚠️ 未提供OpenAI API密钥。AI功能已禁用。",
            "invalid_key": "❌ OpenAI API密钥无效。请检查您的配置。",
            "success": "✅ AI分析成功完成",
            "suggestion": "💡 AI建议：{}",
            "priority_advice": "📊 优先级管理建议",
            "study_plan": "📚 推荐学习计划",
            "time_management": "⏰ 时间管理技巧",
        },
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        language: str = "en",
        enable_ai: bool = True,
        model: str = "gpt-3.5-turbo",
    ):
        """
        Initialize AI Assistant | 初始化AI助手

        Args:
            api_key: OpenAI API key (optional) | OpenAI API密钥（可选）
            language: Interface language ('en' or 'zh') | 界面语言
            enable_ai: Whether to enable AI features | 是否启用AI功能
            model: OpenAI model to use | 使用的OpenAI模型
        """
        self.language = language
        self.enable_ai = enable_ai
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None

        self._log("init")

        if self.enable_ai and self.api_key:
            try:
                openai.api_key = self.api_key
                self.client = openai
                self._log("enabled")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self._log("invalid_key")
                self.enable_ai = False
        else:
            self._log("disabled" if not self.enable_ai else "no_key")

    def _log(self, key: str, *args):
        """Log bilingual message | 记录双语消息"""
        msg = self.MESSAGES[self.language].get(key, key)
        if args:
            msg = msg.format(*args)
        logger.info(msg)
        return msg

    def analyze_assignments(
        self, assignments: List[Assignment], analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze assignments with AI | 使用AI分析作业

        Args:
            assignments: List of assignments | 作业列表
            analysis_data: Analysis data from analyzer | 分析器的分析数据

        Returns:
            AI-enhanced analysis results | AI增强的分析结果
        """
        if not self.enable_ai or not self.client:
            return {"enabled": False, "message": self._log("disabled")}

        try:
            self._log("analyzing")

            # Prepare assignment data for AI | 为AI准备作业数据
            assignment_summary = self._prepare_assignment_summary(
                assignments, analysis_data
            )

            # Generate AI insights | 生成AI洞察
            insights = self._generate_insights(assignment_summary)

            # Generate study recommendations | 生成学习建议
            recommendations = self._generate_recommendations(
                assignment_summary, insights
            )

            # Generate time management plan | 生成时间管理计划
            time_plan = self._generate_time_plan(assignments, analysis_data)

            self._log("success")

            return {
                "enabled": True,
                "insights": insights,
                "recommendations": recommendations,
                "time_plan": time_plan,
                "summary": self._generate_summary(insights, recommendations),
                "message": self._log("success"),
            }

        except Exception as e:
            error_msg = self._log("error", str(e))
            logger.error(f"AI analysis failed: {e}")
            return {"enabled": False, "error": str(e), "message": error_msg}

    def _prepare_assignment_summary(
        self, assignments: List[Assignment], analysis_data: Dict[str, Any]
    ) -> str:
        """Prepare assignment summary for AI | 为AI准备作业摘要"""
        summary = []

        # Add basic statistics | 添加基本统计
        summary.append(f"Total assignments: {len(assignments)}")
        summary.append(f"Overdue: {analysis_data.get('overdue_count', 0)}")
        summary.append(f"Due this week: {analysis_data.get('due_this_week', 0)}")

        # Add priority distribution | 添加优先级分布
        priority_dist = analysis_data.get("priority_distribution", {})
        summary.append(f"High priority: {priority_dist.get('high', 0)}")
        summary.append(f"Medium priority: {priority_dist.get('medium', 0)}")
        summary.append(f"Low priority: {priority_dist.get('low', 0)}")

        # Add course distribution | 添加课程分布
        course_dist = analysis_data.get("course_distribution", {})
        summary.append(f"Courses with assignments: {len(course_dist)}")

        # Add assignment details | 添加作业详情
        summary.append("\nAssignment details:")
        for assignment in assignments[:10]:  # Limit to first 10 for API
            summary.append(
                f"- {assignment.title} ({assignment.course}): Due {assignment.due_date}"
            )

        return "\n".join(summary)

    def _generate_insights(self, assignment_summary: str) -> Dict[str, str]:
        """Generate AI insights | 生成AI洞察"""
        if not self.client:
            return {}

        try:
            prompt = f"""
            Based on the following assignment summary, provide insights in {self.language}:
            
            {assignment_summary}
            
            Please provide:
            1. Overall workload assessment
            2. Key challenges identified
            3. Recommended focus areas
            4. Risk factors to watch
            
            Format as JSON with keys: workload, challenges, focus_areas, risks
            """

            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational assistant helping students manage their assignments.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )

            content = response.choices[0].message.content

            # Try to parse JSON response | 尝试解析JSON响应
            try:
                return json.loads(content)
            except (json.JSONDecodeError, TypeError):
                return {"analysis": content}

        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")
            return {}

    def _generate_recommendations(
        self, assignment_summary: str, insights: Dict[str, str]
    ) -> List[str]:
        """Generate study recommendations | 生成学习建议"""
        if not self.client:
            return []

        try:
            prompt = f"""
            Based on the assignment summary and insights, provide 5 actionable recommendations in {self.language}:
            
            Summary: {assignment_summary}
            Insights: {json.dumps(insights)}
            
            Provide practical, specific recommendations for managing these assignments effectively.
            Return as a JSON array of strings.
            """

            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational assistant providing study recommendations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )

            content = response.choices[0].message.content

            try:
                return json.loads(content)
            except (json.JSONDecodeError, TypeError):
                return [content]

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []

    def _generate_time_plan(
        self, assignments: List[Assignment], analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate time management plan | 生成时间管理计划"""
        if not self.client:
            return {}

        try:
            # Prepare assignment list for planning | 准备计划的作业列表
            assignment_list = []
            for assignment in assignments[:10]:
                assignment_list.append(
                    {
                        "title": assignment.title,
                        "course": assignment.course,
                        "due_date": assignment.due_date,
                        "priority": analysis_data.get("priorities", {}).get(
                            assignment.title, "medium"
                        ),
                    }
                )

            prompt = f"""
            Create a time management plan in {self.language} for these assignments:
            {json.dumps(assignment_list, indent=2)}
            
            Provide:
            1. Daily schedule suggestions
            2. Priority order for completion
            3. Time allocation recommendations
            4. Break and rest periods
            
            Format as JSON with keys: daily_schedule, priority_order, time_allocation, breaks
            """

            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a time management expert helping students plan their work.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )

            content = response.choices[0].message.content

            try:
                return json.loads(content)
            except (json.JSONDecodeError, TypeError):
                return {"plan": content}

        except Exception as e:
            logger.error(f"Failed to generate time plan: {e}")
            return {}

    def _generate_summary(
        self, insights: Dict[str, str], recommendations: List[str]
    ) -> str:
        """Generate executive summary | 生成执行摘要"""
        if self.language == "zh":
            summary = "🤖 AI助手分析摘要\n\n"

            if insights:
                summary += "📊 关键洞察：\n"
                for key, value in insights.items():
                    summary += f"• {value}\n"

            if recommendations:
                summary += "\n💡 建议行动：\n"
                for i, rec in enumerate(recommendations[:5], 1):
                    summary += f"{i}. {rec}\n"
        else:
            summary = "🤖 AI Assistant Analysis Summary\n\n"

            if insights:
                summary += "📊 Key Insights:\n"
                for key, value in insights.items():
                    summary += f"• {value}\n"

            if recommendations:
                summary += "\n💡 Recommended Actions:\n"
                for i, rec in enumerate(recommendations[:5], 1):
                    summary += f"{i}. {rec}\n"

        return summary

    def get_quick_suggestion(self, assignment: Assignment) -> str:
        """
        Get quick AI suggestion for a single assignment | 获取单个作业的快速AI建议

        Args:
            assignment: Assignment to analyze | 要分析的作业

        Returns:
            Quick suggestion string | 快速建议字符串
        """
        if not self.enable_ai or not self.client:
            return ""

        try:
            prompt = f"""
            Provide a brief suggestion in {self.language} for this assignment:
            Title: {assignment.title}
            Course: {assignment.course}
            Due: {assignment.due_date}
            
            Give one concise, actionable tip (max 50 words).
            """

            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=100,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Failed to get quick suggestion: {e}")
            return ""
