import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bin')
parser.add_argument('text')
args = parser.parse_args()
table = ' !"Ñ$C&\'®®©+,-./0123456789:Ù¡=¿?ÄABCDEFGHIJKLMNOPQRSTUVWXYZÖÜÀÈÌ'
# call = open(args.bin, 'rb')
call = open("D:\\temp\\patching teach\\Gargoyle's Quest - Text Restoration.ips", 'rb')
back = ''
while call:
    h = call.read(1)
    h = int(h) - 0x20
    char = h % 0b1000000
    char = table[char]
    char = str(char)
    white = (h // 0b1000000) % 0b100
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
    back += char + white
print(back)
text = open('args.text', 'w+')
text.write(back)
