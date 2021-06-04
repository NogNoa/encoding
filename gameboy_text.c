# include <stdio.h>
# include <stdlib.h>

# /*

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

# */
// """

char * file_stringise(char * filename);

int main(int argc, char *argv[])
{
    #define HIGH 0b1000000

    char table[66] = {' ','!','"','Ñ','$','C','&','\'','®','®','©','+',',','-','.','/', /* 0x */
                      '0','1','2','3','4','5','6','7' ,'8','9',':','Ù','¡','=','¿','?', /* 1x */
                      'Ä','A','B','C','D','E','F','G' ,'H','I','J','K','L','M','N','O', /* 2x */ 
                      'P','Q','R','S','T','U','V','W' ,'X','Y','Z','Ö','Ü','À','È','Ì'};/* 3x */
    char * call = file_stringise(argv[1]);

    for (int i=0;call[i] != 0;++i){
        int c =call[i];
        c -= 0x20;
        char white = (c / HIGH);
        c %= HIGH;
        c = table[c];
        switch(white){
            case 0: white = '\a';break; //empty charecter
            case 1: white = '\n';break;
            case 2: white = ' ';break;
            case 3: white = '|';break;
            default: printf("\nerror: %x %x\n",white,c);
        }
        putchar(c);putchar(white);
    }
}

// todo: learn about wide charecters in c.

// """


