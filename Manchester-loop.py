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


class Fifo(Data):

    def append(self, call):
        back = binarise(call) + binarise(self.val)
        self.val = int('0b' + back)


class stack(Data):
    def append(self, call):
        back = binarise(self.val) + binarise(call)
        self.val = int('0b' + back)


class Reciever:
    def __init__(self):
        self.clock = Clock()
        self.synched = False

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
