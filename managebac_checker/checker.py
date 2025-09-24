"""向后兼容的 ManageBacChecker 封装。"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from .config import Config
from .runner import Runner
from .logging_utils import setup_logging, BilingualLogger


class ManageBacChecker:
    """提供与旧接口兼容的高层封装。"""

    def __init__(
        self, config: Optional[Config] = None, logger: Optional[BilingualLogger] = None
    ) -> None:
        self.config = config or Config.from_environment()
        self.runner = Runner(config=self.config)
        self.logger = logger or self.runner.logger

    async def run(self) -> Dict[str, Any]:
        """运行作业检查流程，返回结果。"""
        return await self.runner.execute()

    def run_sync(self) -> Dict[str, Any]:
        """同步运行入口，便于脚本或 GUI 调用。"""
        return asyncio.run(self.run())
