# -*- coding: utf-8 -*-

from string import ascii_lowercase, ascii_uppercase, ascii_letters

"""
Created on Sat Aug 31 19:47:07 2019
@author: omer Navon
"""

"""Bacon’s Code
Bacon used a naïve binary system to encode the alphabeth. This was 24 rather than 26 letters as IJ and UV were combined.
So each letter was represented by it’s ordinal from 0 to 23,
in 5-bit binary (00000 to 10111) (it was big endian like hindu-arabic numerals ←)
Instead of 0 and 1 he used ‘a’ and ‘b’ but this was only for discussing the system.
The actual encoding was done by a pair of fonts.
And than a false messege was written in them to encode the real messege (which was obviously 5 times shorter)
"""

order = ascii_lowercase.replace('j', '').replace('v', '')

"""all Packet Objects are Equivalent to a letter of the True Massage or 5-bit"""


class Letter:
    """format:1*(a-z).exclude(j,v)"""

    def __init__(self, letter: str):
        letter = letter.lower()
        if letter == 'j':
            letter = 'i'
        if letter == 'v':
            letter = 'u'
        self.val = letter

    def __str__(self):
        return self.val

    def ordinise(self):
        return Ordinal(order.index(self.val))

    def abbinise(self):
        return self.ordinise().abbinise()


class Ordinal:
    """Format:(0-23)"""

    def __init__(self, ordinal: int):
        self.val = ordinal

    def __int__(self):
        return self.val

    def letterise(self):
        return Letter(order[self.val])

    def abbinise(self):
        strbin = format(self.val, 'b')  # sans 0b prefix
        strab = ''
        for b in strbin:
            if b == '0':
                strab += 'a'
            else:
                strab += 'b'
        return abBin(strab)


class abBin:
    """format:5*(a,b)
    ab-binary"""

    def __init__(self, abbin: str):
        # we always want to have 5 bits
        # negative difs will be queitly treated as 0
        dif = 5 - len(abbin)
        abbin = dif * 'a' + abbin
        self.val = abbin

    def __str__(self):
        return self.val

    def ordinise(self):
        strbin = ''
        for b in self.val:
            if b == 'a':
                strbin += '0'
            elif b == 'b':
                strbin += '1'
            else:
                print(f'That\'s weird. I didn\'t expect any {b} in a&b binary {self.val}.')
        return Ordinal(int(strbin, 2))

    def letterise(self):
        return self.ordinise().letterise()

    def falsify(self, key_packet: str):
        back = ''
        for char in key_packet:
            if char in ascii_letters:
                if self.val[0] == 'a':
                    char = char.lower()
                elif self.val[0] == 'b':
                    char = char.upper()
                else:
                    print(f'That\'s weird. I didn\'t expect any {self.val[0]} in a&b binary {self.val}.')
                self.val = self.val[1:]
            back += char
        return FalsePacket(back)


class FalsePacket:
    """format:5*(a-z,A-Z)"""

    def __init__(self, string: str):
        self.val = string

    def __str__(self):
        return self.val

    def abbinise(self):
        back = ''
        for ltr in self.val:
            if ltr in ascii_lowercase:
                back += 'a'
            elif ltr in ascii_uppercase:
                back += 'b'
        return abBin(back)


"""Full Objects: Equivalent to the whole of the true message"""


def listise(message: str):
    back = []
    while message:
        letter_index = -1
        for pl, val in enumerate(message):
            char = val
            if char in ascii_letters:
                letter_index += 1
                if letter_index >= 4:
                    char_index = pl + 1
                    break
        else:
            char_index = len(message)
        back.append(message[:char_index])
        message = message[char_index:]
    return back


class TrueMessage:
    """format:free.exclude(A-Z)"""

    def __init__(self, text: str):
        self.val = text

    def __str__(self):
        return self.val

    def list_abbinise(self):
        back = []
        for ltr in self.val:
            if ltr in ascii_letters:
                ltr = Letter(ltr).abbinise()
                back.append(ltr)
        return abBinList(back)


class abBinList:
    """format: [abbin]
    exposed format: [5*(a,b)]"""

    def __init__(self, call: list):
        self.val = call

    def __str__(self):
        return str(self.expose())

    def textualise(self):
        back = ''
        for abbin in self.val:
            abbin = abbin.letterise()
            back += abbin.val
        return TrueMessage(back)

    def expose(self):
        back = []
        for packet in self.val:
            back.append(packet.val)
        return back

    def falsify(self, key_message: str):
        back = ''
        key_list = listise(key_message)
        for pl, abbin in enumerate(self.val):
            key_packet = key_list[pl]
            back += abbin.falsify(key_packet).val
        return FalseMessage(back)


class FalseMessage:
    """format:free"""

    def __init__(self, text: str):
        self.val = text

    def __str__(self):
        return self.val

    def list_abbinise(self):
        back = []
        false_list = listise(self.val)
        for packet in false_list:
            packet = FalsePacket(packet)
            packet = packet.abbinise()
            back.append(packet)
        return abBinList(back)


"""Main Functions"""


def expose(call):
    if type(call) is not str:
        call = call.val
    return call


def bacon(true, key):
    if type(true) is str:
        true = TrueMessage(true)
    key = expose(key)
    back = true.list_abbinise().falsify(key)
    print(back.val)
    return back


def decipher(false):
    if type(false) is str:
        false = FalseMessage(false)
    back = false.list_abbinise().textualise()
    print(back.val)
    return back


"""file interface"""


def load_file(file):
    return open(file, 'r').read()


def save_file(file, message):
    open(file, 'w+').write(message)


def bacon_file(true, key, false='false-message.txt'):
    true = load_file(true)
    key = load_file(key)
    back = TrueMessage(true).list_abbinise().falsify(key)
    save_file(false, str(back))
    return back


def decipher_file(false, true='true-message.txt'):
    false = load_file(false)
    back = FalseMessage(false).list_abbinise().textualise()
    save_file(true, str(back))
    return back


if __name__ == "__main__":
    """
    Joe = Letter('J')
    print(Joe.val)
    print(Joe.ordinise().val)
    print(Ordinal(4).letterise().val)
    Joe = Joe.abbinise()
    print(Joe.val)
    print(Joe.letterise().val)
    print(Joe.falsify('Letsg'))

    jack = ''

    for l in "Tolkien":
        l = Letter(l)
        l = l.abbinise()
        jack += l.val + ' '
    print(jack)
    """
    jack = TrueMessage('Tolkien')
    jim = jack.list_abbinise()
    print(jim)
    print(jim.textualise().val)
    print(jim.expose())
    lock = "So, here is our first 12 example of a slice: 2:7. The full slice syntax is: start:stop:step. "
    joe = jim.falsify(lock)
    print(joe.list_abbinise().expose())

    joe = bacon('Tolkien', lock)
    Jay = decipher(joe)
    bacon_file("README.md", "english.txt")
    decipher_file('false-message.txt')

#  maybe rewrite listise?
#
#  Done: is it okey to silently accept too long key_packets? Not really. If a packet longer than 5 got there, something
#  weird've happened.
