import os

from pydub import AudioSegment
from scipy.io import wavfile

'''
For information about the _0_signal_processing_functions usage, check: 
1.  https://github.com/jiaaro/pydub/issues/169
2.  https://pypi.org/project/pydub/

@param 
    sound               is a pydub.AudioSegment
    silence_threshold   is in dB ( find the average loudness of the sound in dBFS
                        (if for e.g -19 then quieter than the default silence_thresh of -16dBFS)
    chunk_size          is in ms
@works
    iterate over chunks until you find the first one with sound
'''


def detect_leading_silence(sound, silence_threshold, chunk_size=5):
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


'''
@param 
    input_file      is the file containing silence and sound together  
    output_file     is an empty file to be written with the sound only after removing the silence
'''


def remove_detected_silence(input_file, output_file, silence_threshold):
    sound = AudioSegment.from_file(input_file, format="wav")
    print('To modify silence_thresh parameter; good to know that average loudness of your file sound : ', sound.dBFS, 'dBFS')
    print('while default silence_thresh : -16 dBFS')
    start_trim = detect_leading_silence(sound, silence_threshold)
    end_trim = detect_leading_silence(sound.reverse(), silence_threshold)
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]
    trimmed_sound.export(output_file, format="wav")


if __name__ == '__main__':
    file_name = '1-init-4000-15-250'

    input_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\recordings\\initiator"
    input_file = os.path.join(input_path, file_name + '.wav')

    sound_output_path = "D:\\India-\\Ph.D\\3rd sem\\projects1\\python\\input_output_files\\sound_only\\initiator_sound"
    sound_output_file = os.path.join(sound_output_path, file_name + '.wav')

    # apply silence removing and write the sound into the output file
    remove_detected_silence(input_file, sound_output_file, -45.5)

    # now, we can deal with and process the resultant sound file
    sampFreq, samples = wavfile.read(sound_output_file)
