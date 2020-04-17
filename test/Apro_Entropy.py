import numpy as np
from for_printing.read_txt_get_bits import get_num_after_phrase_in_file, dec_to_bin_list


def bits_to_int(bits):
    theint = 0
    for i in range(len(bits)):
        theint = (theint << 1) + bits[i]
    return theint


def ApEn(U, m, r):

    def _maxdist(x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(m):
        x = [[U[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]
        C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (N - m + 1.0) for x_i in x]
        return (N - m + 1.0)**(-1) * sum(np.log(C))

    N = len(U)

    return abs(_phi(m+1) - _phi(m))

# Usage example

fileOut = "C:\\Users\\Dania\\PycharmProjects\\audio_key\\quantize_reconcile_amplify_privacy\\out.txt"
phrase = 'Final_Shared_Key_Dec_AB'
Final_Shared_Key_Dec_AB = get_num_after_phrase_in_file(fileOut, phrase)
Final_Shared_Key_Dec_to_bin_list = dec_to_bin_list(Final_Shared_Key_Dec_AB)
print("from dec to binList: ", Final_Shared_Key_Dec_to_bin_list)
print(len(Final_Shared_Key_Dec_to_bin_list))
bits = Final_Shared_Key_Dec_to_bin_list
# U = bits

# U = np.array(bits)
# print(U)
# print(ApEn(U, 2, 3))


U = np.array([85, 80, 89] * 17)
print(U)
print (ApEn(U, 2, 3))
#
#
# randU = np.random.choice([85, 80, 89], size=17*3)
# print (ApEn(randU, 2, 3))