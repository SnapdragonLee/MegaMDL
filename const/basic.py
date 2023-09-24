import json

search_page = 'https://songwhip.com/'
detail_page = 'https://songwhip.com/api/songwhip/create'

qobuz_page = 'https://slavart.gamesdrive.net/tracks?'

ripper_page = 'https://doubledouble.top/'

with open("config/config.json", encoding="utf-8") as f:
    api_config = json.load(f)
f.close()
