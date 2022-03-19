def binarise(call):
    return format(call, 'b')


class Clock:
    def __init__(self):
        self.val = False

    def tick(self):
        self.val = not self.val

    def __str__(self):
        if self.val:
            return "Tick"
        else:
            return "Tock"


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

    def tick(self, clock):
        try:
            back = int(self.val[-1])
        except IndexError:
            back = False
        if not clock.val:
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

    def tick(self, ):
        self.clock.tick()
        bit = self.fifo.tick(self.clock)
        self.val = bit if bit is not None else False


airwaves = Airwaves()


class Reciever:
    def __init__(self):
        self.clock = Clock()
        self.synched = False
        self.stack = Stack()

    def tick(self):
        self.clock.tick()
        signal = airwaves.val
        if signal is not None:
            self.stack.push(signal)

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
