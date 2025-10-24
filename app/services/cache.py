import time
from typing import Any, Optional

class SimpleCache:
    def __init__(self, ttl: int = 3600):
        self._data: dict[str, tuple[Any, float]] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        item = self._data.get(key)
        if not item: return None
        val, ts = item
        if time.time() - ts > self.ttl:
            self._data.pop(key, None)
            return None
        return val

    def set(self, key: str, value: Any) -> None:
        self._data[key] = (value, time.time())

    def clear(self) -> None:
        self._data.clear()
