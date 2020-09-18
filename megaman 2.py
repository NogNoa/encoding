from string import ascii_uppercase


def num_pentise(number: int):
    """format: (0 - 24)
    returns the place in a five by five table of a dot.
     pent values goes from A1 to E5"""
    back: str = ascii_uppercase[number // 5] + str(number % 5 + 1)
    return pent(back)


class pent:
    def __init__(self, call: str):
        """format: (A-E)(1-5)"""
        self.val = call

    def pent_numerise(self):
        call = self.val
        Row: str = call[0]
        col: str = call[1]
        number: int = (ascii_uppercase.index(Row)) * 5 + int(col) - 1
        return number


class pent_list:
    """ format: 9*((A-E)(1-5)
    a list of pent values"""

    def __init__(self, table: str):
        # table has to be 9 pent values with spaces!
        self.val: list = table.split()

    def pent_objectify(self):
        back = self.val
        for pl in enumerate(back):
            back[pl[0]] = pent(pl[1])
        return back


class state_bin:
    """ format: 11*(0-1)
    8bits for bosses,3 for Etanks"""

    def __init__(self, call: int):
        if call > 2047:
            raise ValueError(f'state value {call}, {bin(call)} is larger than 11bits')
        self.val = call

    def state_variablise(self):
        boss = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            back: int = self.val & 2**i
            back = bool(back)
            boss[i] = back
        etank = self.val // 2**8
        return state_var(boss, etank)


class state_var:
    """format: [8*(bool)], (0-4)"""
    def __init__(self, boss, etank):
        self.boss, self.etank = boss, etank

    def inventorise(self):
        def mask(char, cond):
            if cond:
                return char
            else:
                return ' '
        b = self.boss
        back  = 'P'  + mask('B', b[0]) + mask('A', b[1]) + mask('Q', b[2])
        back += '\n' + mask('H', b[3]) + mask('W', b[4]) + mask('M', b[5]) + mask('F', b[6])
        back += '\n' + mask('C', b[7]) + mask('1', b[3]) + mask('2', b[1]) + mask('3', b[6])
        return back

    def genpassword(self):
        Boss_Ante = pent_list("C3 D2 C4 D5 B5 E1 E4 E2")  # pre-win values
        Boss_Post = pent_list("D1 E3 B4 B2 D3 E5 C1 C5")  # post-win values
        pswd = []
        for pl in enumerate(self.boss):
            i = pl[0]
            cond = pl[1]
            if cond:
                back = Boss_Post[i]
            else:
                back = Boss_Ante[i]
            back = back.pent_numerise() + self.etank
            # if we reach E5 which is 24 (4*5 +5 -1) the next should be B1 = 10 (2*5 + 1 - 1)
            # instead of 25. So 15 less. Thw A row is actually kept for the Etanks count itself.
            back -= 15*(back > 24)
            pswd += back
        pswd += self.etank.num_pentise()
        return pswd











def genpassword(Etank, bossbin):
    for i in range(8):
        bs = Boss_Ante.val[i]
        win = bossbin & (2 ** i)
        if win:
            bs = Boss_Post.val[i]
        bs = pent(bs).pent_numerise()
        bs += Etank
        bs = num_pentise(bs)
        Boss_Ante.val[i] = bs
    Password: list = [num_pentise(Etank)] + Boss_Ante.val
    return Password







if __name__ == "__main__":
    """"jack = (genpassword(0, 255))
    for i in jack:
        print(i.val)"""
    bill = pent_list("C3 D5 D2 B5 C4 E4 E2 E1")
    bill.pent_objectify()
    print(bill.val[2].val)
    print(state_bin(2048).state_variablise())


# TODO:File interface; console interface; print to table, mention input format in function name.
