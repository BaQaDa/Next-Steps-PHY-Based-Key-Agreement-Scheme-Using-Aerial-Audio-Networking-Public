from for_printing.binList_to_dec import bin_list_to_dec


def dec_to_bin_list(dec_num, required_list_len):
    bin_from_dec = bin(dec_num)
    bin_from_dec_str = str(bin_from_dec[2:])
    bin_from_dec_list = list(bin_from_dec_str)
    binList = [ord(x)%2 for x in bin_from_dec_list]
    missed_zeros_num = required_list_len - len(binList)
    if (missed_zeros_num > 0):
        binList = [0 for i in range(missed_zeros_num)] + binList
        print("appended", missed_zeros_num, "zero")
    return binList

if (__name__) == "__main__":

    Final_Shared_Key = [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    Final_Shared_Key_Dec_AB = bin_list_to_dec(Final_Shared_Key)
    print("key binList after privAmp: ", Final_Shared_Key)
    print("from binList to dec: ", Final_Shared_Key_Dec_AB)
    Final_Shared_Key_Dec_AB_bin_list = dec_to_bin_list(Final_Shared_Key_Dec_AB, len(Final_Shared_Key))
    # diff_left_zeros = len(Final_Shared_Key) - len(Final_Shared_Key_Dec_AB_bin_list)
    # if (diff_left_zeros > 0):
    #     for i in range(len(Final_Shared_Key_Dec_AB)):
    #         Final_Shared_Key_Dec_AB_bin_list = [0] + Final_Shared_Key_Dec_AB_bin_list
    print("from dec to binList: ", Final_Shared_Key_Dec_AB_bin_list)

    if (Final_Shared_Key == Final_Shared_Key_Dec_AB_bin_list):
        print("successful conversion")
