import time
import functools
from typing import Dict, Any, Callable
from collections import defaultdict
import cProfile
import io
import pstats

class PerformanceMonitor:
    def __init__(self):
        self._metrics = defaultdict(list)
        self._profiler = cProfile.Profile()

    def measure_time(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            self._metrics[func.__name__].append(duration)
            return result
        return wrapper

    def profile_function(self, func: Callable) -> str:
        """Profile a function and return stats as string."""
        pr = cProfile.Profile()
        pr.enable()
        func()
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        return s.getvalue()

    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get performance metrics for monitored functions."""
        metrics = {}
        for func_name, times in self._metrics.items():
            metrics[func_name] = {
                'avg_time': sum(times) / len(times),
                'min_time': min(times),
                'max_time': max(times),
                'total_calls': len(times)
            }
        return metrics

    def reset_metrics(self):
        """Reset all collected metrics."""
        self._metrics.clear()


class PerformanceMetrics:
    def __init__(self):
        self.metrics = {}

    def track_metric(self, name: str, value: float):
        self.metrics[name] = value
