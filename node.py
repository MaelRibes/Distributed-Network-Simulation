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
        self.data = {}

    ############## SETTERS ##############
    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev
    
    def add_data(self, key, value):
        self.data[key] = value

    ############## ADD NODES TO DHT ##############
    def join(self, nodes):
        contact = self.find(nodes)
        self.send(self.pipe, contact, 'INSERT')

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
        return contact

    def insert(self, from_node):
        from_node.set_next(self.next)
        from_node.set_prev(self)
        self.next.set_prev(from_node)
        self.set_next(from_node)
        print(f'[{self.env.now}][{self.id}][NODE INSERTED]')

    def leave(self):
        self.send(self.pipe, self.prev, 'LEAVE', ("NEXT", self.next))
        self.send(self.pipe, self.next, 'LEAVE', ("PREV", self.prev))
        self.set_prev(self)
        self.set_next(self)

    def nodes_rearrangement(self, msg):
        if msg.content[0] == "PREV":
            self.set_prev(msg.content[1])
        else:
            self.set_next(msg.content[1])
        print(f'[{self.env.now}][{self.id}][NEIGHBOURS {msg.content[0]} UPDATED] {msg.content[1].id}')


    ############## MESSAGES MANAGEMENT ##############

    def message_generator(self, to_, from_, type, env, pipe, content):
        yield env.timeout(1)
        msg = Message(to_, from_, type, env, content)
        pipe.put(msg)
        print(f'[{self.env.now}][{self.id}][SEND {type}] {self.id} --> {to_.id}')

    def send(self, pipe, to, type, content=None):
        self.env.process(self.message_generator(to, self, type, self.env, pipe, content))
        self.env.process(to.receive(pipe))

    def receive(self, pipe):
        msg = yield pipe.get()
        yield self.env.timeout(random.randint(1, 4))
        self.messages.append(msg)
        print(f'[{self.env.now}][{self.id}][RECEIVE {msg.type}] {msg.from_node.id} --> {msg.to_node.id}')
        

    ############## RUN ENVIRONMENT ##############
    
    def run(self):
        while True:
            if len(self.messages) != 0:
                msg = self.messages[-1]
                if msg.type == 'INSERT':
                    yield self.env.timeout(2)
                    self.insert(msg.from_node)
                    self.messages.pop()
                elif msg.type == 'LEAVE':
                    yield self.env.timeout(1)
                    self.nodes_rearrangement(msg)
                    self.messages.pop()
                else:
                    yield self.env.timeout(5)
            else:
                yield self.env.timeout(1)