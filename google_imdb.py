# -*- coding: utf-8 -*- 
from grab import Grab,GrabTimeoutError
import re
from model import Movie,TVShow
from time import sleep
from random import randint

class GoogleImdb:
	@staticmethod
	def search_imdbid_on_google(title):
		g = Grab()
		url = 'www.google.com.br/search?q='
		query = title.replace(' ','+')
		query += ('+IMDB')
		try:
			g.go( url + query )
		except GrabTimeoutError as e:
			return None
		search_result = g.doc('//a[contains(@class, "l")]/@href').text_list()
		imdb_ids = []
		for item in search_result:
			list_found = re.findall(r'www.imdb.com/title/tt[0-9]*',item)
			if len(list_found) > 0:
				for imdb in list_found:
					imdb_ids.append(re.findall(r'tt[0-9]*',imdb)[0])

		if len(imdb_ids) > 0:
			return imdb_ids[0]
		return None


def finder():
	movie_list = Movie.select().where(Movie.imdb_id >> None)
	for movie in movie_list:
		imdb_id = GoogleImdb.search_imdbid_on_google(movie.title)
		print imdb_id
		movie.imdb_id = imdb_id
		movie.save()
		sleep(randint(2, 9))

finder()