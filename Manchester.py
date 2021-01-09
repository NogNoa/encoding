class Clock:
    def __init__(self):
        self.val = 0

    def tick(self):
        self.val = not self.val


class Data:
    def __init__(self, call: int):
        self.val = bin(call)[2:]
        self.pl = 0

    def tick(self):
        if self.pl >= len(self.val):
            back = -1
        else:
            back = self.val[self.pl]
        if not clock.val:
            self.pl += 1
        return back


def manchester(call):
    if call == -1:
        return -1
    return int(call) ^ clock.val





clock = Clock()
data = Data(11)


def mantick():
    clock.tick()
    signal = data.tick()
    signal = manchester(signal)
    print(signal)



for i in range(8):
    mantick()
