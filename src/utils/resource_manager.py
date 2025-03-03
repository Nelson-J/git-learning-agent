import os
import psutil
import logging
from typing import Dict
from threading import Lock

class ResourceManager:
    def __init__(self):
        self.memory_threshold = 0.85  # 85% memory usage threshold
        self.cpu_threshold = 0.90  # 90% CPU usage threshold
        self._cache = {}
        self._cache_lock = Lock()
        self.logger = logging.getLogger(__name__)

    def monitor_resources(self) -> Dict[str, float]:
        """Monitor system resource usage."""
        process = psutil.Process(os.getpid())
        return {
            'memory_percent': process.memory_percent(),
            'cpu_percent': process.cpu_percent(),
            'memory_warning': process.memory_percent() > self.memory_threshold,
            'cpu_warning': process.cpu_percent() > self.cpu_threshold
        }

    def optimize_cache(self):
        """Optimize cache usage based on memory consumption."""
        if psutil.virtual_memory().percent > self.memory_threshold:
            with self._cache_lock:
                self._cache.clear()
                self.logger.warning("Cache cleared due to high memory usage")

    def manage_resources(self):
        """Manage system resources and optimize performance."""
        metrics = self.monitor_resources()
        
        if metrics['memory_warning']:
            self.optimize_cache()
            self.logger.warning("High memory usage detected - cache optimized")
            
        if metrics['cpu_warning']:
            self.logger.warning("High CPU usage detected")
            return False
            
        return True
