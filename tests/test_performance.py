"""性能监控系统的测试用例。"""

import asyncio
import time

import pytest

from managebac_checker.performance import (
    BatchProcessor,
    PerformanceMonitor,
    RateLimiter,
    timeit,
)


@pytest.fixture
def monitor():
    """创建性能监控器实例。"""
    return PerformanceMonitor()


def test_performance_monitor_record(monitor):
    """测试性能监控器记录功能。"""
    monitor.record("test_operation", 1.5)
    monitor.record("test_operation", 2.0)

    stats = monitor.get_stats()

    assert "test_operation" in stats
    assert stats["test_operation"]["count"] == 2
    assert stats["test_operation"]["avg"] == 1.75


def test_performance_monitor_measure(monitor):
    """测试性能监控器上下文管理器。"""
    with monitor.measure("test_operation"):
        time.sleep(0.1)

    stats = monitor.get_stats()

    assert "test_operation" in stats
    assert stats["test_operation"]["count"] == 1
    assert stats["test_operation"]["avg"] >= 0.1


@pytest.mark.asyncio
async def test_performance_monitor_measure_async(monitor):
    """测试异步性能监控器上下文管理器。"""
    async with monitor.measure_async("async_operation"):
        await asyncio.sleep(0.1)

    stats = monitor.get_stats()

    assert "async_operation" in stats
    assert stats["async_operation"]["count"] == 1
    assert stats["async_operation"]["avg"] >= 0.1


def test_performance_monitor_reset(monitor):
    """测试性能监控器重置功能。"""
    monitor.record("test_operation", 1.0)
    monitor.reset()

    stats = monitor.get_stats()
    assert len(stats) == 0


def test_timeit_decorator():
    """测试timeit装饰器。"""

    @timeit
    def sample_function():
        time.sleep(0.1)
        return "result"

    result = sample_function()

    assert result == "result"


@pytest.mark.asyncio
async def test_timeit_decorator_async():
    """测试异步timeit装饰器。"""

    @timeit
    async def async_sample_function():
        await asyncio.sleep(0.1)
        return "async_result"

    result = await async_sample_function()

    assert result == "async_result"


@pytest.mark.asyncio
async def test_rate_limiter():
    """测试速率限制器。"""
    limiter = RateLimiter(max_calls=2, period=1.0)

    start_time = time.time()

    # 前两次调用应该立即执行
    await limiter.acquire()
    await limiter.acquire()

    # 第三次调用应该等待
    await limiter.acquire()

    elapsed = time.time() - start_time

    # 应该至少等待了接近1秒
    assert elapsed >= 0.9


@pytest.mark.asyncio
async def test_batch_processor():
    """测试批处理器。"""
    processor = BatchProcessor(batch_size=3, max_wait=1.0)

    # 添加项目
    await processor.add("item1")
    await processor.add("item2")

    # 第三个项目应该触发刷新
    await processor.add("item3")

    # 队列应该被清空
    assert len(processor.queue) == 0


@pytest.mark.asyncio
async def test_batch_processor_flush():
    """测试批处理器刷新功能。"""
    processor = BatchProcessor(batch_size=10, max_wait=1.0)

    await processor.add("item1")
    await processor.add("item2")

    items = await processor.flush()

    assert len(items) == 2
    assert "item1" in items
    assert "item2" in items
    assert len(processor.queue) == 0
