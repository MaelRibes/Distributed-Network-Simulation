class DHT():
    def __init__(self):
        self.hashmap = {}

    def set(self, key, value):
        self.map[key] = value

    def get(self, key):
        if key in self.map:
            return self.map[key]
        return None