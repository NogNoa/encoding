"""Bacon’s Code
Bacon used a naïve binary system to encode the alphabeth. This was 24 rather than 26 letters as IJ and UV were combined.
So each letter was represented by it’s ordinal from 0 to 23,
in 5-bit binary (00000 to 10111) (it was big endian like hindu-arabic numerals ←)
Instead of 0 and 1 he used ‘a’ and ‘b’ but this was only for discussing the system.
The actual encoding was done by a pair of fonts.
And than a false messege was written in them to encode the real messege (which was obviously 5 times shorter)
"""

from string import ascii_lowercase, ascii_uppercase, ascii_letters

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
            if char in ascii_letters:
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
            elif l in ascii_uppercase:
                back += 'b'
        return abbin(back)

"""Full Objects: Equivalent to the whole of the true message"""

def listise(message: str):
    back = []
    while message:
        letter_index = -1
        for c in enumerate(message):
            char = c[1]
            if char in ascii_letters:
                letter_index += 1
                if letter_index >= 4:
                    break
        char_index = c[0] + 1
        back.append(message[:char_index])
        message = message[char_index:]
    return back


class true_message:
    """format:free.exclude(A-Z)"""

    def __init__(self, text: str):
        self.val = text

    def list_abbinise(self):
        back = []
        for l in self.val:
            if l in ascii_letters:
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
        for packet in self.val:
            back.append(packet.val)
        return back

    def falsify(self, key_message : str):
        back = ''
        key_list = listise(key_message)
        for i in enumerate(self.val):
            l = i[1]
            key_packet = key_list[i[0]]
            back += l.falsify(key_packet).val
        return false_message(back)


class false_message:
    """format:free"""
    
    def __init__(self, text: str):
        self.val = text
        
    def abbinise(self):
        back = []
        false_list = listise(self.val)
        for packet in false_list:
            packet = false_packet(packet)
            packet = packet.abbinise()
            back.append(packet)
        return abbin_list(back)


"""Main Functions"""

def Bacon(true: str, key_message: str):
    true = true_message(true)
    back = true.list_abbinise().falsify(key_message)
    print(back.val)
    return back


def decipher(false:str):
    false = false_message(false)
    back = false.abbinise().textualise()
    print(back.val)
    return back



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
    lock = "So, here is our first 12 example of a slice: 2:7. The full slice syntax is: start:stop:step. "
    joe = jim.falsify(lock)
    print(joe.abbinise().expose())

"""not TODO: Unite true message and false message. Since true message would inevitibely lose Case information, and 
false message has non-standard Case formating they are not really compatible. And recursive encoding wouldn't really be 
fruitfull"""
