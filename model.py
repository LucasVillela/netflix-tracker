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
	psql_db.create_tables([TVShow])