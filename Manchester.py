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
    return format(call, 'b')


class Clock:
    def __init__(self):
        self.val = 0

    def tick(self):
        self.val = not self.val

    def __str__(self):
        if self.val:
            return "Tick"
        else:
            return "Tock"

    def __repr__(self):
        return self.val


class Data:
    def __init__(self, call: int = None):
        if call is None:
            self.val = ''
        else:
            self.val = call

    def tick(self, clock):
        bn_val = binarise(self.val)
        try:
            back = bn_val[-1]
            back = int(back)
        except IndexError:
            back = None
        if not clock.val:
            bn_val = bn_val[:-1]  # delete last char every time clock is 0
            self.val = int('0b' + bn_val)
        return back

    def append(self, call):
        back = binarise(call) + binarise(self.val)
        self.val = int('0b' + back)


class Transmitter:

    def __init__(self):
        self.clock = Clock()
        self.data = Data()

    def load(self, msg: int):
        self.data.append(msg)

    def tick(self):
        self.clock.tick()
        signal = self.data.tick(self.clock)
        signal = manchester(signal, self.clock)
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
            msg = manchester(signal, self.clock)
            if msg == self.prev:
                self.retrii = 0
                return msg
            else:
                self.retrii += 1
                if self.retrii == 3:
                    stderr.write(str(msg) * 4)
                    exit()
                self.tick(signal)


def manchester(signal, clock):
    if signal is None:
        back = 0
    else:
        back = signal ^ clock.val
    return back


if __name__ == "__main__":
    transmitter = Transmitter()
    transmitter.load(11)
    receiver = Reciever()
    out = ''

    for i in range(8):
        sign = transmitter.tick()
        sign = receiver.tick(sign)
        if sign is not None:
            out += str(sign)
    print(out)

#
# Done: get data in transmitter
# change -1 to 00 and make receiver being able to interpret 0000 as end of transmission.
