import concurrent.futures
import re

import requests

from const.basic import *


# Define a function to send POST requests and collect information
def collect_info(data, entry, sequence):
    m128k_st = False
    hq_st = False
    sq_st = False
    hires_st = False

    try:
        response = requests.post(url=detail_page, json=data)  # Replace with your actual URL and data
        if response.status_code != 200:
            raise Exception(f'Request failed with status code: {response.status_code}. Please check your network.')
    except Exception as e:
        print(f"Connection Error occurred, Please restart script!: {e}")

    # Decode the JSON response
    dat = response.json()
    links = dat['data']['item']['links']
    if 'qobuz' in links:
        hires_st = True
    if 'tidal' in links:
        sq_st = True
        sq_link = links['tidal'][0]['link']
    elif 'deezer' in links:
        sq_st = True
        sq_link = links['deezer'][0]['link']
    if 'spotify' in links:
        hq_st = True
    if 'soundcloud' in links:
        m128k_st = True
    track_name = entry['name']
    artists = ', '.join(artist['name'] for artist in entry['artists'])
    release_date = re.sub(r'T.*?Z', '', dat['data']['item']['releaseDate'])
    return (sequence, track_name, artists, release_date, [m128k_st, hq_st, sq_st, hires_st],
            [
                links['soundcloud'][0]['link'] if m128k_st else None,
                links['spotify'][0]['link'] if hq_st else None,
                sq_link if sq_st else None,
                links['qobuz'][0]['link'] if hires_st else None
            ])


def collect_info_main(query_list):
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for entry in query_list:
            query_data = {
                "url": entry['sourceUrl'],
                "country": "US",
            }
            futures.append(executor.submit(collect_info, query_data, entry, len(futures) + 1))
        concurrent.futures.wait(futures)
    return [future.result() for future in futures]
