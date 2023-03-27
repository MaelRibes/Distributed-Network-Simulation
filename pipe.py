import simpy
import random
from message import Message

class Pipe(object):
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env

    def message_generator(to, content, env, pipe):
        while True:
            yield env.timeout(random.randint(6, 10))
            msg = Message(to, content, env)
            pipe.put(msg)

    def message_consumer(name, env, pipe):
        while True:
            msg = yield pipe.get()
            print('LATE Getting Message: at time %d: %s received message: %s' % (env.now, name, msg[1]))
            yield env.timeout(random.randint(4, 8))