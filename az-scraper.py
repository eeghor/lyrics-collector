import socks  # create TCP connections through a SOCKS proxy
import socket
import stem.process
import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict

SOCKS_PORT=7000

tor_process = stem.process.launch_tor_with_config(
    config = {
        'SocksPort': str(SOCKS_PORT),
    },
)

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                      addr="127.0.0.1", #theres a ',' change it to '.' -- linkedin was being glitchy
                      port=SOCKS_PORT)

socket.socket = socks.socksocket

header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}

MAIN_URL = "http://www.azlyrics.com"

r = requests.get(MAIN_URL, headers=header).text  # response body as bytes so need get text first

artist_list = ["depeche mode", "alt-j"]

artist_1st_letter_urls = defaultdict(str)

soup = BeautifulSoup(r, "lxml")

# go to the header picture showing "AZ"
bar_w_letters  = soup.find("ul", id="artists-collapse")
for s in bar_w_letters.find_all("a"):
	artist_1st_letter_urls[s.text.strip().lower()] = s["href"]

for artist in artist_list:
	artist_letter = artist.strip()[0]
	# go to the page for this letter
	pg_letter_artists = requests.get(artist_1st_letter_urls[artist_letter], headers=header).text  # response body as bytes so need get text first
	#print(pg_letter_artists)
	soup_page = BeautifulSoup(pg_letter_artists, "lxml")
	# collect all artis names on this page
	this_page_urls = defaultdict(str)
	for a in soup_page.find_all("a", href=re.compile(artist_letter + "/")):
		this_page_urls["".join([v for v in a.text.lower().strip() if (v.isalnum() or (v == " "))])] = "/".join([MAIN_URL, a["href"]])
	# try to find out if the artist is on this page
	try:
		albums_page = requests.get(this_page_urls[artist], headers=header).text
	except:
		# most likely, caouldn't find the artist; move on to the next artist
		continue
	# if artist has been found, create a soup object for the album page
	soup_alb_page = BeautifulSoup(albums_page, "lxml")
	# song dictionary
	this_artist_track_urls = defaultdict(str)
	for a in soup_alb_page.find_all("a", href=re.compile("/lyrics/")):
		this_artist_track_urls[a.text.lower().strip()] = "/".join([MAIN_URL, a["href"][3:]])  # skip "../"
	# now got to the page where the lyrics is
	for song in this_artist_track_urls:
		track_lyrics_pg = requests.get(this_artist_track_urls[song], headers=header).text
		soup_lyrics_pg = BeautifulSoup(track_lyrics_pg, "lxml")
		# go to that span over the lyrics
		sp = soup_lyrics_pg.find("span", id="cf_text_top")
		print(sp.parent.find_next_sibling("div"))

	tor_process.kill()






