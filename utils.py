def get_url(url, imdb_id, api_key):
	url = url.replace('xxxx', imdb_id)
	return url.replace('yyyy', api_key)