def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]
    # Join list items using join()
    res = int("".join(s))
    return (res)

def convert_to_str(list):
    # Converting integer list to string list
    s = [str(i) for i in list]
    res = "".join(s)
    return (res)

def binaryToDecimal(binary):
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return (decimal)

def bin_list_to_dec(bin_list):
    bin_str = convert(bin_list)
    dec_num = binaryToDecimal(bin_str)
    return dec_num


if (__name__) == "__main__":

    bin_list = [0, 1, 0, 1, 0]
    print("bin_list", bin_list)

    dec_num = bin_list_to_dec(bin_list)
    print("dec_num", dec_num)

    bin_from_dec = bin(dec_num)
    bin_from_dec_str = str(bin_from_dec[2:])
    print(type(bin_from_dec))
    bin_from_dec_list = list(bin_from_dec_str)
    print("dec_num to bin list", bin_from_dec_list)
    print([ord(x)%2 for x in bin_from_dec_list])