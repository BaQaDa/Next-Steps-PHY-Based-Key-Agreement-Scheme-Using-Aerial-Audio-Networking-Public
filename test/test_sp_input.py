import string
import sys
import pickle

from for_printing.read_txt import get_num_after_phrase_in_file


def read_bits_from_file(filename,bigendian):
    bitlist = list()
    if filename == None:
        f = sys.stdin
    else:
        f = open(filename, "rb")
    while True:
        bytes = f.read(16384)
        if bytes:
            for bytech in bytes:
                if sys.version_info > (3,0):
                    byte = bytech
                else:
                    byte = ord(bytech)
                for i in range(8):
                    if bigendian:
                        bit = (byte & 0x80) >> 7
                        byte = byte << 1
                    else:
                        bit = (byte >> i) & 1
                    bitlist.append(bit)
        else:
            break
    f.close()
    return bitlist

if (__name__) == "__main__":

    fileOut = "C:\\Users\\Dania\\PycharmProjects\\audio_key\\quantize_reconcile_amplify_privacy\\out.txt"
    fileTxt = "C:\\Users\\Dania\\PycharmProjects\\audio_key\\quantize_reconcile_amplify_privacy\\key.txt"
    fileBin = "C:\\Users\\Dania\\PycharmProjects\\audio_key\\quantize_reconcile_amplify_privacy\\key.bin"


    phrase = 'Final_Shared_Key_Dec_AB'
    Final_Shared_Key_Dec_AB = get_num_after_phrase_in_file(fileOut, phrase)
    Final_Shared_Key_Dec_AB = bin(Final_Shared_Key_Dec_AB)
    Final_Shared_Key_Dec_AB =  list(Final_Shared_Key_Dec_AB.split(" "))


    print("Final_Shared_Key_Dec_AB from out file: ", Final_Shared_Key_Dec_AB)
    print(bin(Final_Shared_Key_Dec_AB))
    with open('key.bin', 'wb') as f:
        pickle.dump(Final_Shared_Key_Dec_AB, f)

    with open('key.txt', 'w') as f:
        f.write(str(Final_Shared_Key_Dec_AB))

    with open('data.bin', 'wb') as f:
        pickle.dump(Final_Shared_Key_Dec_AB, f)

    bits = read_bits_from_file('key.bin',True)
    print(bits)
    bits2 = read_bits_from_file('key.txt',True)
    print(bits2)

    if(bits == bits2 ):
        print("dsbfhsdbfhs")

