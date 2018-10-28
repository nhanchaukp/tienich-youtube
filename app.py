import json, requests, sys
import os
import youtube_dl
from flask import Flask, render_template, json, request, send_file,request
import urllib
from bs4 import BeautifulSoup
import datetime
import re

year = datetime.date.today().year

# Flask app should start in global layout
app = Flask(__name__)

def make_savepath(title):
    return os.path.join("%s.mp3" % (title.replace("mp3","")))

@app.route('/', methods=['GET'])
url = 'https://www.youtube.com/watch?v=HXkh7EOqcQ4'
options = {
    'format': 'bestaudio/best',
	'outtmpl': '%(id)s'
}

ydl = youtube_dl.YoutubeDL(options)
song_name = ydl.extract_info(url, download=False)
savepath = make_savepath(song_name['title'].replace(" ", ""))
savepath = re.sub('[^A-Za-z0-9]+', '', savepath)
savepath = make_savepath((savepath))
with ydl:
	result = ydl.extract_info(url, download=True)
	os.rename(result['id'], savepath)
	print("Downloaded and converted %s successfully!" % savepath)
	try:
		send_file(savepath,savepath, as_attachment=True)
	except Exception as e:
		print(str(e))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print("Starting app on port %d" % port)
app.run(debug=False, port=port, host='0.0.0.0')
