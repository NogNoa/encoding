"""
Manchester takes a regular bits stream and convert it to a specilied bits stream with double the length

Manchester should give back:

10: if it was given a 0 from the stream
01: if it was given a 1
00: if the stream was emptied and don't give any more bits
11: never

If the receiver gets 00 or 11 it tries to shift it's clock, making one more tick for the transmitter tick.
So if it recieve 001 it wil ignore the first 0, give back a 1, and it's clock will be odd with what it was before.
Similarly if it recieve 0001 it will treat it as if it received 01 and return a 1, one clock cycle was skiped
and it's clock will be even with what it was before.
However if the transmitter receives four of the same bit in a row 0000 or 1111, this program will be shutdown
and it will not see whatever came after.
This is both for halting when the string ends (0000) and when there's a mistake (either 0000 or 1111).

"""

from sys import stderr


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
            back = None
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
        self.prev = 0
        self.retrii = 0

    def tick(self, signal):
        self.clock.tick()
        signal = int(signal)
        if self.clock.val:
            self.prev = manchester(signal, self.clock)
        else:
            val = manchester(signal, self.clock)
            if val == self.prev:
                self.retrii = 0
                return val
            else:
                if self.retrii == 2:
                    # 1st that is the same didn't cause a retry. 2nd and 3rd rised retrii from 0 to 2.
                    # Now it's the forth bit in a row that is the same.
                    stderr.write(str(val)*4)
                    exit()
                else:
                    self.retrii += 1
                self.tick(signal)


def manchester(call, clock):
    if call is None:
        back = 0
    else:
        back = call ^ clock.val
    return back


data = Data(11)
transmitter = Transmitter()

for i in range(8):
    transmitter.tick()

# todo: get data in transmitter
# Done: change -1 to 00 and make receiver being able to interpret 0000 as end of transmision.
