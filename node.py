import random
from message import Message


class Node(object):

    ############## CONSTRUCTOR ##############
    def __init__(self, env, pipe, id):
        self.env = env
        self.id = id
        self.messages = []
        self.pipe = pipe
        self.next, self.prev = None, None
        self.action = env.process(self.run())

    ############## SETTERS ##############
    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev

    ############## ADD NODES TO DHT ##############
    def join(self, nodes):
        self.find(nodes)
        # yield self.env.process(self.find(nodes)) #waiting for the node to be insert in the network

    def find(self, nodes):
        print(f'[{self.env.now}][{self.id}][SEARCHING CONTACT]')
        contact = nodes[random.randint(0, len(nodes) - 1)]
        init = contact.id
        lap_complete = False
        contact = contact.next
        print(f'[{self.env.now}][{self.id}][TRYING TO JOIN] {contact.id}')
        while contact.id >= self.id or self.id >= contact.next.id:
            if contact.id == init:
                lap_complete = True
            if contact.id >= contact.next.id and lap_complete:
                break
            else:
                contact = contact.next
            print(f'[{self.env.now}][{self.id}][TRYING TO JOIN] {contact.id}')
        print(f'[{self.env.now}][{self.id}][CONTACT FOUND] {contact.id}')
        self.insert(contact)
        # yield self.env.process(self.insert(contact))

    def insert(self, contact):
        self.send(self.pipe, contact, 'INSERT')

    def send(self, pipe, to, content):
        # put to.prev in parameters
        self.env.process(self.message_generator(
            to, self, content, self.env, pipe))
        self.env.process(to.receive(self.env, pipe))
        print(f'[{self.env.now}][{self.id}][SEND {content}] {self.id} --> {to.id}')

    def message_generator(self, to_, from_, content, env, pipe):
        yield env.timeout(random.randint(6, 10))
        msg = Message(to_, from_, content, env)
        pipe.put(msg)

    def receive(self, env, pipe):
        msg = yield pipe.get()
        self.messages.append(msg)
        print(
            f'[{self.env.now}][{self.id}][RECEIVE {msg.content}] {msg.from_node.id} --> {msg.to_node.id}')
        yield env.timeout(random.randint(4, 8))

    ############## MESSAGES MANAGEMENT ##############
    def run(self):
        while True:
            if len(self.messages) != 0:
                msg = self.messages[-1]
                if msg.content == 'INSERT':
                    msg.from_node.set_next(self.next)
                    msg.from_node.set_prev(self)
                    self.next.set_prev(msg.from_node)
                    self.set_next(msg.from_node)

                    self.messages.pop()
                    yield self.env.timeout(random.randint(4, 8))
                else:
                    yield self.env.timeout(random.randint(4, 8))
            else:
                yield self.env.timeout(random.randint(4, 8))
