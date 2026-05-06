from collections import OrderedDict
from threading import Lock


class LRUCache:
    """In-memory LRU cache. Thread-safe via lock."""

    def __init__(self, max_size: int = 512):
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._lock = Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            self._cache.move_to_end(key)
            self.hits += 1
            return self._cache[key]

    def set(self, key: str, value) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self._max_size:
                    self._cache.popitem(last=False)
            self._cache[key] = value

    def __len__(self) -> int:
        return len(self._cache)

    def stats(self) -> dict:
        total = self.hits + self.misses
        rate = round(self.hits / total, 3) if total else 0.0
        return {"size": len(self), "hits": self.hits, "misses": self.misses, "hit_rate": rate}
