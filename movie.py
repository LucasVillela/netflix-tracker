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

	@staticmethod
	def new_movie(obj):
		movieid = obj['summary']['id']
		title = obj['title']
		movie = Movie(movie_id=movieid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		movie.save()

class TVShow(BaseModel):
	tvshow_id = IntegerField()
	title = TextField()
	total_seasons = IntegerField(default=1)
	updated_at = DateField()
	created_at = DateField()

	@staticmethod
	def new_show(obj):
		tvshowid = obj['summary']['id']
		title = obj['title']
		tvshow = TVShow(tvshow_id=tvshowid, title=title, updated_at=datetime.now(), created_at=datetime.now())
		tvshow.save()


def create_tables():
	psql_db.connect()
	psql_db.create_tables([TVShow])