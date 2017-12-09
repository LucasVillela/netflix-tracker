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
	updated_at = DateField()
	created_at = DateField()

	@classmethod
	def new_movie(obj):
		movieid = obj['summary']['id']
		title = obj['title']
		movie = Movie(movie_id=movieid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		movie.save()

	@classmethod
	def update_movie(obj):
		movie = Movie.get( Movie.movie_id == obj['summary']['id'])
		movie.updated_at = datetime.now()
		movie.save()

	@classmethod
	def save_movie(obj):
		if Movie.get( Movie.movie_id == obj['summary']['id']) is None:
			self.new_movie(obj)
		else:
			self.update_movie(obj)

class TVShow(BaseModel):
	tvshow_id = IntegerField()
	title = TextField()
	total_seasons = IntegerField(default=1)
	updated_at = DateField()
	created_at = DateField()

	@classmethod
	def new_show(self, obj):
		tvshowid = obj['summary']['id']
		title = obj['title']
		tvshow = TVShow(tvshow_id=tvshowid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		tvshow.save()

	@classmethod		
	def update_show(self, obj):
		tvshow = TVShow.get( TVShow.tvshow_id == obj['summary']['id'])
		tvshow.updated_at = datetime.now()
		tvshow.save()

	@classmethod
	def save_show(self, obj):
		if TVShow.get( TVShow.tvshow_id == obj['summary']['id']) is None:
			self.new_show(obj)
		else:
			self.update_show(obj)


def create_tables():
	psql_db.connect()
	psql_db.create_tables([TVShow])