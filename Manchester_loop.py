def binarise(call):
    return format(call, 'b')


class Clock:
    def __init__(self):
        self.val = False

    def tick(self):
        self.val = not self.val

    def __str__(self):
        return ("Tock", "Tick")[self.val]


class Data:
    def __init__(self, call: int = None):
        if call is None:
            self.val = ''
        else:
            self.val = binarise(call)

    def __str__(self):
        return self.val

    def __int__(self):
        return int('0b' + self.val)

    def pull(self, clock_val):
        try:
            back = int(self.val[-1])
        except IndexError:
            back = False
        if not clock_val:
            self.val = self.val[:-1]  # delete last char every time clock is 0
        return back


class Fifo(Data):
    def push(self, call):
        self.val = binarise(call) + self.val


class Stack(Data):
    def push(self, call):
        self.val += binarise(call)


class Airwaves:
    def __init__(self):
        self.clock = Clock()
        self.val = False
        self.fifo = Fifo()

    def push(self, call):
        self.fifo.push(call)

    def tick(self):
        self.clock.tick()
        self.val = self.fifo.pull(self.clock.val)


airwaves = Airwaves()


class Reciever:
    def __init__(self):
        self.clock = Clock()
        self.synched = False
        self.stack = Stack()

    def tick(self):
        self.clock.tick()
        if self.clock.val:
            self.recieve()

    def recieve(self):
        self.stack.push(airwaves.val)

    def loop(self):
        while True:
            while self.synched:
                self.habit()
            else:
                self.improv()

    def habit(self):
        pass

    def improv(self):
        # feat.sleep
        pass


class Transmitter:
    def __init__(self):
        self.clock = Clock()
        self.fifo = Fifo()

    def set(self, msg: int):
        self.fifo.push(msg)

    def tick(self):
        self.clock.tick()
        self.transmit()

    def transmit(self):
        airwaves.push(self.fifo.pull)


rec = Reciever()
trans = Transmitter()

def tick():
    airwaves.tick()
    rec.tick()
    trans.tick()
