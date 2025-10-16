import time

class TTLCache:
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl):
        self.store[key] = (value, time.time() + ttl)

    def get(self, key):
        val = self.store.get(key)
        if not val:
            return None
        v, exp = val
        if time.time() > exp:
            self.store.pop(key, None)
            return None
        return v
