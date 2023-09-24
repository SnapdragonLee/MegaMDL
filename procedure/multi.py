import concurrent.futures
import re

import requests

from const.basic import *


# Define a function to send POST requests and collect information
def collect_info(data, entry):
    mp3_128k_st = False
    mp3_320k_st = False
    flac_st = False
    hi_res_st = False

    try:
        response = requests.post(url=detail_page, json=data)  # Replace with your actual URL and data
        if response.status_code == 200:
            # Decode the JSON response
            dat = response.json()
            links = dat['data']['item']['links']
            if 'qobuz' in links:
                hi_res_st = True
            if ('tidal' in links) or ('deezer' in links):
                flac_st = True
            if 'spotify' in links:
                mp3_320k_st = True
            if 'soundcloud' in links:
                mp3_128k_st = True
            track_name = entry['name']
            artists = ', '.join(artist['name'] for artist in entry['artists'])
            realease_date = re.sub(r'T.*?Z', '', dat['data']['item']['releaseDate'])
            return track_name, artists, realease_date, [mp3_128k_st, mp3_320k_st, flac_st, hi_res_st]
        else:
            return f'Request failed with status code: {response.status_code}. Please check your network.'
    except Exception as e:
        print(f"Connection Error occurred, Please restart script!: {e}")


def collect_info_main(query_list):
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for entry in query_list:
            query_data = {
                "url": entry['sourceUrl'],
                "country": "US",
            }
            futures.append(executor.submit(collect_info, query_data, entry))
        concurrent.futures.wait(futures)
    return [future.result() for future in futures]
