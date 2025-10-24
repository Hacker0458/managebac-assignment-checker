"""智能缓存系统，提升性能并减少不必要的请求。"""

from __future__ import annotations

import hashlib
import json
import pickle
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import Assignment


class AssignmentCache:
    """作业数据缓存管理器，支持时间过期和智能失效。"""

    def __init__(
        self,
        cache_dir: Path | str = "./cache",
        ttl_minutes: int = 30,
        max_entries: int = 100,
    ) -> None:
        """
        初始化缓存管理器。

        Args:
            cache_dir: 缓存目录路径
            ttl_minutes: 缓存生存时间（分钟）
            max_entries: 最大缓存条目数
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(minutes=ttl_minutes)
        self.max_entries = max_entries
        self.metadata_file = self.cache_dir / "metadata.json"
        self._load_metadata()

    def _load_metadata(self) -> None:
        """加载缓存元数据。"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    self.metadata: Dict[str, Any] = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.metadata = {"entries": {}, "last_cleanup": None}
        else:
            self.metadata = {"entries": {}, "last_cleanup": None}

    def _save_metadata(self) -> None:
        """保存缓存元数据。"""
        try:
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _get_cache_key(self, email: str, url: str) -> str:
        """生成缓存键。"""
        key_string = f"{email}:{url}"
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(self, email: str, url: str) -> Optional[List[Assignment]]:
        """
        从缓存获取作业数据。

        Args:
            email: 用户邮箱
            url: ManageBac URL

        Returns:
            缓存的作业列表，如果不存在或已过期则返回None
        """
        cache_key = self._get_cache_key(email, url)
        entry = self.metadata["entries"].get(cache_key)

        if not entry:
            return None

        # 检查是否过期
        cached_time = datetime.fromisoformat(entry["timestamp"])
        now = datetime.now(timezone.utc)

        if now - cached_time > self.ttl:
            # 过期，删除缓存
            self.invalidate(email, url)
            return None

        # 读取缓存文件
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "rb") as f:
                assignments = pickle.load(f)
            return assignments
        except (pickle.PickleError, IOError):
            # 缓存损坏，删除
            self.invalidate(email, url)
            return None

    def set(self, email: str, url: str, assignments: List[Assignment]) -> None:
        """
        保存作业数据到缓存。

        Args:
            email: 用户邮箱
            url: ManageBac URL
            assignments: 作业列表
        """
        cache_key = self._get_cache_key(email, url)

        # 检查是否需要清理旧缓存
        if len(self.metadata["entries"]) >= self.max_entries:
            self._cleanup_old_entries()

        # 保存数据
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(assignments, f)

            # 更新元数据
            self.metadata["entries"][cache_key] = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "count": len(assignments),
                "email": email,
            }
            self._save_metadata()
        except (pickle.PickleError, IOError):
            pass

    def invalidate(self, email: str, url: str) -> None:
        """
        使特定缓存失效。

        Args:
            email: 用户邮箱
            url: ManageBac URL
        """
        cache_key = self._get_cache_key(email, url)

        # 删除缓存文件
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        if cache_file.exists():
            try:
                cache_file.unlink()
            except OSError:
                pass

        # 从元数据中删除
        if cache_key in self.metadata["entries"]:
            del self.metadata["entries"][cache_key]
            self._save_metadata()

    def clear_all(self) -> None:
        """清除所有缓存。"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
            except OSError:
                pass

        self.metadata = {"entries": {}, "last_cleanup": None}
        self._save_metadata()

    def _cleanup_old_entries(self) -> None:
        """清理过期的缓存条目。"""
        now = datetime.now(timezone.utc)
        to_remove = []

        for cache_key, entry in self.metadata["entries"].items():
            cached_time = datetime.fromisoformat(entry["timestamp"])
            if now - cached_time > self.ttl:
                to_remove.append(cache_key)

        # 删除过期条目
        for cache_key in to_remove:
            cache_file = self.cache_dir / f"{cache_key}.pkl"
            if cache_file.exists():
                try:
                    cache_file.unlink()
                except OSError:
                    pass
            del self.metadata["entries"][cache_key]

        # 如果仍然超过最大数量，删除最旧的
        if len(self.metadata["entries"]) >= self.max_entries:
            sorted_entries = sorted(
                self.metadata["entries"].items(),
                key=lambda x: x[1]["timestamp"],
            )
            to_remove_count = len(sorted_entries) - self.max_entries + 10
            for cache_key, _ in sorted_entries[:to_remove_count]:
                cache_file = self.cache_dir / f"{cache_key}.pkl"
                if cache_file.exists():
                    try:
                        cache_file.unlink()
                    except OSError:
                        pass
                del self.metadata["entries"][cache_key]

        self.metadata["last_cleanup"] = now.isoformat()
        self._save_metadata()

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息。

        Returns:
            包含缓存统计的字典
        """
        return {
            "total_entries": len(self.metadata["entries"]),
            "cache_dir": str(self.cache_dir),
            "ttl_minutes": int(self.ttl.total_seconds() / 60),
            "last_cleanup": self.metadata.get("last_cleanup"),
        }
