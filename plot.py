import os, sys

import matplotlib.pyplot as plt
import seaborn as sns

from lib import audio
from lib import client
from lib import utils

HOST = 'localhost'
PORT = 8827
OUTPUT_FOLDER = 'gen'
OUTPUT_FORMAT = 'pdf'


'''
Align and plot a vocal audio and its transcription.
An Easy Align server needs to be running on HOST:PORT 
'''
def main():
	if len(sys.argv) != 3 or any(a == '-h' or a == '--help' for a in sys.argv):
		print('Usage: %s <audio file in WAV format> <text file for the transcription>'%(sys.argv[0]))
		return

	audio_path = sys.argv[1]
	transcript_path = sys.argv[2]
	
	rate, snd = audio.read_wav(audio_path)
	snd, max = audio.normalize(snd)

	try:
		data = client.request_alignment(audio_path, open(transcript_path).read())
	except:
		print("Can't find server at %s:%s"%(HOST,PORT))
		return

	if not os.path.exists(OUTPUT_FOLDER):
		os.system('mkdir -p %s'%OUTPUT_FOLDER)

	fig = utils.plot_alignment(snd, rate, data)
	fig.savefig("%s/%s_alignment.%s"%(OUTPUT_FOLDER, audio_path.split("/")[-1].split(".")[-2], OUTPUT_FORMAT))
		

if __name__ == '__main__':
	main()
