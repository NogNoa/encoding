#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bin')
parser.add_argument('--text')
args = parser.parse_args()
call = open(args.bin, 'rb')
# call = open("D:\\Games\\mGBA-0.6.3-win32\\rom\\Operation C (U) [!].gb", 'rb')
# call = open("hello_world.gb", 'rb')
table = ' !"Ñ$C&\'®®©+,-./0123456789:Ù¡=¿?ÄABCDEFGHIJKLMNOPQRSTUVWXYZÖÜÀÈÌ'

back = ''
call = call.read()
for h in call:
    h -= 0x20
    char = h % 0x40
    char = table[char]
    white = (h // 0x40) % 0x4
    if white == 0:
        white = ''
    elif white == 1:
        white = '\n'
    elif white == 2:
        white = ' '
    elif white == 3:
        white = '||'
    else:
        print('error:', char)
    print(char, end=white)
#text = open('args.text', 'w+')
#text.write(back)
