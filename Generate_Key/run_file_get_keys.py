from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from quantize_reconcile_amplify_privacy.cascade import bit_error_rate, find_mismatch_num, setBasicBlockSize, output, \
    cascade
from quantize_reconcile_amplify_privacy.privacy_amplification import amplify_privacy
from for_printing.binList_to_dec import bin_list_to_dec, convert_to_str
from for_printing.dec_to_binList import dec_to_bin_list
from for_printing.read_txt import get_num_after_phrase_in_file

import sys
import time
import os
import pickle
import struct
import math



##Computes the length of the final key.
#   @param rl is the size of the reconciled key. The size of the
#   key to be hashed in privacy amplification.
#   @param db is the number of parity bits disclosed during reconciliation and
#   confirmation.
#   @param s is the security parameter in between 0..1. The larger
#   the value the more secure is the final key.
#   @return rl-db-s*rl (this is a somewhat arbitrary way of defining the final length).
#   Might return a negative value.

_securityParameter = 0.05

def setSecurityParameter(c):
    if((c<1.0) and (abs(c)== c)):
        global _securityParameter
        _securityParameter = c

def finalLength(rl, db, s):
    extra = int(math.ceil(rl*s))
    if (extra < 1):
        extra = 1
    return rl-db-extra



if (__name__) == "__main__":
    print('Enter your choice: 1 for KEY_AB, 2 for KEY_AC')
    input1 = int(input())

    # '''for the first path, csv files are already taken by the device while recording, it has (f = 4000 HZ)
    # to see the plots run (C:\Users\Dania\PycharmProjects\audio_key\signal_processing_functions2\run_file_oldExps.py)
    #
    # while for the second path, wav files are recorded by the device and need to get their csv files, so we have to run
    # (C:\Users\Dania\PycharmProjects\audio_key\signal_processing_functions2\run_file_newWavExp.py) and you can also see the plots their
    # it has multiple frequqencis '''


    path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Corridor"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Locality"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\room-multi-freq"

    start_freq, freq_num, freq_gap = 16000, 1, 0


    first_file_num = 1
    last_file_num = first_file_num + 1
    chunk_size, step_size, alpha = 40, 1000, 0.2   # 80, 1000, 0.7
    key_len = 128

    if (input1 == 1):
        orig_stdout = sys.stdout
        f = open('out.txt', 'w')
        sys.stdout = f

        print(
            '\n********************************************* [ KEY_AB ] *********************************************\n')

        start_time = time.time()

        print('\n_______ 1. QUANTIZATION _______\n')

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                          step_size, chunk_size, alpha,
                                                          start_freq, freq_num, freq_gap)

        print('Responder string length before reconciliation:', len(cleaned_qts_resp))
        print('Initiator string length before reconciliation:', len(cleaned_qts_init))
        if (cleaned_qts_resp != cleaned_qts_init):
            print('Key stings are not equal and they need reconciliation (cascade)')

        print('\n_______ 2. CASCADE _______\n')

        print('Mismatches number = ', find_mismatch_num(cleaned_qts_init, cleaned_qts_resp))
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        print('bit error rate (probability) Pe:', Pe)
        size = setBasicBlockSize(Pe)
        print('basic block size: ', size, '\n')

        cascade(cleaned_qts_init, cleaned_qts_resp, size, 4)
        Initial_Shared_Key, _totalDisclosedBits = output()
        print('Initial_Shared_Key --- of length', len(Initial_Shared_Key), 'is:\n', (Initial_Shared_Key))

        print('\n_______ 3. PRIVACY AMPLIFICATION _______\n')

        _finalLength = finalLength(len(Initial_Shared_Key), _totalDisclosedBits, _securityParameter)
        print("_finalLength: ", _finalLength)
        if (_finalLength < 1):
            print("\nNooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            print("Not enough reconciled bits"  "for privacy amplification")
            sys.exit()

        # Final_Shared_Key = amplify_privacy(Initial_Shared_Key, _finalLength)
        Final_Shared_Key = amplify_privacy(Initial_Shared_Key, key_len)
        print('Final_Shared_Key --- of length', len(Final_Shared_Key), 'is:\n', Final_Shared_Key)

        Key_bit_string = convert_to_str(Final_Shared_Key)
        print('Final_Shared_Key_bit_string --- of length', len(Key_bit_string), 'is:\n', Key_bit_string)

        Final_Shared_Key_Dec_AB = bin_list_to_dec(Final_Shared_Key)
        print('Final_Shared_Key_Dec_AB =', Final_Shared_Key_Dec_AB)


        # with open('key.bin', 'wb') as f:
        #     pickle.dump(Final_Shared_Key_Dec_AB, f)
        #
        # with open('key.txt', 'w') as f:
        #     f.write(str(Final_Shared_Key_Dec_AB))

        sys.stdout = orig_stdout
        f.close()

        # check if the key conversion between integer and binary is successful
        print("key binList after privAmp: ", Final_Shared_Key)
        print(len(Final_Shared_Key))
        print("from binList to dec: ", Final_Shared_Key_Dec_AB)
        Final_Shared_Key_Dec_to_bin_list = dec_to_bin_list(Final_Shared_Key_Dec_AB, _finalLength)
        print("from dec to binList: ", Final_Shared_Key_Dec_to_bin_list)
        print(len(Final_Shared_Key_Dec_to_bin_list))
        if (Final_Shared_Key == Final_Shared_Key_Dec_to_bin_list):
            print("successful conversion")

        print("--- %s seconds ---" % (time.time() - start_time))
        # -------------------------------------------------------------------------------------------------------------------#

    elif (input1 == 2):
        orig_stdout = sys.stdout
        f = open('out.txt', 'a')
        sys.stdout = f

        print(
            '\n********************************************* [ KEY_AE ] *********************************************\n')

        print('\n_______ 1. QUANTIZATION _______\n')

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'Alice', 'Eve',
                                                          step_size, chunk_size, alpha,
                                                          start_freq, freq_num, freq_gap)

        print('Responder string length before reconciliation:', len(cleaned_qts_resp))
        print('Initiator string length before reconciliation:', len(cleaned_qts_init))
        if (cleaned_qts_resp != cleaned_qts_init):
            print('Key stings are not equal and they need reconciliation (cascade)')

        print('\n_______ 2. CASCADE _______\n')

        print('Mismatches number = ', find_mismatch_num(cleaned_qts_init, cleaned_qts_resp))
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        print('bit error rate (probability) Pe:', Pe)
        size = setBasicBlockSize(Pe)
        print('basic block size: ', size, '\n')

        cascade(cleaned_qts_init, cleaned_qts_resp, size, 4)
        Initial_Shared_Key, _totalDisclosedBits = output()
        print('Initial_Shared_Key --- of length', len(Initial_Shared_Key), 'is:\n', Initial_Shared_Key)

        print('\n_______ 3. PRIVACY AMPLIFICATION _______\n')

        _finalLength = finalLength(len(Initial_Shared_Key), _totalDisclosedBits, _securityParameter)
        print("_finalLength: ", _finalLength)
        if (_finalLength < 1):
            print("\nNooooooooooooooooooooo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            print("Not enough reconciled bits"  "for privacy amplification")
            sys.exit()

        # Final_Shared_Key = amplify_privacy(Initial_Shared_Key, _finalLength)
        Final_Shared_Key = amplify_privacy(Initial_Shared_Key, key_len)
        print('Final_Shared_Key --- of length', len(Final_Shared_Key), 'is:\n', Final_Shared_Key)

        Key_bit_string = convert_to_str(Final_Shared_Key)
        print('Final_Shared_Key_bit_string --- of length', len(Key_bit_string), 'is:\n', Key_bit_string)

        Final_Shared_Key_Dec_AE = bin_list_to_dec(Final_Shared_Key)
        print('Final_Shared_Key_Dec_AE =', Final_Shared_Key_Dec_AE)

        print(
            '\n********************************************* Compare Keys *********************************************\n')

        phrase = 'Final_Shared_Key_Dec_AB'
        Final_Shared_Key_Dec_AB = get_num_after_phrase_in_file('out.txt', phrase)
        print(type(Final_Shared_Key_Dec_AB))
        print('Final_Shared_Key_Dec_AB =', Final_Shared_Key_Dec_AB)
        print('Final_Shared_Key_Dec_AE =', Final_Shared_Key_Dec_AE)

        if (Final_Shared_Key_Dec_AB == Final_Shared_Key_Dec_AE):
            print('\nIdentical Keys')
        else:
            print('\nDifferent Keys')

        sys.stdout = orig_stdout
        f.close()