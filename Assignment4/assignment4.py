from scipy.io import wavfile
import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt

midi_numbers = [60, 62, 64, 65, 67, 69, 71, 72, 72, 0, 67, 0, 64, 0, 60]
sampling_rate = 8000
duration = 0.25


def main():
    #generate, save and plot notes for part1
    part1 = generate_notes(midi_numbers, 5)
    scipy.io.wavfile.write("notes.wav", int(sampling_rate), part1)
    plot_mag_spec(part1, 'spectrogram-notes.png')

    #create an ADSR envelope with [0.7, 0.01, 0.265, 0.025] and sustain level at 0.3 to mimic violin sound
    env = ADSR_env(sampling_rate*duration, 0.7, 0.01, 0.265, 0.025, 0.3)
    # generate, save and plot notes for part2
    part2 = generate_enveloped_notes(midi_numbers, 5, env)
    scipy.io.wavfile.write("notes_adsr.wav", int(sampling_rate), part2)
    plot_mag_spec(part2, 'spectrogram-notes-adsr.png')


#create ADSR envelope according to the parameters given
def ADSR_env(sample, a, d, s, r, sustain_level):
    attack = a * sample
    decay = d * sample
    sustain = s * sample
    release = r * sample

    A = np.linspace(0.0, 1.0, attack)
    D = np.linspace(1.0, sustain_level, decay)
    S = np.linspace(sustain_level, sustain_level, sustain)
    R = np.linspace(sustain_level, 0.0, release)

    env = np.concatenate((A, D, S, R))
    return env


#calculate the fundamental frequency using the formula given in the handout
def cal_fundamental_freq(num):
    if (num == 0):
        return 0
    else:
        return 440 * (pow(2, ((num - 69) / 12)))


#generate the sine wave with given frequency
def generate_sine(freq):
    period = np.arange(int(duration * sampling_rate))
    sin_wave = np.sin(period * (freq / sampling_rate) * (2 * np.pi) + 0)
    return sin_wave


#generate the notes
def generate_notes(midi_num, num_harmonics):
    notes = []
    for i in midi_num:
        freq = cal_fundamental_freq(i)
        note = np.zeros((num_harmonics, int(sampling_rate * duration)))
        for j in range(1, num_harmonics + 1):
            note[j - 1] = generate_sine(freq * j)
        sumed_notes = np.sum(note, axis=0) # sum up the harmonics with the fundamental note
        notes = np.concatenate((notes, sumed_notes))
    print(notes)
    return notes


#generate notes with envelope applied
def generate_enveloped_notes(midi_num, num_harmonics, env):
    notes = []
    for i in midi_num:
        freq = cal_fundamental_freq(i)
        note = np.zeros((num_harmonics, int(sampling_rate * duration)))
        for j in range(1, num_harmonics + 1):
            note[j - 1] = generate_sine(freq * j)
        sumed_notes = np.sum(note, axis=0) # sum up the harmonics with the fundamental note
        notes = np.concatenate((notes, sumed_notes * env))
    print(notes)
    return notes


#plot the spectraogram
def plot_mag_spec(notes, name):
    num_buffers = int(len(notes) / 256 - 1)
    buffers = np.zeros((num_buffers, 257))

    for i in range(num_buffers):
        start = i * 256
        end = i * 256 + 512
        slice = notes[start:end]
        fft = scipy.fftpack.fft(slice * np.blackman(512))
        fft = fft[:len(fft) / 2 + 1]
        magfft = np.abs(fft) / np.sum(np.blackman(512)) / 2
        mag = 20 * np.log10(magfft + pow(10, -10))
        buffers[i] = mag
    buffers = buffers.transpose()
    plt.title(name)
    plt.xlabel('Time (frames)')
    plt.ylabel('Frequency (bin)')
    plt.imshow(buffers, origin= 'lower')
    plt.savefig(name)


main()