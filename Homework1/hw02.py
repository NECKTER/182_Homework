import getopt, sys


e = 65537

#all chars are 8 bits
def encrypt(data):
    i = 0
    keySizeDifference = (128 - (len(data) * 8) % 128) / 8
    for _ in range(0,int(keySizeDifference)):
        data += chr(10)
    print(i % 128, ' ', (128 - (len(data) * 8) % 128) / 8)
    for c in data:
        i+=8
        print(ord(c), " ", i)
    print(i%128, ' ', (128-(len(data)*8)%128)/8)
    return data

def decrypt(data):

    return data

try:
    opts, args = getopt.getopt(sys.argv[1:], "e:d:", ["encrypt=", "decrypt="])  #set up call commands
except getopt.GetoptError as err:
    print(err)                                                                  #prints the error if one occurs
    sys.exit(2)                                                                 #exit sys with code 2

in_file = 0                                                                     #declare input file
out_file = open(args[0], "w")                                                   #declare and difine output file
text = ""                                                                       #declare text
for o, a in opts:
    if o == "-e":                                                               #if encrypt command
        in_file = open(a, "r")                                                  #define input file
        text = encrypt(in_file.read())                                                   #read the input file
        in_file.close()                                                         #close the input file
    if o == "-d":                                                               #if decrypt command
        in_file = open(a, "r")                                                  #define input file
        text = decrypt(in_file.read())                                                   #read input file
        in_file.close()                                                         #close the input file
print(text)

out_file.write(text)                                                            #output resulting text to file
