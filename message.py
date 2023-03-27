import simpy

class Message():
    def __init__(self, to_, from_, content, env):
        self.to_node = to_
        self.from_node = from_
        self.content = content
        self.date = env.now