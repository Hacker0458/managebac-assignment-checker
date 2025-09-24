#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Performance Optimizer for ManageBac Assignment Checker
ManageBac作业检查器性能优化器
"""

import os
import sys
import time
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

class PerformanceOptimizer:
    """Performance optimization utilities | 性能优化工具"""
    
    def __init__(self):
        self.start_time = time.time()
        self.memory_usage = []
        self.cpu_usage = []
        self.monitoring = False
        
    def start_monitoring(self):
        """Start performance monitoring | 开始性能监控"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_performance, daemon=True)
        self.monitor_thread.start()
        print("📊 Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring | 停止性能监控"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1)
        print("📊 Performance monitoring stopped")
        
    def _monitor_performance(self):
        """Monitor system performance | 监控系统性能"""
        while self.monitoring:
            try:
                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_usage.append({
                    'timestamp': time.time(),
                    'percent': memory.percent,
                    'used': memory.used,
                    'available': memory.available
                })
                
                # CPU usage
                cpu = psutil.cpu_percent(interval=1)
                self.cpu_usage.append({
                    'timestamp': time.time(),
                    'percent': cpu
                })
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                break
                
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report | 获取性能报告"""
        if not self.memory_usage or not self.cpu_usage:
            return {"error": "No performance data available"}
            
        # Calculate averages
        avg_memory = sum(m['percent'] for m in self.memory_usage) / len(self.memory_usage)
        avg_cpu = sum(c['percent'] for c in self.cpu_usage) / len(self.cpu_usage)
        
        # Calculate max values
        max_memory = max(m['percent'] for m in self.memory_usage)
        max_cpu = max(c['percent'] for c in self.cpu_usage)
        
        # Runtime
        runtime = time.time() - self.start_time
        
        return {
            'runtime_seconds': runtime,
            'runtime_formatted': self._format_time(runtime),
            'memory': {
                'average_percent': round(avg_memory, 2),
                'max_percent': max_memory,
                'current_percent': psutil.virtual_memory().percent,
                'total_gb': round(psutil.virtual_memory().total / (1024**3), 2)
            },
            'cpu': {
                'average_percent': round(avg_cpu, 2),
                'max_percent': max_cpu,
                'current_percent': psutil.cpu_percent()
            },
            'recommendations': self._get_recommendations(avg_memory, avg_cpu)
        }
        
    def _format_time(self, seconds: float) -> str:
        """Format time in human readable format | 格式化时间为人类可读格式"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        else:
            return f"{seconds/3600:.1f} hours"
            
    def _get_recommendations(self, avg_memory: float, avg_cpu: float) -> List[str]:
        """Get performance recommendations | 获取性能建议"""
        recommendations = []
        
        if avg_memory > 80:
            recommendations.append("🔴 High memory usage detected. Consider closing other applications.")
            
        if avg_cpu > 80:
            recommendations.append("🔴 High CPU usage detected. Check for background processes.")
            
        if avg_memory > 60 and avg_cpu > 60:
            recommendations.append("⚠️ System under stress. Consider optimizing application settings.")
            
        if not recommendations:
            recommendations.append("✅ Performance is within normal ranges.")
            
        return recommendations
        
    def optimize_memory(self):
        """Optimize memory usage | 优化内存使用"""
        try:
            import gc
            gc.collect()
            print("🧹 Memory garbage collection completed")
            return True
        except Exception as e:
            print(f"❌ Memory optimization failed: {e}")
            return False
            
    def optimize_cache(self, cache_dir: str = "cache"):
        """Optimize cache directory | 优化缓存目录"""
        try:
            cache_path = Path(cache_dir)
            if not cache_path.exists():
                return True
                
            # Remove old cache files (older than 7 days)
            import time
            current_time = time.time()
            removed_count = 0
            
            for file_path in cache_path.rglob("*"):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > 7 * 24 * 3600:  # 7 days
                        file_path.unlink()
                        removed_count += 1
                        
            print(f"🧹 Removed {removed_count} old cache files")
            return True
            
        except Exception as e:
            print(f"❌ Cache optimization failed: {e}")
            return False
            
    def optimize_logs(self, logs_dir: str = "logs"):
        """Optimize log files | 优化日志文件"""
        try:
            logs_path = Path(logs_dir)
            if not logs_path.exists():
                return True
                
            # Compress old log files
            import gzip
            compressed_count = 0
            
            for log_file in logs_path.glob("*.log"):
                if log_file.stat().st_size > 1024 * 1024:  # > 1MB
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(f"{log_file}.gz", 'wb') as f_out:
                            f_out.writelines(f_in)
                    log_file.unlink()
                    compressed_count += 1
                    
            print(f"📦 Compressed {compressed_count} log files")
            return True
            
        except Exception as e:
            print(f"❌ Log optimization failed: {e}")
            return False
            
    def save_performance_report(self, filename: str = "performance_report.json"):
        """Save performance report to file | 保存性能报告到文件"""
        try:
            report = self.get_performance_report()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"📊 Performance report saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save performance report: {e}")
            return False

def main():
    """Main optimization function | 主优化函数"""
    print("🚀 ManageBac Assignment Checker Performance Optimizer")
    print("🚀 ManageBac作业检查器性能优化器")
    print("=" * 60)
    
    optimizer = PerformanceOptimizer()
    
    # Start monitoring
    optimizer.start_monitoring()
    
    try:
        # Run optimizations
        print("\n🔧 Running optimizations...")
        
        # Memory optimization
        print("🧹 Optimizing memory...")
        optimizer.optimize_memory()
        
        # Cache optimization
        print("🗂️ Optimizing cache...")
        optimizer.optimize_cache()
        
        # Log optimization
        print("📝 Optimizing logs...")
        optimizer.optimize_logs()
        
        # Wait a bit for monitoring data
        print("\n⏳ Collecting performance data...")
        time.sleep(10)
        
        # Stop monitoring
        optimizer.stop_monitoring()
        
        # Generate report
        print("\n📊 Performance Report:")
        print("=" * 40)
        report = optimizer.get_performance_report()
        
        if 'error' in report:
            print(f"❌ {report['error']}")
        else:
            print(f"⏱️ Runtime: {report['runtime_formatted']}")
            print(f"💾 Memory: {report['memory']['average_percent']}% avg, {report['memory']['max_percent']}% max")
            print(f"🖥️ CPU: {report['cpu']['average_percent']}% avg, {report['cpu']['max_percent']}% max")
            
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  {rec}")
        
        # Save report
        optimizer.save_performance_report()
        
        print("\n✅ Optimization completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Optimization interrupted by user")
        optimizer.stop_monitoring()
    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        optimizer.stop_monitoring()

if __name__ == "__main__":
    main()
