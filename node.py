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
        self.blocked = False

    ############## SETTERS ##############
    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev

    def set_blocked(self, boolean):
        self.blocked = boolean

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


    ############## MESSAGES MANAGEMENT ##############
    
    def message_generator(self, to_, from_, content, env, pipe):
        yield env.timeout(random.randint(6, 10))
        msg = Message(to_, from_, content, env)
        pipe.put(msg)

    def send(self, pipe, to, content):
        self.env.process(self.message_generator(to, self, content, self.env, pipe))
        print(f'[{self.env.now}][{self.id}][SEND {content}] {self.id} --> {to.id}')
        self.env.process(to.receive(pipe))
        

    def receive(self,  pipe):
        msg = yield pipe.get()
        self.messages.append(msg)
        print(
            f'[{self.env.now}][{self.id}][RECEIVE {msg.content}] {msg.from_node.id} --> {msg.to_node.id}')
        yield self.env.timeout(random.randint(4, 8))
        
    def padlock(self, pipe, origin, content):
        if self.next.id == origin.id:
            return True
        else:
            self.send(pipe, self.next, content)
            return self.next.padlock(pipe, origin, content)
        
    ############## RUN ENVIRONMENT ##############
    
    def run(self):
        while True:
            if len(self.messages) != 0:
                msg = self.messages[-1]
                if msg.content == 'INSERT':
                    self.set_blocked(True)
                    self.padlock(self.pipe, self, 'LOCK')
                    self.insert(msg.from_node)
                    self.padlock(self.pipe, self, 'UNLOCK')
                    self.messages.pop()
                    yield self.env.timeout(random.randint(4, 8))
                elif msg.content == 'LOCK':
                    self.set_blocked(True)
                    self.messages.pop()
                    yield self.env.timeout(random.randint(4, 8))
                elif msg.content == 'UNLOCK':
                    self.set_blocked(False)
                    self.messages.pop()
                    yield self.env.timeout(random.randint(4, 8))
                else:
                    yield self.env.timeout(random.randint(4, 8))
            else:
                yield self.env.timeout(random.randint(4, 8))
