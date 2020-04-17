from quantize_reconcile_amplify_privacy.cascade import find_mismatch_num, bit_error_rate
from quantize_reconcile_amplify_privacy.quant_chunks import quantization
from pylab import *

if (__name__) == "__main__":
    print('Enter your choice: 1 for KEY_AB, 2 for KEY_AC')
    input1 = int(input())

    path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Conference\\conf2"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Corridor"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\Locality"
    # path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Exps_paper\\room-multi-freq"
    chunk_size_values = [10, 15, 20, 25, 30, 35, 45, 50 ,60, 70]
    # alpha_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
    alpha_values = [i for i in np.arange(0.2, 1, 0.001)]
    pe_values1, pe_values2 = list(), list()
    num_bits_values = list()

    '''____________________ alpha vs. Pe ____________________'''

    for alpha in alpha_values:
        start_freq, freq_num, freq_gap = 16000, 1, 0

        first_file_num = 1
        last_file_num = first_file_num + 1
        chunk_size, step_size, alpha = 60, 1000, alpha

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                              step_size, chunk_size, alpha,
                                                              start_freq, freq_num, freq_gap)
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        pe_values1.append(Pe)

    plt.figure(1)
    plt.plot(alpha_values, pe_values1)
    plt.xlabel(r'Value of $\alpha$')
    plt.ylabel('Bit Mismatch Rate')

    '''____________________ chunk_size vs. Pe ____________________'''

    for chunk_size in chunk_size_values:
        start_freq, freq_num, freq_gap = 16000, 1, 0

        first_file_num = 6
        last_file_num = first_file_num + 1
        chunk_size, step_size, alpha = chunk_size, 1000, 0.2

        cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'Alice', 'Bob',
                                                              step_size, chunk_size, alpha,
                                                              start_freq, freq_num, freq_gap)
        Pe = bit_error_rate(cleaned_qts_init, cleaned_qts_resp)
        pe_values2.append(Pe)
        num_bits = len(cleaned_qts_resp)
        num_bits_values.append(num_bits)

    plt.figure(2)
    plt.plot(chunk_size_values, pe_values2)
    plt.xlabel('chunk-size')
    plt.ylabel('Bit Mismatch Rate')

    '''____________________ chunk_size vs. num_bits generated at quantization ____________________'''

    plt.figure(3)
    plt.plot(chunk_size_values, num_bits_values)
    plt.xlabel('chunk-size')
    plt.ylabel('number of bits after quantization')
    plt.show()