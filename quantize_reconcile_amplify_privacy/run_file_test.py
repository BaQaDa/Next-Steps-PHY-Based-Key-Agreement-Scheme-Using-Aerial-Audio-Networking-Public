from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from quantize_reconcile_amplify_privacy.cascade import bit_error_rate, find_mismatch_num, setBasicBlockSize, output, cascade
from quantize_reconcile_amplify_privacy.privacy_amplification import amplify_privacy
from for_printing.binList_to_dec import bin_list_to_dec
from for_printing.read_txt import get_num_after_phrase_in_file

import sys
import time


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]
    # Join list items using join()
    res = int("".join(s))

    return (res)

if (__name__) == "__main__":
    print('Enter your choice; 1 for KEY_AB, 2 for KEY_BC')
    input1 = int(input())


    path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Amplitude Expers\\dtw exp\\my_dtw\\6_250_45"
    # path = 'D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\moveObj'

    first_file_num = 10
    last_file_num = first_file_num + 1
    chunk_size, step_size, alpha = 100, 1000, 0.8


    if (input1 == 1):
        orig_stdout = sys.stdout
        f = open('out.txt', 'w')
        sys.stdout = f

        print ('\n********************************************* [ KEY_AB ] *********************************************\n')

        start_time = time.time()

        print('\n_______ 1. QUANTIZATION _______\n')

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'init_', 'second_', step_size,
                                                                       chunk_size, alpha)
        print('Responder string length before reconciliation:', len(cleaned_qts_resp))
        print('Initiator string length before reconciliation:', len(cleaned_qts_init))
        if (cleaned_qts_resp != cleaned_qts_init):
            print('Key stings are not equal and they need reconciliation (cascade)')

        print('\n_______ 2. CASCADE _______\n')

        print('Mismatches number = ', find_mismatch_num(cleaned_qts_init, cleaned_qts_resp))
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        print('bit error rate (probability) Pe:', Pe)
        size = setBasicBlockSize(Pe)
        print('basic block size: ', size ,'\n')

        cascade(cleaned_qts_init, cleaned_qts_resp, size, 4)
        Initial_Shared_Key = output()
        print('Initial_Shared_Key --- of length', len(Initial_Shared_Key), 'is:\n', (Initial_Shared_Key))

        print('\n_______ 3. PRIVACY AMPLIFICATION _______\n')

        Final_Shared_Key = amplify_privacy(Initial_Shared_Key, 128)
        print('Final_Shared_Key --- of length', len(Final_Shared_Key), 'is:\n', Final_Shared_Key)
        Final_Shared_Key_Dec_AB = bin_list_to_dec(Final_Shared_Key)
        print('Final_Shared_Key_Dec_AB =',Final_Shared_Key_Dec_AB)

        sys.stdout = orig_stdout
        f.close()
        print("--- %s seconds ---" % (time.time() - start_time))
        # -------------------------------------------------------------------------------------------------------------------#

    elif(input1 == 2):
        orig_stdout = sys.stdout
        f = open('out.txt', 'a')
        sys.stdout = f

        print ('\n********************************************* [ KEY_BC ] *********************************************\n')

        print('\n_______ 1. QUANTIZATION _______\n')

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'second_', 'secondC_', step_size,
                                                                       chunk_size, alpha)
        print('Responder string length before reconciliation:', len(cleaned_qts_resp))
        print('Initiator string length before reconciliation:', len(cleaned_qts_init))
        if (cleaned_qts_resp != cleaned_qts_init):
            print('Key stings are not equal and they need reconciliation (cascade)')

        print('\n_______ 2. CASCADE _______\n')

        print('Mismatches number = ', find_mismatch_num(cleaned_qts_init, cleaned_qts_resp))
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        print('bit error rate (probability) Pe:', Pe)
        size = setBasicBlockSize(Pe)
        print('basic block size: ', size ,'\n')

        cascade(cleaned_qts_init, cleaned_qts_resp, size, 4)
        Initial_Shared_Key = output()
        print('Initial_Shared_Key --- of length', len(Initial_Shared_Key), 'is:\n', Initial_Shared_Key)

        print('\n_______ 3. PRIVACY AMPLIFICATION _______\n')

        Final_Shared_Key = amplify_privacy(Initial_Shared_Key, 128)
        print('Final_Shared_Key --- of length', len(Final_Shared_Key), 'is:\n', Final_Shared_Key)
        Final_Shared_Key_Dec_BC = bin_list_to_dec(Final_Shared_Key)
        print('Final_Shared_Key_Dec_BC =', Final_Shared_Key_Dec_BC)

        print ('\n********************************************* Compare Keys *********************************************\n')

        phrase = 'Final_Shared_Key_Dec_AB'
        Final_Shared_Key_Dec_AB = get_num_after_phrase_in_file('out.txt', phrase)

        print('Final_Shared_Key_Dec_AB =', Final_Shared_Key_Dec_AB)
        print('Final_Shared_Key_Dec_BC =', Final_Shared_Key_Dec_BC)

        if (Final_Shared_Key_Dec_AB == Final_Shared_Key_Dec_BC):
            print('\nIdentical Keys')
        else:
            print('\nDifferent Keys')

        sys.stdout = orig_stdout
        f.close()