import json
import os

search_page = 'https://songwhip.com/'
detail_page = 'https://songwhip.com/api/songwhip/create'

qobuz_page = 'https://slavart.gamesdrive.net/tracks?'

ripper_page = 'https://doubledouble.top/'

with open('config/config.json', 'rb') as f:
    config = json.load(f)
f.close()

save_dir = config.get('save_dir', '')

if not os.path.isabs(save_dir):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(script_dir, save_dir)

os.makedirs(save_dir, exist_ok=True)
