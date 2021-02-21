import numpy as np
import scipy.io.wavfile as wav

def _time_vector(audio, rate):
	size = len(audio)
	return np.linspace(0., 1.*size/rate, size)

def read_wav(filepath):
	rate, audio = wav.read(filepath)	# returns the audio's sampling rate and its data
	return rate, audio

def normalize(audio):
	max = np.amax(audio) if np.amax(audio) > abs(np.amin(audio)) else abs(np.amin(audio))
	audio = audio/float(max) # normalized vector
	return audio, max
