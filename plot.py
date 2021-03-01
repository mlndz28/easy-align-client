import os, sys

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from lib import audio
from lib import client

sns.set()
sns.set_style('ticks')

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
	except FileNotFoundError:
		print("Can't find %s or %s"%(audio_path,transcript_path))
		return
	except requests.exceptions.ConnectionError:
		print("Can't find server at %s:%s"%(HOST,PORT))
		return
	except:
		print(sys.exc_info()[0])
		raise

	if not os.path.exists(OUTPUT_FOLDER):
		os.system('mkdir -p %s'%OUTPUT_FOLDER)

	fig = plot_alignment(snd, rate, data)
	fig.savefig("%s/%s_alignment.%s"%(OUTPUT_FOLDER, audio_path.split("/")[-1].split(".")[-2], OUTPUT_FORMAT))
		

def plot_alignment(snd, rate, data):
	fig = plt.figure()
	ax = [ plt.subplot2grid((len(data['item']) + 3, 1), (0, 0), rowspan=3) ]
	fig.subplots_adjust(hspace=0)
	time = audio._time_vector(snd, rate)
	x_start = time[np.where(snd > np.amax(snd)*0.1)[0][0]]
	x_start = x_start if x_start - len(snd)/rate*0.05 < 0 else x_start - len(snd)/rate*0.05 

	x_end = time[ -1 * np.where(snd[::-1] > np.amax(snd)*0.1)[0][0]]
	x_end = x_end if x_end + len(snd)/rate*0.05 > time[-1] else x_end + len(snd)/rate*0.05 
	ax[0].set_xlim([x_start, x_end])
	ax[0].set_ylabel("y(t)")
	ax[0].plot(time, snd, color='black')

	for i in range(3,len(data['item'])+3):
		ax.append(plt.subplot2grid((len(data['item']) + 3, 1), (i, 0), sharex = ax[0]))

	for i in range(len(data['item'])):
		ax[i+1].set_ylabel(data['item'][i]['name'], rotation = 0, labelpad=30, va='center')
		ax[i+1].set_yticks([])
		ax[i+1].set_ylim([0, 1])
		for interval in data['item'][i]['intervals']:
			xmin =  interval['xmin'] if interval['xmin'] > x_start else x_start
			xmax =  interval['xmax'] if interval['xmax'] < x_end else x_end
			if interval['text'] != '_': 
				ax[i+1].text(0.5*(xmin + xmax),  0.5, interval['text'], va="center", ha="center")
				if xmax != x_end: 
					ax[i+1].axvline(xmax, color='black', lw=0.75)

	ax[-1].set_xlabel("time [s]")

	fig.set_size_inches(18, 9)
	return fig


if __name__ == '__main__':
	main()
