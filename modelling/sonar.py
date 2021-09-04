# =============================================================================
# ARTY A7 FPGA SONAR modelling
# 
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy import signal

def gen_single_chirp(f_min, f_max, duration, fs):
    """
    Generates linear chirp signal based of equation detailed here: 
        https://en.wikipedia.org/wiki/Chirp#Linear

    Parameters
    ----------
    f_min : Integer
        lower/starting frequency of chirp signal.
    f_max : Integer
        Upper frequency of chirp signal.
    duration : Float
        Duration of chirp signal, in seconds.
    fs : Integer
        Sampling frequency in samples per second.

    Returns
    -------
    chirp signal, windowed with hamming window

    """
    # time index
    t = np.linspace(0, duration, int(fs*duration));
    chirp_rate = (f_max - f_min) / duration
    chirp = np.sin(2*np.pi*(chirp_rate / 2 * t ** 2 + f_min * t))
    chirp = chirp * np.hamming(np.size(chirp))
    return chirp

def gen_sonar_chirp(f_min, f_max, duration, fs, n_chirps):
    single_chirp = gen_single_chirp(f_min, f_max, duration, fs)
    # 4 times per seconds approx
    zeros = np.zeros(fs//4)
    base_sonar_sig = np.concatenate((zeros, single_chirp))
    sonar_chirp = []
    for i in range(n_chirps):
        sonar_chirp = np.concatenate((sonar_chirp, base_sonar_sig))
    return sonar_chirp

def play_rec_sonar(f_min, f_max, duration, fs, n_chirps):    
    sonar_chirp = gen_sonar_chirp(f_min, f_max, duration, fs, n_chirps)
    recorded_data = sd.playrec(sonar_chirp, fs, channels=1)
    sd.wait()
    np.save("test_rec_data", recorded_data)

def plot_chirp(f_min, f_max, duration, fs):
    t = np.linspace(0,duration,int(fs*duration));
    chirp_sig = gen_single_chirp(f_min, f_max, duration, fs)
    plt.plot(t, chirp_sig)
    plt.title('Chirp signal (%d-%d Hz)' %(f_min, f_max))
    plt.xlabel('time (t)')
    plt.ylabel('Amplitude')
    
def plot_chirp_autocorr(f_min, f_max, duration, fs, n_plot_samples=100):
    chirp_sig = gen_single_chirp(f_min, f_max, duration, fs)
    auto_corr = signal.correlate(chirp_sig, chirp_sig)
    middle_idx = len(auto_corr) // 2
    plt.plot(auto_corr[middle_idx - n_plot_samples // 2 : middle_idx + n_plot_samples // 2 ])
    plt.title('Autocorrelation of Chirp Signal (%d-%d Hz)' %(f_min, f_max))

def plot_chirp_autocorr_filtered(f_min, f_max, duration, fs, num_taps, cutoff_hz, n_samples=100):
    chirp_sig = gen_single_chirp(f_min, f_max, duration, fs)
    auto_corr = signal.correlate(chirp_sig, chirp_sig)
    abs_auto_corr = np.abs(auto_corr) 
    filt_coeffs = signal.firwin(num_taps, cutoff_hz/fs)
    filtered_autocorr = np.convolve(abs_auto_corr, filt_coeffs)
    middle_idx = len(filtered_autocorr) // 2
    plt.plot(filtered_autocorr[middle_idx - n_samples // 2 : middle_idx + n_samples // 2 ])
    plt.title('Filtered Absolute Autocorrelation of Chirp Signal')

if __name__ == "__main__": 
    fs = 44100
    f_min = 200
    f_max = 12000
    duration = 256/fs #roughly 0.0058 in seconds
    t = np.linspace(0,duration,int(fs*duration));
    n_chirps = 16
    chirp_sig = gen_single_chirp(f_min, f_max, duration, fs)

    run_sonar = False
    
    if run_sonar:
        play_rec_sonar(f_min, f_max, duration, fs, n_chirps)
    
    try:
        test_rec = np.load("test_rec_data.npy")[:,0]
    except FileNotFoundError:
        print("Sonar file not generated yet. Set run_sonar variable to true to play and record sonar signal first.")
    
    # Matched filter
    corr_test_rec = signal.correlate(test_rec, chirp_sig)
    # Take absolute value
    abs_test_rec = np.abs(corr_test_rec)
    n_samples = 100
    #low pass filter the signal
    num_taps = 101
    cutoff_hz = 2000
    filt_coeffs = signal.firwin(num_taps, cutoff_hz/fs)
    lf_sig = signal.fftconvolve(abs_test_rec, filt_coeffs)
    # Plot result
    plt.figure(figsize=(20,5))
    plt.plot(lf_sig)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    