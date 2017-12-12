from grab import Grab
import re

class GoogleImdb:
	@staticmethod
	def search_imdbid_on_google(title):
		g = Grab()
		url = 'www.google.com.br/search?q='
		query = title.replace(' ','+')
		query += ('+IMDB')
		g.go( url + query )
		search_result = g.doc('//a[contains(@class, "l")]/@href').text_list()
		for item in search_result:
			list_found = re.findall(r'www.imdb.com/title/tt[0-9]*',item)
			if len(list_found) > 0:
				for imdb in list_found:
					imdb_ids = re.findall(r'tt[0-9]*',imdb)

		if imdb_ids is not None:
			return imdb_ids[0]
		return None

