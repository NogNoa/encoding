# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:50:08 2020

@author: omer
"""


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


if __name__ == '__main__':
    print(BinToMorse(0b111000100000001))
    # print(bin(137))

    print(MorseToBinary('... --- ...'))
