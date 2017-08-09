import requests

ACCESS_TOKEN = "xbe3FTL4S0Ybni7r6sPaKFYSkcVVszqPWoGAQUZw_kSBYFjTkLBFHieDULkq2AO3"

BASE_URL = "https://api.genius.com"

TOKEN = "Bearer {}".format(ACCESS_TOKEN)

SEARCH_URL = BASE_URL + "/search"

headers = {'Authorization': TOKEN}

ARTIST = "porcupine tree"

response = requests.get(SEARCH_URL, data={"q": "porcupine"}, headers=headers)

for hit in response.json()["response"]["hits"]:
	if hit["result"]["primary_artist"]["name"].lower() == ARTIST:
		print(hit["result"]["api_path"])    # this path is like "/songs/65262"