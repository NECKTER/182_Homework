import getopt
import sys
import BitVector as BitV


e = 65537
p = 0 #49157
q = 0 #49169


def calculateKeys():
    pKey = BitV.BitVector(intVal=e)
    x = 0
    p = 0
    g = 0
    for i in range(49153, 49200):
        q = BitV.BitVector(intVal=i-1)
        if (2 ** (i-1)) % i == 1 and int(pKey.gcd(q)) == 1:
            x += 1
            if x == 1:
                p = i
            else:
                g = i
                return p, g
    return p, g


def multiply(number, key, mod):
    data = number
    value = str(key)
    i = 0
    for c in value:
        i += 1
        if c == '1':
            data = data.gf_multiply_modular(number, mod, 256)
        if i != key.length():
            data = data.gf_multiply_modular(data, mod, 256)
    return data


def encrypt(data):
    temp = ''
    data_out = ''
    bits = BitV.BitVector(size=256)

    alpha, beta = calculateKeys()
    key = BitV.BitVector(intVal=e)
    n = BitV.BitVector(intVal=(alpha*beta))

    keySizeDifference = (128 - (len(data) * 16) % 128) / 16
    for _ in range(0, int(keySizeDifference)):
        data += chr(10)
    i = 0
    for c in data:
        i += 1
        temp += c
        if i == 16:
            bits.set_value(textstring=temp)
            bits.pad_from_left(128)
            #encode
            data_out += multiply(bits, key, n).get_bitvector_in_ascii()
            temp = ''
            i = 0
    return data_out


#does not work properly
def decrypt(data):
    data_out = ''
    bits = BitV.BitVector(size=256)
    temp = ''

    alpha, beta = calculateKeys()
    key = BitV.BitVector(intVal=e)
    n = BitV.BitVector(intVal=(alpha * beta))
    phi_n = BitV.BitVector(intVal=((alpha - 1) * (beta - 1)))
    d = key.multiplicative_inverse(phi_n)

    x = 0
    i = 0
    for c in data:
        i += 1
        temp += c
        if i == 32:
            x += 1
            print(x)
            bits.set_value(textstring=temp)
            #decode
            padding, text = multiply(bits, d, n).divide_into_two()
            data_out += text.get_bitvector_in_ascii()
            temp = ''
            i = 0

    return data_out


try:
    opts, args = getopt.getopt(sys.argv[1:], "e:d:", ["encrypt=", "decrypt="])  # set up call commands
except getopt.GetoptError as err:
    print(err)  # prints the error if one occurs
    sys.exit(2)  # exit sys with code 2

in_file = 0  # declare input file
out_file = open(args[0], "w", errors='ignore')  # declare and difine output file
text = ""  # declare text
for o, a in opts:
    if o == "-e":  # if encrypt command
        in_file = open(a, "r")  # define input file
        text = encrypt(in_file.read())  # read the input file
        in_file.close()  # close the input file
    if o == "-d":  # if decrypt command
        in_file = open(a, "r")  # define input file
        text = decrypt(in_file.read())  # read input file
        in_file.close()  # close the input file
print(text)
out_file.write(text)  # output resulting text to file
