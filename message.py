class Message():
    def __init__(self, to_, from_, content, env, data=None):
        self.to_node = to_
        self.from_node = from_
        self.content = content
        self.date = env.now
        self.data = data