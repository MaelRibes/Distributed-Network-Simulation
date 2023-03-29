import random
from message import Message


class Node(object):

    ############## CONSTRUCTOR ##############
    def __init__(self, env, pipe, id):
        self.env = env
        self.id = id
        self.messages = []
        self.pipe = pipe
        self.next, self.prev = self, self
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
        self.send(self.pipe, contact, 'INSERT')
        # yield self.env.process(self.insert(contact))

    def insert(self, from_node):
        from_node.set_next(self.next)
        from_node.set_prev(self)
        self.next.set_prev(from_node)
        self.set_next(from_node)

    def leave(self):
        self.send(self.pipe, self.prev, 'LEAVE', ("next", self.next))
        self.send(self.pipe, self.next, 'LEAVE', ("prev", self.prev))
        self.set_prev(self)
        self.set_next(self)

    ############## MESSAGES MANAGEMENT ##############

    def message_generator(self, to_, from_, content, env, pipe, data):
        yield env.timeout(random.randint(1, 4))
        msg = Message(to_, from_, content, env, data)
        pipe.put(msg)
        print(f'[{self.env.now}][{self.id}][SEND {content}] {self.id} --> {to_.id}')

    def send(self, pipe, to, content, data=None):
        self.env.process(self.message_generator(to, self, content, self.env, pipe, data))
        self.env.process(to.receive(self.env, pipe))
        

    def receive(self, env, pipe):
        msg = yield pipe.get()
        yield env.timeout(random.randint(1, 4))
        self.messages.append(msg)
        print(f'[{self.env.now}][{self.id}][RECEIVE {msg.content}] {msg.from_node.id} --> {msg.to_node.id}')
        
        

    ############## RUN ENVIRONMENT ##############
    def run(self):
        while True:
            if len(self.messages) != 0:
                msg = self.messages[-1]
                if msg.content == 'INSERT':
                    self.insert(msg.from_node)
                    self.messages.pop()
                    yield self.env.timeout(5)
                elif msg.content == 'LEAVE':
                    if msg.data[0] == "prev":
                        self.set_prev(msg.data[1])
                    else:
                        self.set_next(msg.data[1])
                    self.messages.pop()
                    yield self.env.timeout(5)
                else:
                    yield self.env.timeout(5)
            else:
                yield self.env.timeout(5)
