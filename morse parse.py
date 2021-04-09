# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:50:08 2020

@author: omer
"""


def BinToMorse(Binary):
    Binary = str(format(Binary, 'b')) + '0'
    morse = ''
    while Binary != '':
        if Binary[:4] == '1110':
            Binary = Binary[3:]
            morse += '-'
        elif Binary[:2] == '10':
            Binary = Binary[1:]
            morse += '.'
        elif Binary[:3] == '000':
            Binary = Binary[2:]
            morse += ' '
            """this is not a by-1 mistake
            the parser has to see 3 0s but to delete only 2 for each pause.
            so that  pauses = (0s-1)/2  and not divided by 3"""
        elif Binary[0] == '0':
            Binary = Binary[1:]
        else:
            print('Error')
            print('morse:', morse, '    reminder:', Binary)
            break
    return morse


def MorseToBinary(Morse):
    Morse = str(Morse)
    Binary = '0b'
    for m in Morse:
        if m == '-':
            Binary += '1110'
        elif m == '.':
            Binary += '10'
        elif m == ' ':
            Binary += '00'
    return Binary


if __name__ == '__main__':
    print(BinToMorse(0b111000100000001))
    # print(bin(137))

    print(MorseToBinary('... --- ...'))
