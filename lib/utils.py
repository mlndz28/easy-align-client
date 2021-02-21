import os

import numpy as np
import matplotlib.pyplot as plt

from lib import audio



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
	ax[0].plot(time, snd)

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
