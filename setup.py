"""
🎓 ManageBac Assignment Checker | ManageBac作业检查器
=====================================================

An intelligent automation tool for ManageBac assignment tracking.
一个用于ManageBac作业追踪的智能自动化工具。

Author: Hacker0458
License: MIT
"""

from setuptools import setup, find_packages
import os


# Read README file | 读取README文件
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "ManageBac Assignment Checker - An intelligent automation tool for assignment tracking."


# Read requirements file | 读取requirements文件
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [
                line.strip() for line in fh if line.strip() and not line.startswith("#")
            ]
    except FileNotFoundError:
        return [
            "playwright>=1.40.0",
            "python-dotenv>=1.0.0",
            "pytest>=7.4.3",
            "black>=23.11.0",
            "flake8>=6.1.0",
        ]


setup(
    name="managebac-assignment-checker",
    version="2.0.0",
    author="Hacker0458",
    author_email="",
    description="🎯 An intelligent automation tool for ManageBac assignment tracking | 智能ManageBac作业追踪工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Hacker0458/managebac-assignment-checker",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pre-commit>=3.5.0",
        ],
        "charts": [
            "matplotlib>=3.7.0",
            "plotly>=5.17.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "managebac-checker=managebac_checker.cli:main",
            "mbc=managebac_checker.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "managebac",
        "assignment",
        "checker",
        "automation",
        "education",
        "web-scraping",
        "student",
        "homework",
        "tracking",
        "notification",
        "report",
        "analysis",
        "productivity",
        "school",
        "academic",
    ],
    project_urls={
        "Homepage": "https://github.com/Hacker0458/managebac-assignment-checker",
        "Bug Reports": "https://github.com/Hacker0458/managebac-assignment-checker/issues",
        "Source Code": "https://github.com/Hacker0458/managebac-assignment-checker",
        "Documentation": "https://github.com/Hacker0458/managebac-assignment-checker#readme",
        "Changelog": "https://github.com/Hacker0458/managebac-assignment-checker/releases",
    },
    package_data={
        "managebac_checker": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
        ],
    },
)
