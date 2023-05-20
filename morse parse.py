# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:50:08 2020

@author: omer
"""

from types import MappingProxyType

Latin = MappingProxyType({
    '.': {
        ' ': 'e',
        '.': {
            ' ': 'i',
            '.': {
                ' ': 's', '.': {' ': 'h'}, '-': {' ': 'v'}},
            '-': {
                ' ': 'u', '.': {' ': 'f'}}},
        '-': {
            ' ': 'a',
            '.': {
                ' ': 'r', '.': {' ': 'l'}},
            '-': {
                ' ': 'w', '.': {' ': 'p', }, '-': {' ': 'j'}}}},
    '-': {
        ' ': 't',
        '.': {
            ' ': 'n',
            '.': {
                ' ': 'd', '.': {' ': 'b'}, '-': {' ': 'x'}},
            '-': {
                ' ': 'k', '.': {' ': 'c'}, '-': {' ': 'y'}}},
        '-': {
            ' ': 'm',
            '.': {
                ' ': 'g', '.': {' ': 'z'}, '-': {' ': 'q'}},
            '-': {' ': 'o'}}}})


# noinspection GrazieInspection
def tree_build(d: dict[str, str] | str):
    # take dict from char to morse
    # returns a tree from morse to char
    if isinstance(d, str):
        # the original keys are the leaves
        return d

    back = {'.': {}, '-': {}}
    for key, val in d.items():
        if not len(val):
            # the SP branch if it exists is a key leaf
            back[' '] = key
        else:
            # collect the items to a . branch and - branch
            back[val[0]][key] = val[1:]
    # construct the . and - branches. the SP branch returns immedietly
    return {m: tree_build(val) for m, val in back.items() if val}


# noinspection GrazieInspection
def tree_extend(tree: dict | str | MappingProxyType, d: dict[str, str] | str, overwrite: bool = False):
    if not d:
        return tree
    elif not tree:
        return tree_build(d)
    elif isinstance(d, str) or isinstance(tree, str):
        return tree_build(d) if overwrite else tree

    back = {' ': {}, '.': {}, '-': {}}
    for key, val in d.items():
        if not len(val):
            # the SP branch if it exists is a key leaf
            back[' '] = key
        else:
            # collect the items to a . branch and - branch
            back[val[0]][key] = val[1:]
    for m in ' .-':
        try:
            tree[m]
        except KeyError:
            back[m] = tree_build(back[m])
        else:
            back[m] = tree_extend(tree[m], back[m], overwrite)
    return {m: val for m, val in back.items() if val}


def BinToMorse(binary):
    binary = str(format(binary, 'b')) + '0'
    morse = ''
    while binary != '':
        if binary[:4] == '1110':
            binary = binary[3:]
            morse += '-'
        elif binary[:2] == '10':
            binary = binary[1:]
            morse += '.'
        elif binary[:3] == '000':
            binary = binary[2:]
            morse += ' '
            """this is not a by-1 mistake
            the parser has to see 3 0s but to delete only 2 for each pause.
            so that  pauses = (0s-1)/2  and not divided by 3"""
        elif binary[0] == '0':
            binary = binary[1:]
        else:
            print('Error')
            print('morse:', morse, '    reminder:', binary)
            break
    return morse


def MorseToBinary(morse):
    morse = str(morse)
    binary = '0b'
    for m in morse:
        if m == '-':
            binary += '1110'
        elif m == '.':
            binary += '10'
        elif m == ' ':
            binary += '00'
    return binary


def MorseDecode(morse, tree=Latin):
    latin = ''
    morse += ' '
    while morse:
        c = tree
        while not isinstance(c, str):
            c = c[morse[0]]
            morse = morse[1:]
        latin += c
    return latin


if __name__ == '__main__':
    print(BinToMorse(0b111000100000001))
    # print(bin(137))
    new_Latin = tree_extend(Latin, {
        str(i): ('-' * (i - 5) +
                 '.' * ((10 - i) if (i > 5) else i if (i < 5) else 5) +
                 '_' * (5 - i))
        for i in range(10)
    })
    print(MorseDecode('... --- ...', new_Latin))

    print(str(tree_build({"a": "-.", "b": "-...", "c": "-.-."})).replace("'},", "'},\n"))
    input()
