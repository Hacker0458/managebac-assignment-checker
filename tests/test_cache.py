"""缓存系统的测试用例。"""

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from managebac_checker.cache import AssignmentCache
from managebac_checker.models import Assignment


@pytest.fixture
def temp_cache_dir():
    """创建临时缓存目录。"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def cache(temp_cache_dir):
    """创建缓存实例。"""
    return AssignmentCache(cache_dir=temp_cache_dir, ttl_minutes=30)


@pytest.fixture
def sample_assignments():
    """创建示例作业列表。"""
    return [
        Assignment(
            identifier="test1",
            title="Test Assignment 1",
            course="Math",
            status="Pending",
            due_date="2024-12-31",
        ),
        Assignment(
            identifier="test2",
            title="Test Assignment 2",
            course="Science",
            status="Submitted",
            due_date="2024-12-30",
        ),
    ]


def test_cache_set_and_get(cache, sample_assignments):
    """测试缓存的设置和获取。"""
    email = "test@example.com"
    url = "https://test.managebac.com"

    # 设置缓存
    cache.set(email, url, sample_assignments)

    # 获取缓存
    cached = cache.get(email, url)

    assert cached is not None
    assert len(cached) == len(sample_assignments)
    assert cached[0].title == sample_assignments[0].title


def test_cache_miss(cache):
    """测试缓存未命中。"""
    cached = cache.get("nonexistent@example.com", "https://test.com")
    assert cached is None


def test_cache_invalidation(cache, sample_assignments):
    """测试缓存失效。"""
    email = "test@example.com"
    url = "https://test.managebac.com"

    # 设置缓存
    cache.set(email, url, sample_assignments)

    # 验证缓存存在
    assert cache.get(email, url) is not None

    # 使缓存失效
    cache.invalidate(email, url)

    # 验证缓存已清除
    assert cache.get(email, url) is None


def test_cache_expiration(temp_cache_dir, sample_assignments):
    """测试缓存过期。"""
    # 创建TTL为0的缓存（立即过期）
    cache = AssignmentCache(cache_dir=temp_cache_dir, ttl_minutes=0)

    email = "test@example.com"
    url = "https://test.managebac.com"

    # 设置缓存
    cache.set(email, url, sample_assignments)

    # 立即获取应该已过期
    cached = cache.get(email, url)
    assert cached is None


def test_cache_clear_all(cache, sample_assignments):
    """测试清除所有缓存。"""
    # 设置多个缓存
    cache.set("user1@example.com", "https://test1.com", sample_assignments)
    cache.set("user2@example.com", "https://test2.com", sample_assignments)

    # 清除所有缓存
    cache.clear_all()

    # 验证所有缓存已清除
    assert cache.get("user1@example.com", "https://test1.com") is None
    assert cache.get("user2@example.com", "https://test2.com") is None


def test_cache_stats(cache, sample_assignments):
    """测试缓存统计信息。"""
    email = "test@example.com"
    url = "https://test.managebac.com"

    # 设置缓存
    cache.set(email, url, sample_assignments)

    # 获取统计信息
    stats = cache.get_stats()

    assert stats["total_entries"] == 1
    assert stats["ttl_minutes"] == 30


def test_cache_max_entries(temp_cache_dir, sample_assignments):
    """测试缓存最大条目限制。"""
    cache = AssignmentCache(cache_dir=temp_cache_dir, max_entries=3)

    # 添加3个缓存
    for i in range(3):
        cache.set(f"user{i}@example.com", f"https://test{i}.com", sample_assignments)

    # 添加第4个应该触发清理
    cache.set("user3@example.com", "https://test3.com", sample_assignments)

    # 验证缓存数量
    stats = cache.get_stats()
    assert stats["total_entries"] <= 3
