import os, sys, json, requests

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from lib import audio
from lib import client

HOST = 'localhost'
PORT = 8827
OUTPUT_FOLDER = '../gen/'


'''
Analyze a list of audio files to get the average time
length of each phoneme (vowels in this example).
'''
def main():
	
	file_list = open('list.json','rb').read()
	files = json.loads(file_list)
	phones = phone_stats(files)
	fig = plot_vowels(phones)

	
	
	if not os.path.exists(OUTPUT_FOLDER):
		os.system('mkdir -p %s'%OUTPUT_FOLDER)

	fig.savefig("%s/vowel_stats.pdf"%(OUTPUT_FOLDER))
		
	#plt.show()
	
def phone_stats(files):
	phones = {}
	for f in files[:]:
		audio_path = f['audio']
		transcript_path = f['text']
		try:
			data = client.request_alignment(audio_path, open(transcript_path).read())
			if(data.get('error')==None):
				for item in data['item']:
					if item['name'] == 'phones':
						for interval in item['intervals']:
							if interval['text'] != '_':
								if interval['text'] in phones:
									phones[interval['text']]['count'] += 1
									phones[interval['text']]['length'] += interval['xmax'] - interval['xmin']
								else:
									phones[interval['text']] = {'count': 1, 'length': interval['xmax'] - interval['xmin']} 
		except FileNotFoundError:
			print("Can't find %s or %s"%(audio_path,transcript_path))
			raise
		except requests.exceptions.ConnectionError:
			print("Can't find server at %s:%s"%(HOST,PORT))
			raise
		except:
			print(sys.exc_info()[0])
			raise
	return phones

def plot_vowels(phonemes):
	labels = ['a','e','i','o', 'u']
	values = []
	for l in labels:
		if phonemes.get(l) != None:
			values.append(phonemes[l]['length'] / phonemes[l]['count'])
		else:
			labels.remove(l)
	fig, ax = plt.subplots()
	ax.barh(range(1,len(labels)+1), values, 0.2, align='center', color='black')
	ax.set_yticks(range(1,len(labels)+1))
	ax.set_yticklabels(labels)
	ax.invert_yaxis()
	ax.set_xlabel('average time [s]')
	ax.set_ylabel("vowels")

	return fig

if __name__ == '__main__':
	main()
