file = open('goblinorig.txt', 'w+')
table =  ' !"Ñ$C&\'®®©+,-./0123456789:Ù¡=¿?ÄABCDEFGHIJKLMNOPQRSTUVWXYZÖÜÀÈÌ'
call = '05 20 FC FA 1A'
call =call.split(' ')
back = ''
for h in call:
    h = int(h,16)
    h -= 0x20
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
file.write(back)