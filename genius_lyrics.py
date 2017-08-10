import requests
from bs4 import BeautifulSoup

ACCESS_TOKEN = "xbe3FTL4S0Ybni7r6sPaKFYSkcVVszqPWoGAQUZw_kSBYFjTkLBFHieDULkq2AO3"

BASE_URL = "https://api.genius.com"

TOKEN = "Bearer {}".format(ACCESS_TOKEN)

SEARCH_URL = BASE_URL + "/search"

headers = {'Authorization': TOKEN}

ARTIST = "depeche mode"

response = requests.get(SEARCH_URL, data={"q": "personal jesus"}, headers=headers)

for hit in response.json()["response"]["hits"]:
	if hit["result"]["primary_artist"]["name"].lower() == ARTIST:
		song_api = hit["result"]["api_path"]    # this path is like "/songs/65262"
		song_url = BASE_URL + song_api
		response = requests.get(song_url, headers=headers)
		path = response.json()["response"]["song"]["path"]
		page_url = "http://genius.com" + path
		page = requests.get(page_url)
		html = BeautifulSoup(page.text, "html.parser")
		# PageElement.extract() removes a tag or string from the tree. 
		# It returns the tag or string that was extracted:
		[h.extract() for h in html('script')]
		lyrics = html.find("div", class_="lyrics").get_text()
		print(lyrics)