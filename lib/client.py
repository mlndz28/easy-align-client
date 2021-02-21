import requests

def request_alignment(audio_file, transcript):
	r = requests.post('http://localhost:7728/align', data={'transcript': transcript}, files={'audio': open(audio_file,'rb')})
	return r.json()
