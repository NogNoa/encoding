# include <stdio.h>
# include <stdlib.h>

# 

parser = argparse.ArgumentParser()
parser.add_argument('bin')
parser.add_argument('--text')
args = parser.parse_args()
table = ' !"Ñ$C&\'®®©+,-./0123456789:Ù¡=¿?ÄABCDEFGHIJKLMNOPQRSTUVWXYZÖÜÀÈÌ'
call = open(args.bin, 'rb')
# call = open("D:\\Games\\mGBA-0.6.3-win32\\rom\\Operation C (U) [!].gb", 'rb')
back = ''
while call:
    h = call.read(1)
    h = int.from_bytes(h, "little") - 0x20
    char = h % 0b1000000
    char = table[char]
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

# 
// """

int main(int argc, char *argv[])
{
    char *bin = argv[1]

    char table[66] = {' ','!','"','Ñ','$','C','&','\'','®','®','©','+',',','-',
                      '.','/','0','1','2','3','4','5','6','7','8','9',':','Ù',
                      '¡','=','¿','?','Ä','A','B','C','D','E','F','G','H','I',
                      'J','K','L','M','N','O','P','Q','R','S','T','U','V','W',
                      'X','Y','Z','Ö','Ü','À','È','Ì'};
    FILE * call = fopen (bin, "rb");

    for 
}

// """