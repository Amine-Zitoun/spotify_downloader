import requests
from bs4 import BeautifulSoup as bs
import youtube_dl
from youtube_search import YoutubeSearch
import os
url ="https://open.spotify.com/playlist/1qGdNJZENqM0UfKxC7i09i?si=fHI7_fKqSPiaCqUWJHKGeA"
def get_tracks(url):
	res = requests.get(url)
	html = bs(res.text,'lxml')
	tracks = [x.text for x in html.find_all('span',{'class': 'track-name'})]
	ppl = [x.a.span.text for x in html.find_all('div',{'class': 'tracklist-col name'})]
	name = html.find_all('h1')[0].text
	print(name)
	res_dict = dict(zip(ppl,tracks))
	return res_dict,name


def search_song(song):
	print("searching song: "+song)
	results = YoutubeSearch(song, max_results=10).to_dict()
	return "https://www.youtube.com/"+results[0]['link']

def download_songs(tracklist,playlist_name):
	print("PLAYLIST NAME: ",playlist_name)
	for song in tracklist:
		link = search_song(song)
		SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/'+playlist_name

		ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
				}],
				'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s',

		  	}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])

def main():
	print("***************MADE BY YA BOI ZITOUNNNN************")
	url = input("Enter url: ")
	#url = "https://open.spotify.com/playlist/3sWZfGIwY3mqncSoc6hk9s?si=wP3euTolTKSRQ8x36p7c1g"
	res,playlist_name = get_tracks(url)
	songs =[]
	for pp,track in zip(res.keys(),res.values()):
		songs.append(pp+ " "+track)
	download_songs(songs,playlist_name)	
	input(" ")
main()
