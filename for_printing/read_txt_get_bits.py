import re

def find_phrase_line(file_name, phrase):
    with open(file_name) as myFile:
        for num, line in enumerate(myFile, 1):
            if phrase in line:
                phrase_line_num = num
                phrase_line = line
                break
        return phrase_line

def get_num_after_phrase_in_string(string):
    num = re.search('(\d+)', string, re.IGNORECASE)
    num1 = int(num.group(1))
    return num1

def get_num_after_phrase_in_file(file_name, phrase):
    line = find_phrase_line(file_name, phrase)
    num = get_num_after_phrase_in_string(line)
    return num

def dec_to_bin_list(dec_num):
    bin_from_dec = bin(dec_num)
    bin_from_dec_str = str(bin_from_dec[2:])
    bin_from_dec_list = list(bin_from_dec_str)
    binList = [ord(x)%2 for x in bin_from_dec_list]
    return binList

if (__name__) == "__main__":

    output_file = 'C:\\Users\\Dania\\PycharmProjects\\audio_key\\quantize_reconcile_amplify_privacy\\out.txt'
    phrase = 'Final_Shared_Key_Dec'
    num = get_num_after_phrase_in_file(output_file, phrase)
    print(num)
