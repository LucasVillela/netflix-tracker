# -*- coding: utf-8 -*- 
import urllib2
import urllib
import json
from model import Movie,TVShow,WhereTo
from model import create_tables
from genre_list import get_genre_list
from credentials import netflix_id, api_url


#create_tables()



def main():
	list_total = float(len(get_genre_list()))
	for index, genre in enumerate(get_genre_list()):
		max_video = 600
		should_continue = True
		while should_continue:
			has_finished = sucker_punch(genre, max_video)
			if not has_finished:
				max_video += 600
			else:
				should_continue = False

def sucker_punch(genre,max_video):
	method = 'POST'
	url = api_url()
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	json_model = {"paths":[["genres",genre,"su",{"from":max_video-599,"to":max_video},["summary","title","userRating"]]]}
	data = json.dumps(json_model)
	request = urllib2.Request(url, data=data)
	request.add_header('Content-Type','application/json')
	request.add_header('Cookie', netflix_id())
	request.get_method = lambda: method
	connection = opener.open(request)

	if connection.code == 200:
		data = json.loads(connection.read())
		value = data['value']
		counter = -1
		if value.has_key('videos'):
			videos = value['videos']
			for video in videos.keys():
				if video.isdigit():
					if videos[video].has_key('summary') and videos[video]['summary']['type'] == 'movie':
						WhereTo.save_movie(videos[video])
					else:
						WhereTo.save_show(videos[video]) 
					counter += 1
		print genre
		if counter == 600:
			return False
		return True

main()