def binarise(call):
    if type(call) == int:
        call = bin(call)[2:]
    """
    elif type(call) == str:
        for char in call:
            if char != '0' and char != '1':
                call.replace(char, '')
    """
    return call


class Clock:
    def __init__(self):
        self.val = 0

    def tick(self):
        self.val = not self.val


class Data:
    def __init__(self, call: int):
        self.val = binarise(call)

    def tick(self, clock):
        try:
            back = self.val[-1]
        except IndexError:
            back = -1
        if not clock.val:
            self.val = self.val[:-1]  # delete last char every time clock is 0
        return back

    def append(self, call):
        self.val = binarise(call) + self.val


class Transmitter:

    def __init__(self):
        self.clock = Clock()

    def tick(self):
        self.clock.tick()
        signal = data.tick(self.clock)
        signal = manchester(signal, self.clock)
        print(signal)
        return signal


class Reciever:

    def __init__(self):
        self.clock = Clock()
        self.mem = 0

    def tick(self, signal):
        self.clock.tick()
        signal = int(signal)
        if self.clock.val:
            self.mem = manchester(signal, self.clock)
        else:
            val = manchester(signal, self.clock)
            if val == self.mem:
                return val
            else:
                self.tick(signal)


def manchester(call, clock):
    if call == -1:
        back = call
    else:
        back = call ^ clock.val
    return back


data = Data(11)
transmitter = Transmitter()

for i in range(8):
    transmitter.tick()

# todo: get data in transmitter
# change -1 to 00 and make receiver being able to interpret 0000 as end of transmision.
