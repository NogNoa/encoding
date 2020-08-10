"""Bacon’s Code
Bacon used a naïve binary system to encode the alphabeth. This was 24 rather than 26 letters as IJ and UV were combined.
So each letter was represented by it’s ordinal from 0 to 23,
in 5-bit binary (00000 to 10111) (it was big endian like hindu-arabic numerals ←)
Instead of 0 and 1 he used ‘a’ and ‘b’ but this was only for discussing the system.
The actual encoding was done by a pair of fonts.
And than a false messege was written in them to encode the real messege (which was obviously 5 times shorter)
"""

from string import ascii_lowercase

order = ascii_lowercase.replace('j', '').replace('v', '')

"""Packet Objects: Equivalent to a letter of the True Massage or 5-bit"""


class letter:
    """format:1*(a-z).exclude(j,v)"""

    def __init__(self, letter: str):
        letter = letter.lower()
        if letter == 'j':
            letter = 'i'
        if letter == 'v':
            letter = 'u'
        self.val = letter

    def ordinise(self):
        return ordinal(order.index(self.val))

    def abbinise(self):
        return self.ordinise().abbinise()


class ordinal:
    """Format:(0-23)"""

    def __init__(self, ordinal: int):
        self.val = ordinal
        self.bin = bin(ordinal)

    def letterise(self):
        return letter(order[self.val])

    def abbinise(self):
        strbin = str(self.bin)[2:]
        strab = ''
        for b in strbin:
            if b == '0':
                strab += 'a'
            else:
                strab += 'b'
        return abbin(strab)


class abbin:
    """format:5*(a,b)
    ab-binary"""

    def __init__(self, abbin: str):
        dif = 5 - len(abbin)
        abbin = dif * 'a' + abbin
        # we always want to have 5 bits
        self.val = abbin

    def ordinise(self):
        strbin = ''
        for b in self.val:
            if b == 'a':
                strbin += '0'
            elif b == 'b':
                strbin += '1'
            else:
                print('That\'s weird. I didn\'t expect any', b, 'in a&b binary', self.val, '.')
        return ordinal(int(strbin, 2))

    def letterise(self):
        return self.ordinise().letterise()

    def falsify(self, key_packet: str):
        back = ''
        for char in key_packet:
            if char in ascii_lowercase:
                if self.val[0] == 'a':
                    char = char.lower()
                elif self.val[0] == 'b':
                    char = char.upper()
                else:
                    print('That\'s weird. I didn\'t expect any', self.val[0], 'in a&b binary', self.val, '.')
                self.val = self.val[1:]
            back += char          
        return false_packet(back)


class false_packet:
    """format:5*(a-z,A-Z)"""

    def __init__(self, string: str):
        self.val = string

    def abbinise(self):
        back = ''
        for l in self.val:
            if l in ascii_lowercase:
                back += 'a'
            else:
                back += 'b'
        return abbin(back)

"""Full Objects: Equivalent to the whole of the true message"""

def listise(object,message: str):


class true_message:
    """format:free.exclude(A-Z)"""

    def __init__(self, text: str):
        self.val = text.lower()

    def list_abbinise(self):
        back = []
        for l in self.val:
            if l in ascii_lowercase:
                l = letter(l).abbinise()
                back.append(l)
        return abbin_list(back)


class abbin_list:
    """format: [abbin]
    exposed format: [5*(a,b)]"""

    def __init__(self, call: list):
        self.val = call

    def textualise(self):
        back = ''
        for l in self.val:
            l = l.letterise()
            back += l.val
        return true_message(back)

    def expose(self):
        back = []
        for l in self.val:
            back.append(l.val)
        return back

    def flasify(self, key_list : list):
        back = ''
        key_list = key_list.val
        for i in enumerate(self.val):
            l = i[1]
            key_packet = key_list[i[0]]
            back += l.falsify(key_packet).val
        return false_messege(back)


class key_list:
    """format:[free]"""

    def __init__(self, key_message: str):
        back = []
        key_message = key_message.lower()
        while key_message:
            letter_index = -1
            for c in enumerate(key_message):
                char = c[1]
                if char in ascii_lowercase:
                    letter_index += 1
                    if letter_index >= 4:
                        break
            char_index = c[0] + 1
            back.append(key_message[:char_index])
            key_message = key_message[char_index:]
        self.val = back


class false_messege:
    """format:free"""
    
    def __init__(self, text: str):
        self.val = text
        
    def abbinize(self):


if __name__ == "__main__":
    """
    Joe = letter('J')
    print(Joe.val)
    print(Joe.ordinise().val)
    print(ordinal(4).letterise().val)
    Joe = Joe.abbinise()
    print(Joe.val)
    print(Joe.letterise().val)
    print(Joe.falsify('Letsgo'))
    
    jack = ''
    
    for l in "Tolkien":
        l = letter(l)
        l = l.abbinise()
        jack += l.val + ' '
    print(jack)
    """
    jack = true_message('Tolkien')
    jim = jack.list_abbinise()
    print(jim)
    print(jim.textualise().val)
    print(jim.expose())
    lock = key_list("So, here is our first 12 example of a slice: 2:7. The full slice syntax is: start:stop:step. ")
    print(lock.val)
    print(jim.flasify(lock))
