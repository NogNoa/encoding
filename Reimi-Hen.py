Sencii = [" ", "[Blank1]", "[Blank2]", "[Blank3]", "[Sword]", "[light_sword]", "[ring]", "[bracelet]",
          "[Bomerang]", "[Shirt]", "[Mail]", "[Plate]", "[Hide]", "[Dress]", "[garment]", "[Bag]",
          "[Helm]", "[Crown]", 'a', 'd', "or", 'a', "T", "h",
          "or", 'n', " ", "of ", " ", "if", "e", "ti",
          "o", "G", "ro", "u", "p", "D", "ef", "e",
          "nd", "ri", "c", "[Stone]", "[Compass]", "[Pendent]", "vi", "c",
          '0', '1', '2', '3', '4', '5', '6', '7',
          '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
          'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
          'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
          'y', 'z', "ll", 'il', 'li', "'t", "'s", "il",
          "ll", '."', "ll", "i", "'", "'ll", 'F', "ig",
          "h", "t", "'r", "'v", "I'", "m", ": ", "C",
          "la", "w", "[Heart]", "Ka", "is", "e", "r", "la",
          "s", "t", "a", ", ", "ck", "sl", "?", "..",
          "G", "H", "I", "J", "K", "L", "N", "M",
          "O", "P", "Q", "R", "S", "T", "U", "V",
          "W", "X", "Y", "Z", "ee", "p", "S", "w",
          "oo", "n", "'d", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          "", "", "", "", "", "", "", "",
          ]

with open("D:/temp/patching teach/radia100/radia100.ips", mode="rb") as file:
    scroll = bytearray(file.read())
length = 0
codex = []

# state head
if scroll[:5] == b'PATCH':
    del scroll[:5]
else:
    raise IOError

while scroll:
    # state body
    if scroll[:3] == b"EOF":
        break
    else:
        ofsett = scroll[0] * 0x10000 + scroll[1] * 0x100 + scroll[2]
        del scroll[:3]
    # state length
    if scroll[:2] == b'\u0\u0':
        raise ZeroDivisionError
    else:
        length = scroll[0] * 0x100 + scroll[1]
        del scroll[:2]
    # state payload
    codex += [Sencii[b] for b in scroll[:length] if (b == 0 or 0x12 <= b <= 0x9A)]
    del scroll[:length]

codex = ''.join(codex)
with open("D:/temp/patching teach/radia100/radia100-transcript.txt", mode="w+") as file:
    file.write(codex)
