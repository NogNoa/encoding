from string import ascii_uppercase


def penta(number: int):
    """returns the place in a five by five table of a dot.
       pent values goes from A1 to E5"""
    pent: str = ascii_uppercase[number // 5] + str(number % 5 + 1)
    return pent


def unpenta(pent: str):
    Row: str = pent[0]
    col: str = pent[1]
    number: int = (ascii_uppercase.index(Row)) * 5 + int(col) - 1
    return number


class pental:
    """a list of pent values"""

    def __init__(self, table: str) -> list:
        # table has to be 9 pent values with spaces!
        self.pental: list = table.split()


def genpassword(Etank, bossbin):
    Boss = pental("C3 D5 D2 B5 C4 E4 E2 E1")  # pre-win values
    Bossw = pental("D1 B2 E3 D3 B4 C1 C5 E5")  # post-win values
    for i in range(8):
        bs = Boss.pental[i]
        win = bossbin & (2 ** i)
        if win:
            bs = Bossw.pental[i]
        bs = unpenta(bs)
        bs += Etank
        bs = penta(bs)
        Boss.pental[i] = bs
    Password: list = [penta(Etank)] + Boss.pental
    return Password


print(genpassword(0, 255))
