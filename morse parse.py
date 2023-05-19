# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:50:08 2020

@author: omer
"""

Latin = {
'.': {
    ' ': 'e',
    '.': {
        ' ':'i',
        '.': {
            ' ': 's', '.':{' ': 'h'}, '-': {' ': 'v'}},
        '-': {
            ' ': 'u', '.': {' ': 'f'}}},
    '-': {
        ' ': 'a',
        '.': {
            ' ': 'r', '.': {' ': 'l'}},
        '-': {
            ' ': 'w', '.': {' ': 'p',}, '-': {' ': 'j'}}}},
'-': {
    ' ': 't',
    '.': {
        ' ': 'n',
        '.': {
            ' ': 'd', '.': {' ':'b'}, '-': {' ': 'x'}},
        '-': {
            ' ': 'k', '.': {' ': 'c'}, '-': {' ': 'y'}}},
    '-': {
        ' ': 'm',
        '.': {
            ' ': 'g', '.': {' ': 'z'}, '-': {' ': 'q'}},
        '-': {' ': 'o'}}
}}

def tree_build(d: dict[str, str]):
    # take dict from char to morse
    # return tree from morse to char
    if not d or isinstance(d, str):
        return d
    
    back = {'.': {}, '-': {}}
    for key,val in d.items():
        if not len(val):
            back[' '] = key
        else:
            back[val[0]][key] = val[1:]
    
    return {m: tree_build(val) for m, val in back.items()}

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

def MorseToLatin(morse):
    latin = ''
    morse += ' '
    while morse:
        c = Latin
        while not isinstance(c, str):
            c = c[morse[0]]
            morse =  morse[1:]
        latin += c
    return latin


if __name__ == '__main__':
    print(BinToMorse(0b111000100000001))
    # print(bin(137))

    print(MorseToLatin('... --- ...'))
    print(str(tree_build({"a": "-.", "b": "-...", "c": "-.-."})).replace("'},", "'},\n"))
    input()
