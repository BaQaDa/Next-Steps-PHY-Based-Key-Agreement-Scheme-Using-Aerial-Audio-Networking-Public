# import sys
#
# #
# # def prRed(skk): print("\033[91m {}\033[00m".format(skk))
# # def prGreen(skk): print("\033[92m {}\033[00m".format(skk))
# # prRed("Hello")
# # #------------------------------------------------------------------------------------
# #
# import pickle
# # with open('data.bin', 'wb') as f: pickle.dump(9 ** 33, f)
# # with open('data.bin', 'rb') as f: print(pickle.load(f))
# # #------------------------------------------------------------------------------------
# #
# # from random import randint
# # def random_with_N_digits(n):
# #     range_start = 10**(n-1)
# #     range_end = (10**n)-1
# #     return randint(range_start, range_end)
# # num = random_with_N_digits(len(str(5454545)))
# # #------------------------------------------------------------------------------------
# #
# # a = format(5, "b")
# # print(a)
# # print(bin(5))
# # #------------------------------------------------------------------------------------
# #
# # # with open('data2.txt', 'w') as f:
# # #     f.write(format(5, "b"))
# # #------------------------------------------------------------------------------------
# # # import struct
# # # bits = "10111111111111111011110"  # example string. It's always 23 bits
# # # with open("test.bnr", "wb") as f:
# # #     f.write(struct.pack('i', int(bits[::-1], 2)))
# # #------------------------------------------------------------------------------------
# #
# # #------------------------------------------------------------------------------------
# # Final_Shared_Key_Dec_AB = 36423883339734525136181950071060118351253235124805464900551463122051820977733
# # print(len(str(Final_Shared_Key_Dec_AB)))
# #
# # with open('data.bin', 'wb') as f:
# #     pickle.dump(Final_Shared_Key_Dec_AB, f)
# #
# # with open('data.bin', mode='rb') as file: # b is important -> binary
# #     fileContent = file.read()
# #
# # # print(int(fileContent))
# # print(fileContent)
#
#
# # with open('key_ab_bin.txt', 'w') as f:
# #     f.write(bin(Final_Shared_Key_Dec_AB))
#
# # with open('key_ab_asci.txt', 'w') as f:
# #     f.write(format(str(Final_Shared_Key_Dec_AB).encode('ascii')))
#
# # with open('key_ab_u.txt', 'w') as f:
# #     f.write(format(str(Final_Shared_Key_Dec_AB).encode('utf8')))
# #
# # with open('key_str.txt', 'w') as f:
# #     f.write(str(Final_Shared_Key_Dec_AB))
# #------------------------------------------------------------------------------------
# Final_Shared_Key_Dec_AB = 5
# Final_Shared_Key_Dec_AB = bin(Final_Shared_Key_Dec_AB)
# print(Final_Shared_Key_Dec_AB)
# Final_Shared_Key_Dec_AB = list(Final_Shared_Key_Dec_AB.split(" "))
#
# print(Final_Shared_Key_Dec_AB)
# print()
#
# a= [1,2,3]
# print(a+[5])
#
# #------------------------------------------------------------------------------------
import numpy as np
#
# def chunks(concatenated_step_amp, chunk_size):
#     """Yield successive n-sized chunks from l."""
#     for i in range(0, len(concatenated_step_amp), chunk_size):
#         yield concatenated_step_amp[i:i + chunk_size]
#
#
# def get_thresholds(chunk, alpha):
#     mean = np.mean(chunk)
#     stdDev = np.std(chunk)
#     q_pos = mean + alpha * stdDev
#     q_neg = mean - alpha * stdDev
#     return q_pos, q_neg
#
#
# def quantize_chunks(chunked_step_amp, alpha):
#     for chunk in chunked_step_amp:
#         q_pos, q_neg = get_thresholds(chunk, alpha)
#         print(q_pos, q_neg)
#
#
# ch_lst = chunks([1,2,3,4,5,6,7,8,9,10,11,12], 3)
# # print(list(ch_lst))
# quantize_chunks(ch_lst, 0.5)
#
# alpha_values = [i for i in np.arange(0, 2, 0.1)]
# print(alpha_values)
#
# bits = '10010011011100100110101010101011110000011111100001111000100111011111001010110101001111000111000011100111111110001110001010110001'
#
# print(len(bits))
# print(1e3)

def normalize(array, x, y):
    m = array.min()
    range = array.max() - m
    array_temp = (array - m) / range

    range2 = y - x
    df_norm = (array_temp * range2) + x

    return df_norm

a = np.array([1, 2, 3, 10 , 50 , 20 , 30])
b = normalize(a, 0, 6)
print(b)
