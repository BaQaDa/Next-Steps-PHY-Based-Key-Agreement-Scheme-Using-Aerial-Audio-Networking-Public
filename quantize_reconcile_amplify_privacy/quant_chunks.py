import numpy as np
import pandas as pd
import os

##  Detects step in time series
#   @param df is the data frame containing the time series
def detect_step_in_time_series(df):
    mdary = np.asarray(df['Amp'])
    dary = np.array([*map(float, mdary)])
    dary -= np.average(dary)
    step = np.hstack((np.ones(len(dary)), -1 * np.ones(len(dary))))
    dary_step = np.convolve(dary, step, mode='valid')
    # get the peak of the convolution, its index
    step_indx = np.argmax(dary_step)
    return step_indx


##  Extracts the step area from the time series
#   @param df           is the data frame containing the time series
#   @param step_index   is the step index detected in detect_step_in_time_series
#   @param step_size    is the step (tone) duration
def extract_step_df(df, step_indx, step_size):
    post_step_df = df[df['Time'] >= step_indx]
    step_df = post_step_df[post_step_df['Time'] <= (step_indx + step_size)]
    return step_df

##  Concates consecutive probes into one time series
def concate_probes(path, file_name, range_start, range_end, step_size):
    step_amp = list()
    for exp_num in range(range_start, range_end):
        file = os.path.join(path, str(exp_num) + file_name + '.csv')
        df = pd.read_csv(file)
        step_index = detect_step_in_time_series(df)
        step_df = extract_step_df(df, step_index, step_size)
        step_amp += step_df['Amp'].tolist()
    return step_amp


##  Divides the concatenated time series into smaller chunks of size chunk_size
#   note that it can be (chunk_size = step_size)
#   @param list         is the list to be divided
#   @param chunk_size   is the chunk size
def chunks(concatenated_step_amp, chunk_size):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(concatenated_step_amp), chunk_size):
        yield concatenated_step_amp[i:i + chunk_size]


##  Computes quantization thresholds of a chunk
#   @param alpha >= 0.2
#   @returns q_pos, q_neg
def get_thresholds(chunk, alpha):
    mean = np.mean(chunk)
    stdDev = np.std(chunk)
    q_pos = mean + alpha * stdDev
    q_neg = mean - alpha * stdDev
    return q_pos, q_neg


##  Quantization function
#   @param estimate     is the value to be quantized
#   @param q_pos  is the positive threshold
#   @param q_neg  is the negative threshold
def quantize(estimate, q_pos, q_neg):
    if estimate > q_pos:
        return 1
    elif (estimate < q_neg):
        return 0
    else:
        return 2  # represent None


##  Apply quantization on the chunks of concatenated time series
#   @param chunked_step_amp is the time series to be quantized
#   returns concatenated quantized time series
def quantize_chunks(chunked_step_amp, alpha):
    qts = list()
    for chunk in chunked_step_amp:
        q_pos, q_neg = get_thresholds(chunk, alpha)
        qts += [quantize(amp, q_pos, q_neg) for amp in chunk]
    return qts


#   Get indices of estimates between q+, q-
#   @param quantized_time_series is the quantized time series from which
#   we will drop estimates between q+, q-
#   @returns drop_indices : a list of the dropped estimates' indices
def getDroppingIndices(quantized_time_series):
    dropped_indices = [i for i, x in enumerate(quantized_time_series) if x == 2]
    return dropped_indices


##  Compute the union of dropped estimates' indices lists (init_drop_indices, resp_drop_indices)
#   @returns dropped_indices_union
def get_dropped_union(dropped_indices_1, dropped_indices_2):
    dropped_indices_union = set().union(dropped_indices_1, dropped_indices_2)
    return list(dropped_indices_union)


##  Applies the whole quantization process on files of both responder, initiator
#   @param range_start   is the number of the first file conducted in experiment
#   @param range_end     is the number of the last file conducted in experiment
#   @param alpha >= 0.2  for the thresholds computation
#   @param chunk_size   is the chunk size into which the concatenated time series will be divided.
#   @returns drop_indices : a list of the dropped estimates' indices
#   @returns cleaned_qts  : the cleaned quantized_time_series after dropping the values
def quantization(path, range_start, range_end, party_name1, party_name2, step_size, chunk_size, alpha, start_freq, freq_num, freq_gap):

    file_name1 = party_name1 + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)
    file_name2 = party_name2 + str(start_freq) + '-' + str(freq_num) + '-' + str(freq_gap)

    concatenated_step_amp_resp = concate_probes(path, file_name1, range_start, range_end, step_size)
    concatenated_step_amp_init = concate_probes(path, file_name2, range_start, range_end, step_size)

    chunked_step_amp_resp = chunks(concatenated_step_amp_resp, chunk_size)
    chunked_step_amp_init = chunks(concatenated_step_amp_init, chunk_size)
    print("concatenated_step_amp_resp = ", concatenated_step_amp_resp)
    qts_resp = quantize_chunks(chunked_step_amp_resp, alpha)
    qts_init = quantize_chunks(chunked_step_amp_init, alpha)

    dropped_indices_resp = getDroppingIndices(qts_resp)
    dropped_indices_init = getDroppingIndices(qts_init)
    dropped_indices_union = get_dropped_union(dropped_indices_init, dropped_indices_resp)

    ## Get the cleaned quantized time series after dropping estimates correspond to inidces in dropped_indices_union
    cleaned_qts_resp = qts_resp.copy()
    for index in sorted(dropped_indices_union, reverse=True):
        del cleaned_qts_resp[index]

    ## Get the cleaned quantized time series after dropping estimates correspond to inidces in dropped_indices_union
    cleaned_qts_init = qts_init.copy()
    for index in sorted(dropped_indices_union, reverse=True):
        del cleaned_qts_init[index]

    ## to plot in case of one experiment:##  one window: same plot axises
    # plt.figure()
    # plt.title("responder and initiator amps")
    # plt.plot(step_amp_resp)
    # plt.plot(step_amp_init)
    # plt.show(plt.grid(True))

    return cleaned_qts_resp, cleaned_qts_init


if (__name__) == "__main__":

    path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\Amplitude Expers\\quant exp\\quant ASBG\\2-quant-250-15"

    first_file_num = 0
    last_file_num = 20
    step_size = 1000
    chunk_size = 25
    alpha = 0.8

    cleaned_qts_resp, cleaned_qts_init = quantization(path, first_file_num, last_file_num, 'init_', 'second_', step_size,
                                                                   chunk_size, alpha)
    print(cleaned_qts_resp)
    print(len(cleaned_qts_resp))

    print(cleaned_qts_init)
    print(len(cleaned_qts_init))
