from peewee import *
from datetime import date
from datetime import datetime

psql_db = PostgresqlDatabase(
	'netflix',  # Required by Peewee.
	user='postgres',  # Will be passed directly to psycopg2.
	password='postgres',  # Ditto.
	host='localhost',  # Ditto.
)



class BaseModel(Model):
	class Meta:
		database = psql_db


class Movie(BaseModel):
	movie_id = IntegerField()
	title = TextField()
	updated_at = DateTimeField()
	created_at = DateTimeField()
	imdb_id = TextField()

	@staticmethod
	def new_movie(obj):
		movieid = obj['summary']['id']
		title = obj['title']
		movie = Movie(movie_id=movieid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		movie.save()

	@staticmethod
	def update_movie(obj):
		movie = Movie.get( Movie.movie_id == obj['summary']['id'])
		movie.updated_at = datetime.now()
		movie.save()



class TVShow(BaseModel):
	tvshow_id = IntegerField()
	title = TextField()
	total_seasons = IntegerField(default=1)
	updated_at = DateTimeField()
	created_at = DateTimeField()
	imdb_id = TextField()

	@staticmethod
	def new_show(obj):
		tvshowid = obj['summary']['id']
		title = obj['title']
		tvshow = TVShow(tvshow_id=tvshowid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		tvshow.save()

	@staticmethod		
	def update_show(obj):
		tvshow = TVShow.get( TVShow.tvshow_id == obj['summary']['id'])
		tvshow.updated_at = datetime.now()
		tvshow.save()

class Actor(BaseModel):
	name = TextField(unique = True)

class OMDB(BaseModel):
	imdb_id = TextField(primary_key = True, unique = False)
	title = TextField(null=True)
	year = TextField(null=True)
	rated = TextField(null=True)
	released = TextField(null=True)
	runtime = TextField(null=True)
	genre = TextField(null=True)
	director = TextField(null=True)
	writer = TextField(null=True)
	plot = TextField(null=True)
	language = TextField(null=True)
	country = TextField(null=True)
	awards = TextField(null=True)
	poster = TextField(null=True)
	metascore = TextField(null=True)
	imdb_rating = TextField(null=True)
	rotten_tomatoes = TextField(null=True)
	metacritic = TextField(null=True)
	imdb_votes = TextField(null=True)
	dvd = TextField(null=True)
	production = TextField(null=True)
	website = TextField(null=True)

class OMDB_Actors(BaseModel):
	imdb_id = ForeignKeyField(OMDB, related_name = 'owner')
	actor = ForeignKeyField(Actor, related_name = 'child')

class WhereTo():

	@staticmethod
	def save_movie(obj):
		try:
			Movie.get( Movie.movie_id == obj['summary']['id'])
			Movie.update_movie(obj)
		except DoesNotExist as e:
			Movie.new_movie(obj)


	@staticmethod
	def save_show(obj):
		try:
			TVShow.get( TVShow.tvshow_id == obj['summary']['id'])
			TVShow.update_show(obj)
		except DoesNotExist as e:
			TVShow.new_show(obj)

def create_tables():
	psql_db.connect()
	psql_db.create_tables([Actor, OMDB, OMDB_Actors])