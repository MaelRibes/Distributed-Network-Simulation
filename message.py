class Message():
    def __init__(self, to_, from_, type, env, content=None):
        self.to_node = to_
        self.from_node = from_
        self.type = type
        self.date = env.now
        self.content = content