"""性能监控和优化工具。"""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class PerformanceMonitor:
    """性能监控器，跟踪函数执行时间和资源使用。"""

    def __init__(self) -> None:
        """初始化性能监控器。"""
        self.metrics: Dict[str, List[float]] = {}
        self.call_counts: Dict[str, int] = {}

    def record(self, operation: str, duration: float) -> None:
        """
        记录操作执行时间。

        Args:
            operation: 操作名称
            duration: 执行时长（秒）
        """
        if operation not in self.metrics:
            self.metrics[operation] = []
            self.call_counts[operation] = 0

        self.metrics[operation].append(duration)
        self.call_counts[operation] += 1

    @contextmanager
    def measure(self, operation: str):
        """
        上下文管理器，用于测量代码块执行时间。

        Args:
            operation: 操作名称

        Example:
            with monitor.measure("login"):
                await perform_login()
        """
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            self.record(operation, duration)

    @asynccontextmanager
    async def measure_async(self, operation: str):
        """
        异步上下文管理器，用于测量异步代码块执行时间。

        Args:
            operation: 操作名称

        Example:
            async with monitor.measure_async("scraping"):
                await scrape_assignments()
        """
        start_time = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            self.record(operation, duration)

    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """
        获取性能统计信息。

        Returns:
            包含各操作统计数据的字典
        """
        stats = {}
        for operation, durations in self.metrics.items():
            if durations:
                stats[operation] = {
                    "count": self.call_counts[operation],
                    "total": sum(durations),
                    "avg": sum(durations) / len(durations),
                    "min": min(durations),
                    "max": max(durations),
                    "last": durations[-1],
                }
        return stats

    def reset(self) -> None:
        """重置所有统计数据。"""
        self.metrics.clear()
        self.call_counts.clear()

    def print_stats(self) -> None:
        """打印性能统计信息。"""
        print("\n" + "=" * 80)
        print("⚡ 性能统计报告")
        print("=" * 80)

        stats = self.get_stats()
        if not stats:
            print("无性能数据")
            return

        for operation, data in sorted(
            stats.items(), key=lambda x: x[1]["total"], reverse=True
        ):
            print(f"\n📊 {operation}:")
            print(f"   调用次数: {data['count']}")
            print(f"   总耗时: {data['total']:.3f}s")
            print(f"   平均耗时: {data['avg']:.3f}s")
            print(f"   最小耗时: {data['min']:.3f}s")
            print(f"   最大耗时: {data['max']:.3f}s")


def timeit(func: F) -> F:
    """
    装饰器：自动测量函数执行时间。

    Args:
        func: 要测量的函数

    Returns:
        包装后的函数
    """
    monitor = PerformanceMonitor()

    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            async with monitor.measure_async(func.__name__):
                return await func(*args, **kwargs)

        return async_wrapper  # type: ignore

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        with monitor.measure(func.__name__):
            return func(*args, **kwargs)

    return sync_wrapper  # type: ignore


class RateLimiter:
    """速率限制器，防止请求过于频繁。"""

    def __init__(self, max_calls: int, period: float) -> None:
        """
        初始化速率限制器。

        Args:
            max_calls: 时间窗口内的最大调用次数
            period: 时间窗口（秒）
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []

    async def acquire(self) -> None:
        """
        获取执行权限，如果超过速率限制则等待。

        Example:
            limiter = RateLimiter(max_calls=5, period=1.0)
            await limiter.acquire()
            # 执行操作
        """
        now = time.time()

        # 清理过期的调用记录
        self.calls = [call_time for call_time in self.calls if now - call_time < self.period]

        if len(self.calls) >= self.max_calls:
            # 计算需要等待的时间
            wait_time = self.period - (now - self.calls[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            # 重新清理
            now = time.time()
            self.calls = [
                call_time for call_time in self.calls if now - call_time < self.period
            ]

        self.calls.append(time.time())


class BatchProcessor:
    """批处理器，用于优化多个小任务的执行。"""

    def __init__(self, batch_size: int = 10, max_wait: float = 1.0) -> None:
        """
        初始化批处理器。

        Args:
            batch_size: 批次大小
            max_wait: 最大等待时间（秒）
        """
        self.batch_size = batch_size
        self.max_wait = max_wait
        self.queue: List[Any] = []
        self.last_flush = time.time()

    async def add(self, item: Any) -> None:
        """
        添加项目到批次队列。

        Args:
            item: 要处理的项目
        """
        self.queue.append(item)

        # 检查是否需要刷新
        if len(self.queue) >= self.batch_size or (
            time.time() - self.last_flush >= self.max_wait
        ):
            await self.flush()

    async def flush(self) -> List[Any]:
        """
        刷新队列，返回所有待处理项目。

        Returns:
            待处理项目列表
        """
        if not self.queue:
            return []

        items = self.queue.copy()
        self.queue.clear()
        self.last_flush = time.time()
        return items


# 全局性能监控器实例
_global_monitor: Optional[PerformanceMonitor] = None


def get_global_monitor() -> PerformanceMonitor:
    """
    获取全局性能监控器实例。

    Returns:
        全局性能监控器
    """
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor
