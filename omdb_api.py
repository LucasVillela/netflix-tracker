from credentials import omdb_api_key
from model import OMDB,Actor,Movie,OMDB_Actors
from peewee import DoesNotExist
from utils import get_url
import urllib2
import json


class OMDB_API:

	def __init__(self):
		self.OMDB_URL = 'http://www.omdbapi.com/?i=xxxx&apikey=yyyy'
		self.api_key = omdb_api_key()

	def omdb_model(self, data, existing_omdb):
		omdb = None		
		if existing_omdb is None:
			omdb = OMDB()
		else:
			omdb = existing_omdb
		if data.has_key('Plot'):
			omdb.plot = data['Plot']
		if data.has_key('Rated'):
			omdb.rated = data['Rated']
		if data.has_key('DVD'):
			omdb.dvd = data['DVD']
		if data.has_key('Writer'):
			omdb.writer = data['Writer']
		if data.has_key('Production'):
			omdb.production = data['Production']
		if data.has_key('imdbVotes'):
			omdb.imdb_votes = data['imdbVotes']
		if data.has_key('Website'):
			omdb.website = data['Website']
		if data.has_key('Poster'):
			omdb.poster = data['Poster']
		if data.has_key('Director'):
			omdb.director = data['Director']
		if data.has_key('Released'):
			omdb.released = data['Released']
		if data.has_key('Awards'):
			omdb.awards = data['Awards']
		if data.has_key('Genre'):
			omdb.genre = data['Genre']
		if data.has_key('imdbRating'):
			omdb.imdb_rating = data['imdbRating']
		if data.has_key('Language'):
			omdb.language = data['Language']
		if data.has_key('Country'):
			omdb.country = data['Country']
		if data.has_key('BoxOffice'):
			omdb.box_office = data['BoxOffice']
		if data.has_key('Metascore'):
			omdb.metascore = data['Metascore']
		if data.has_key('Year'):
			omdb.year = data['Year']
		if data.has_key('Title'):
			omdb.title = data['Title']
		if data.has_key('Runtime'):
			omdb.runtime = data['Runtime']
		if data.has_key('imdbID'):
			omdb.imdb_id = data['imdbID']
		print omdb.title

		if existing_omdb is not None:
			omdb.save()
		else:
			omdb.save(force_insert=True)

	def actor_model(self, data):
		if data.has_key('Actors'):
			actor_string = data['Actors']
			actors = []
			actors_array = actor_string.split(',')
			for x in actors_array:
				result = Actor.select().where(Actor.name == x.strip()).execute()
				if len(result) == 0:
					actor = Actor()
					actor.name = x.strip()
					actors.append(actor)
					actor.save()
			for x in actors:
				relationship = OMDB_Actors()
				relationship.imdb_id = data['imdbID']
				actor = Actor.get(Actor.name == x.name)
				relationship.actor = actor.id
				relationship.save()

	def get_movie_info(self, imdb_id):
		request = urllib2.Request(get_url(self.OMDB_URL, imdb_id, self.api_key))
		handler = urllib2.HTTPHandler()
		opener = urllib2.build_opener(handler)
		response = opener.open(request)

		if response.code == 200:
			data = json.loads(response.read())
			omdb = None
			try:
				omdb = OMDB.get( OMDB.imdb_id == data['imdbID'])
				self.omdb_model(data, omdb)
				self.actor_model(data)
			except DoesNotExist as e:
				self.omdb_model(data, omdb)
				self.actor_model(data)

def finder():
	movie_list = Movie.select().where(Movie.imdb_id != None)
	omdbapi = OMDB_API()
	for movie in movie_list:
		omdbapi.get_movie_info(movie.imdb_id)


finder()


