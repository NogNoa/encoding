from enum import Enum

Sencii = Enum("Sencii",
              [" ", "[Blank1]", "[Blank2]", "[Blank3]", "[Sword]", "[light_sword]", "[ring]", "[bracelet]",
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
               "ll", '."', "ll", "i", "'", "'ll",  'F', "ig",
               "h", "t", "'r", "'v", "I'", "m", ": ", "C",
               "la", "w", "[Heart]", "Ka", "is", "e", "r", "la",
               "s", "t", "a", ", ", "ck", "sl", "?", "..",
               "G", "H", "I", "J", "K", "L", "N", "M",
               "O", "P", "Q", "R", "S", "T", "U", "V",
               "W", "X", "Y", "Z", "ee", "p", "S", "w",
               "oo", "n", "'d"
               ]
              )

with open("D/temp/patching teach/rad-b1/RAD-E.IPS", mode="rb") as file:
    scroll = file.read()

codex = [str(Sencii(b)) for b in scroll]
codex = ''.join(codex)
print(codex)

