# -*- coding: utf-8 -*-

from string import ascii_uppercase
# from codecs import open as cdcopen
import argparse


def num_pentise(number: int) -> str:
    """input format: (0–24)
    returns the place of a dot in a five by five table.
     pent values goes from A1 to E5"""
    back = ascii_uppercase[number // 5] + str(number % 5 + 1)
    return back


def pent_numerise(pent: str) -> int:
    """format: (A–E)(1–5)"""
    row: str = pent[0]
    col: str = pent[1]
    number: int = (ascii_uppercase.index(row)) * 5 + int(col) - 1
    return number


class PentList:
    """ format: 9*((A–E)(1–5))
    a list of pent values
    """

    def __init__(self, table: str | list[str]):
        # table string has to be 9 pent values with spaces!
        # it could be just a list
        if type(table) is str:
            table = table.split(' ')
        self.val = table

    def __str__(self):
        return str(self.val)

    def pent_numerise(self):
        back = [pent_numerise(pl) for pl in self.val]
        return NumList(back)

    def make_table(self, file='MM2pswd.csv'):
        if file[-4:] != '.csv':
            file += '.csv'
        lexicon = {
            'A': [0, 0, 0, 0, 0],
            'B': [0, 0, 0, 0, 0],
            'C': [0, 0, 0, 0, 0],
            'D': [0, 0, 0, 0, 0],
            'E': [0, 0, 0, 0, 0],
        }
        for pl in self.val:
            row = pl[0]
            col = int(pl[1]) - 1
            # ^just translating numeral digit from pent to an integer index in the corresponding list
            lexicon[row][col] = 1
        back = open(file, 'w+', encoding="utf-8")
        back.write(',1,2,3,4,5\n')
        for i in lexicon:
            line = i + ','
            for j in lexicon[i]:
                line += '\u2B24' * j + ','
                # the circle symbol ⬤ is U+2B24
                # the bullet symbol • is U+2022
            line += '\n'
            back.write(line)
        back.close()


class NumList:
    """format: [9*(0–24)]"""

    def __init__(self, call: list):
        self.val = call

    def __str__(self):
        return str(self.val)

    def num_pentise(self):
        back = [num_pentise(pl) for pl in self.val]
        return PentList(back)

    def num_statify(self):
        boss_ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
        boss_post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values
        number_list = self.val[:9]
        # ^accepting too long inputs but at user's risk as only first 9 items get through
        etank = min(number_list)
        number_list.remove(etank)
        if etank >= 5:
            print("Invalid Password")
            return
            # raise ValueError()
        bossi = [2, 2, 2, 2, 2, 2, 2, 2]

        # 0 or 1 will not be distinguised from boolians. None should also work, it's just more crowding.

        def is_defeated(group, val):
            if boss in group:
                place = group.index(boss)
                bossi[place] = val

        while number_list:
            boss = number_list.pop() - etank
            boss += 20 * (boss < 5)
            # see comment for {boss -= 20 * (boss > 24)} in function stt_numerise
            is_defeated(boss_ante, False)
            is_defeated(boss_post, True)
        if 2 in bossi:
            print("Invalid Password")
            return
            # raise ValueError()
        return StateVar(bossi, etank)


class StateVar:
    """format: [8*(bool)], (0–4)"""

    def __init__(self, bossi, etank):
        self.bossi, self.etank = bossi, etank

    def __str__(self):
        return str(self.bossi) + ', ' + str(self.etank)

    def inventorise(self):
        def mask(char, cond):
            if cond:
                return char
            else:
                return ' '

        b = self.bossi
        back = 'P' + mask('B', b[0]) + mask('A', b[1]) + mask('Q', b[2])
        back += '\n' + mask('H', b[3]) + mask('W', b[4]) + mask('M', b[5]) + mask('F', b[6])
        back += '\n' + mask('C', b[7]) + mask('1', b[3]) + mask('2', b[1]) + mask('3', b[6])
        return back

    def stt_numerise(self):
        # output format: [8*(0–24), (0–4)]
        boss_ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
        boss_post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values
        pswd = []
        for i, cond in enumerate(self.bossi):
            boss = boss_post[i] if cond else boss_ante[i]
            boss = boss + self.etank
            # if we reach E5, which is 24 (4*5 +5 -1) the next should be B1 = 5 (1*5 + 1 - 1)
            # instead of 25. So 20 less. The A row is actually kept for the Etank count itself.
            boss -= 20 * (boss > 24)
            pswd += [boss]
        pswd += [self.etank]
        return NumList(pswd)  # as list of 9 numbers

    def stt_binarise(self):
        back = self.etank << 8
        back = sum((cond << i
                    for i, cond
                    in enumerate(self.bossi)),
                   start=back)
        return StateBin(back)


class StateBin:
    """ format: (0–1279) i.e.
                ((0–255)+2^8*(0–4))
    low 8bits for bosses, high 3bits for Etanks"""

    def __init__(self, call: int):
        if call > 2047:
            raise ValueError(f'state value {call}, {bin(call)} is larger than 11bits')
        self.val = call

    def __str__(self):
        return bin(self.val)

    def bin_variablise(self):
        bosses = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            back: int = self.val & 2 ** i
            back = bool(back)
            bosses[i] = back
        etank = self.val // 2 ** 8
        return StateVar(bosses, etank)

    def save(self, file='mm2.sav'):
        back = self.val.to_bytes(2, 'little')
        with open(file, 'w+b') as file:
            file.write(back)


# file loading functions

def load_bin(file='mm2.sav'):
    call = open(file, 'r+b').read()
    back = int.from_bytes(call, 'little')
    return StateBin(back)


def table_num_listise(file='MM2pswd.csv'):
    if file[-4:] != '.csv':
        print('Please point me to a comma separated table')
        raise ValueError(file)
    call = open(file, 'r+').readlines()
    call = [pl.split(',') for pl in call]
    back = []
    for line in call:
        for pl in range(1, 6):
            if line[pl] == '•':
                num = (call.index(line)) * 5 + pl - 6  # -1 from both the 5s & 1s places
                back.append(num)
    return NumList(back)


if __name__ == "__main__":

    # parser functunality

    def bin_get(type_, object_=None, bin_=None):
        call = load_bin(bin_).bin_variablise()
        if type_[0] == 'i':
            back = call.inventorise()
        else:
            back = call.stt_numerise().num_pentise()
            if type_[0] == 't':
                back.make_table(object_)
                back = "You created table in " + str(object_)
            elif type_[0] == 'p':
                back = ' '.join(back.val)
            else:  # if all types have failed
                exit(3)
        return back


    def bin_give(type_, object_=None, bin_=None):
        if type_[0] == 't':
            object_ = table_num_listise(object_)
        elif type_[0] == 'p':
            object_ = PentList(object_)
            object_ = object_.pent_numerise()
        else:  # inventory or something else invalid
            exit(4)
        object_.num_statify().stt_binarise().save(bin_)
        print("a gamestate was saved from your password")


    parser = argparse.ArgumentParser(description='you can only get inventory, it is useless to give it')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('-T', '--get', help='Get from me, the program, a type of object', action="store_true")
    actions.add_argument('-V', '-v', '--give', help='Give to me, the program, a type of object, to save it to a file',
                         action="store_true")
    typs = parser.add_mutually_exclusive_group()
    typs.add_argument('-t', '--table', help='', action="store_true")
    typs.add_argument('-p', '-P', '--password', help='', action="store_true")
    typs.add_argument('-i', '-I', '--inventory', help='', action="store_true")
    parser.add_argument('-o', '--object', help='path to table file or the password sepereted by spaces.', type=str)
    parser.add_argument('-s', '--save', help='the path to your target save file', type=str)
    args = parser.parse_args()

    if args.table:
        typ = ('t', args.table)
    elif args.password:
        typ = ('p', args.password)
    elif args.inventory:
        typ = ('i', args.inventory)
    else:  # if all types have failed
        print('Something was wrong with the type you entered. Sorry')
        exit(2)

    if args.get:
        print(bin_get(type_=typ, object_=args.object, bin_=args.save))
    elif args.give:
        bin_give(type_=typ, object_=args.object, bin_=args.save)
    else:
        print('Something was wrong with the action you entered. Sorry')
        exit(1)

    if args.get:
        call = load_bin(args.save).bin_variablise()
        if args.inventory:
            back = call.inventorise()
            print(back)
        else:
            back = call.stt_numerise().num_pentise()
            if args.table:
                call.stt_numerise().num_pentise().make_table(args.object)
                print("You created table in ", args.object.path)
            else:
                print(back)
        # else:
        #     print('Something was wrong with the type you entered. Sorry')
    elif args.give:
        if args.password:
            call = PentList(args.object)
            back = call.pent_numerise()
        elif args.table:
            back = table_num_listise(args.object)
        else:
            raise ValueError('Something was wrong with the type you entered. Sorry')
        back.num_statify().stt_binarise().save(args.save)
    else:
        print('Something was wrong with the action you entered. Sorry')

    jack = StateBin(1279).bin_variablise().stt_numerise()
    jack = jack.num_statify().stt_binarise()
    print(jack.val)
    jack.save()

    bill = PentList(['D1', 'E3', 'B4', 'B2', 'D3', 'E5', 'C1', 'C5']).val
    jill = []
    for a in bill:
        jill += [pent_numerise(a)]
    print(jill)

    bill = PentList(['D4', 'B1', 'C2', 'B5', 'E1', 'B3', 'C4', 'D3', 'A4'])
    bill.make_table()
    bill = bill.pent_numerise()
    print(bill.val)
    bill = bill.num_statify()
    print(bill.bossi, bill.etank)
    bill = bill.stt_binarise()
    print(bill.val)
    bill.save()
    mill = load_bin()
    print(mill, mill.val, type(mill))
    bill = table_num_listise()
    print(bill.val)

    bill = PentList("C3-D5-D2-B5-C4-E4-E2-E1")
    print(bill.val[2])
    print(StateBin(2048).bin_variablise())

# Td:
# DONE: got password: D5 B2 C3 C1 E2 B4 C5 D4 A5. Program itself claims it's invalid.
#       reimplement cmdln interface
#       console interface;
#       save > inventory
#       table, password <> save
#       File interface; print to table, mention input format in function name.
# Boss_list = [Bubbleman, Airman, Quickman, Heatman, Woodman, Metalman, Flashman, Crashman]
# Boss_Ante = ["C3", 'D2', 'C4', 'D5', 'B5', 'E1', 'E4', 'E2']  # pre-win values
# Boss_Post = ['D1', 'E3', 'B4', 'B2', 'D3', 'E5', 'C1', 'C5']  # post-win values
# Boss_Ante = [12, 16, 13, 19, 9, 20, 23, 21]  # pre-win values
# Boss_Post = [15, 22, 8, 6, 17, 24, 10, 14]  # post-win values

# $009A bits from little endian [Heatman, Airman, Woodman, Bubbleman, Quickman, Flashman, Metalman, Crashman]
# $009B the least significant bits for items 1,2,3 in order
# $00A7 number of energy tanks

# .mst: CPU RAM starts at $1720, hence $17BA $17BB $17C7
