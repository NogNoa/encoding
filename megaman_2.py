# -*- coding: utf-8 -*-

from string import ascii_uppercase


def num_pentise(number: int):
    """input format: (0-24)
    returns the place of a dot in a five by five table.
     pent values goes from A1 to E5"""
    back = ascii_uppercase[number // 5] + str(number % 5 + 1)
    return pent(back)


class num_list:
    """format: [9*(0-24)]"""

    def __init__(self, call: list):
        self.val = call

    def num_pentise(self):
        back = [num_pentise(pl).val for pl in self.val]
        return pent_list(back)

    def num_statify(self):
        Boss_Ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
        Boss_Post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values
        number_list = self.val[:9]
        # ^accepting too long inputs but at user's risk as only first 9 items get through
        etank = min(number_list)
        number_list.remove(etank)
        if etank >= 5:
            print("Invalid Password")
            return
            # raise ValueError()
        bosses = [2, 2, 2, 2, 2, 2, 2, 2]

        # 0 or 1 will not be distinguised from boolians. None should also work, it's just more crowding.

        def is_defeated(group, val):
            if boss in group:
                place = group.index(boss)
                bosses[place] = val

        while number_list:
            boss = number_list.pop() - etank
            boss += 20 * (boss < 5)
            # see comment for {boss -= 20 * (boss > 24)} in function stt_numerise
            is_defeated(Boss_Ante, False)
            is_defeated(Boss_Post, True)
        if 2 in bosses:
            print("Invalid Password")
            return
            # raise ValueError()
        return state_var(bosses, etank)


class pent:
    """format: (A-E)(1-5)"""

    def __init__(self, call: str):
        self.val = call

    def pent_numerise(self):
        call = self.val
        Row: str = call[0]
        col: str = call[1]
        number: int = (ascii_uppercase.index(Row)) * 5 + int(col) - 1
        return number


class pent_list:
    """ format: 9*((A-E)(1-5)
    a list of pent values
    """

    def __init__(self, table):
        # table string has to be 9 pent values with spaces!
        # it could be just a list
        if type(table) is not list:
            table: list = table.split()
        self.val = table

    def pent_objectify(self):
        back = [pent(pl) for pl in self.val]
        return back

    def pent_numerise(self):
        back = [pl.pent_numerise() for pl in self.pent_objectify()]
        return num_list(back)

    def make_table(self, file='MM2pswd.csv'):
        lexicon = {
            'A': [0, 0, 0, 0, 0],
            'B': [0, 0, 0, 0, 0],
            'C': [0, 0, 0, 0, 0],
            'D': [0, 0, 0, 0, 0],
            'E': [0, 0, 0, 0, 0],
        }
        for pl in self.val:
            L = pl[0]
            pl = int(pl[1]) - 1
            # ^just translating numeral digit from pent to an integer index in the corresponding list
            lexicon[L][pl] = 1
        back = open(file, 'w+')
        back.write(',1,2,3,4,5\n')
        for i in lexicon:
            line = i + ','
            for j in lexicon[i]:
                line += '\u2022' * j + ','
                # the circle symbol ⬤ is U+2B24
                # the bullet symbol • is U+2022
            line += '\n'
            back.write(line)


class state_bin:
    """ format: 11*(0-1)
    low 8bits for bosses, high 3bits for Etanks"""

    def __init__(self, call: int):
        if call > 2047:
            raise ValueError(f'state value {call}, {bin(call)} is larger than 11bits')
        self.val = call

    def stt_variablise(self):
        bosses = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            back: int = self.val & 2 ** i
            back = bool(back)
            bosses[i] = back
        etank = self.val // 2 ** 8
        return state_var(bosses, etank)

    def save(self, file='mm2.sav'):
        file = open(file, 'w+b')
        back = self.val.to_bytes(2, 'little')
        file.write(back)


class state_var:
    """format: [8*(bool)], (0-4)"""

    def __init__(self, bosses, etank):
        self.bosses, self.etank = bosses, etank

    def inventorise(self):
        def mask(char, cond):
            if cond:
                return char
            else:
                return ' '

        b = self.bosses
        back = 'P' + mask('B', b[0]) + mask('A', b[1]) + mask('Q', b[2])
        back += '\n' + mask('H', b[3]) + mask('W', b[4]) + mask('M', b[5]) + mask('F', b[6])
        back += '\n' + mask('C', b[7]) + mask('1', b[3]) + mask('2', b[1]) + mask('3', b[6])
        return back

    def stt_numerise(self):
        # output format: [8*(0-24), (0-4)]
        Boss_Ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
        Boss_Post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values
        pswd = []
        for pl in enumerate(self.bosses):
            i = pl[0]
            cond = pl[1]
            if cond:
                boss = Boss_Post[i]
            else:
                boss = Boss_Ante[i]
            boss = boss + self.etank
            # if we reach E5 which is 24 (4*5 +5 -1) the next should be B1 = 5 (1*5 + 1 - 1)
            # instead of 25. So 20 less. The A row is actually kept for the Etanks count itself.
            boss -= 20 * (boss > 24)
            pswd += [boss]
        pswd += [self.etank]
        return num_list(pswd)  # as list of 9 numbers

    def stt_binarise(self):
        back = self.etank * 2 ** 8
        for pl in enumerate(self.bosses):
            i = pl[0]
            cond = pl[1]
            back += cond * 2 ** i
        return state_bin(back)


def load_bin(file='mm2.sav'):
    call = open(file, 'r+b')
    call = call.read()
    call = int.from_bytes(call, 'little')
    return state_bin(call)


def table_num_listise(file='MM2pswd.csv'):
    if file[:-4] != '.csv':
        print('Please give me a comma separated table')
        raise ValueError(file)
    call = open(file, 'r+')
    call = call.readlines()
    call = [pl.split(',') for pl in call]
    """
    for i in call:
        i = [pl == '•' for pl in i]
    """
    back = []
    for line in call:
        for pl in range(1, 6):
            if line[pl] == '•':
                num = (call.index(line)) * 5 + pl - 6  # -1 from both the 5s & 1s place
                back.append(num)
    return num_list(back)


if __name__ == "__main__":
    """
    jack = state_bin(1279).stt_variablise().stt_numerise()
    jack = jack.num_statify().stt_binarise()
    print(jack.val)
    jack.save()

    for a in jack:
        print(a)
    bill = pent_list(['D1', 'E3', 'B4', 'B2', 'D3', 'E5', 'C1', 'C5']).pent_objectify()
    jill = []
    for a in bill:
        jill += [a.pent_numerise()]
    print(jill)
    """
    bill = pent_list(['D4', 'B1', 'C2', 'B5', 'E1', 'B3', 'C4', 'D3', 'A4'])
    bill.make_table()
    bill = bill.pent_numerise()
    print(bill.val)
    bill = bill.num_statify()
    print(bill.bosses, bill.etank)
    bill = bill.stt_binarise()
    print(bill.val)
    bill.save()
    mill = load_bin()
    print(mill, mill.val, type(mill))
    bill = table_num_listise()
    print(bill.val)
    """
    bill = pent_list("C3 D5 D2 B5 C4 E4 E2 E1")
    bill.pent_objectify()
    print(bill.val[2].val)
    print(state_bin(2048).state_variablise())"""

# TODO: console interface;
# TODO: save > string
# TODO: table, password <> save
# DONE: File interface; print to table, mention input format in function name.
# Boss_list = [Bubbleman, Airman, Quickman, Heatman, Woodman, Metalman, Flashman, Crashman]
# Boss_Ante = ["C3", 'D2', 'C4', 'D5', 'B5', 'E1', 'E4', 'E2']  # pre-win values
# Boss_Post = ['D1', 'E3', 'B4', 'B2', 'D3', 'E5', 'C1', 'C5']  # post-win values
# Boss_Ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
# Boss_Post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values
