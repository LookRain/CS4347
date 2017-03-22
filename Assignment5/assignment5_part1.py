import numpy as np
import scipy.io.wavfile
import scipy.signal
import matplotlib.pyplot as plt


FREQUENCY = 1000.0
MAX_AMPLITUDE = 0.5
SAMPLING_RATE = 44100
DURATION = 1.0
#calculated max number of sine waves according to nyquist's theorem
M = int(np.floor(SAMPLING_RATE / 2 / FREQUENCY))
LENGTH = 8192


def main():
    #generate constructed and perfect sawtooth waves
    constructed_sawtooth_wave = construct_sawtooth()
    perfect_sawtooth_wave = perfect_sawtooth()
    #write them to wav files
    scipy.io.wavfile.write("constructed_sawtooth.wav", SAMPLING_RATE, constructed_sawtooth_wave)
    scipy.io.wavfile.write("perfect_sawtooth.wav", SAMPLING_RATE, perfect_sawtooth_wave)
    #plot the time domain graph
    plot_time_domain(constructed_sawtooth_wave, perfect_sawtooth_wave)
    #generate and plot the db_mag fft graph
    constructed_spec =  get_power_spec(constructed_sawtooth_wave)
    perfect_spec = get_power_spec(perfect_sawtooth_wave)
    plot_db_mag(constructed_spec, perfect_spec)


#construct the sawtooth wave using the formula given in handout
def construct_sawtooth():
    time = np.arange(0, DURATION, 1 / SAMPLING_RATE)
    wave = np.zeros(len(time))

    for i in range(1, M + 1):
        temp_wave = (1.0 / i) * np.sin(i * 2.0 * np.pi * time * FREQUENCY)
        wave = wave + temp_wave

    wave = wave * (-2.0 * MAX_AMPLITUDE / np.pi)
    return wave


def perfect_sawtooth():
    time = np.arange(0, DURATION, 1 / SAMPLING_RATE)
    perfect_wave = MAX_AMPLITUDE * scipy.signal.sawtooth(FREQUENCY * 2.0 * np.pi * time)
    return perfect_wave


def plot_time_domain(constructed, perfect):
    plt.xlabel("Time")
    plt.ylabel("Amplitude")

    plt.plot(constructed, c="blue", label="Reconstructed Sawtooth")
    plt.plot(perfect, c="red", label="Perfect Sawtooth")

    plt.legend()
    plt.xlim(0, 250)
    plt.savefig('Time-Domain Waves.png')


def get_power_spec(wave):
    wave = wave[:LENGTH]
    window = np.blackman(len(wave))
    fft = np.fft.fft(wave * window)
    fft = fft[:len(fft) / 2 + 1]
    magfft = np.abs(fft) / (np.sum(window) / 2.0)
    epsilon = np.power(10.0, -10)
    power_spec = 20.0 * np.log10(magfft + epsilon)
    return power_spec


def plot_db_mag(constructed, perfect):
    plt.clf()
    plt.xlabel("FFT bin")
    plt.ylabel("dB")
    plt.plot(constructed, c="blue", label="Reconstructed Sawtooth")
    plt.plot(perfect, c="red", label="Perfect Sawtooth")

    plt.legend()
    plt.xlim(0, 4000)
    plt.title('Sawtooth wave reconstruction with 22 sine wave')
    plt.savefig('dB-magnitude FFT.png')


main()