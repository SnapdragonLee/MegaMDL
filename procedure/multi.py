import concurrent.futures
import re

import requests

from const.basic import *


# Define a function to send POST requests and collect information
def collect_info(data, entry, sequence, mod: int):
    m128k_st = False
    hq_st = False
    sq_st = False
    hires_st = False
    type_list = []
    s = requests.session()

    try:
        response = s.post(url=detail_page, json=data)  # Replace with your actual URL and data
        if response.status_code != 200:
            raise Exception(f'Request failed with status code: {response.status_code}. Please check your network.')
    except Exception as e:
        raise Exception(f'Connection Error occurred, Please restart script!: {e}')

    # Decode the JSON response
    dat = response.json()
    links = dat['data']['item']['links']
    if 'qobuz' in links:
        if mod != 5:
            try:
                temp_q = links['qobuz'][0]['link']
                resp = requests.get(q_page + 'q=' + temp_q[temp_q.rfind('/') + 1:])
                if resp.status_code != 200:
                    raise Exception(f'Request failed with status code: {response.status_code}. Server maybe closed.')
            except Exception as e:
                raise Exception(f'Connection Error occurred, Please restart script!: {e}')
            if resp.json()['tracks']['total'] != 0:
                q_dat = resp.json()['tracks']['items'][0]
                if int(temp_q[temp_q.rfind('/') + 1:]) == q_dat['id']:
                    if q_dat['hires']:
                        hires_st = True
                        q_link = q_dw + 'id=' + str(q_dat['id'])
                    else:
                        sq_st = True
                        sq_link = q_dw + 'id=' + str(q_dat['id'])
    if mod != 2:
        if 'tidal' in links:
            sq_st = True
            sq_link = links['tidal'][0]['link']
        elif 'deezer' in links:
            sq_st = True
            sq_link = links['deezer'][0]['link']
        elif 'qobuz' in links:
            sq_st = True
            sq_link = links['qobuz'][0]['link']
        if 'spotify' in links:
            hq_st = True
    if 'soundcloud' in links:
        m128k_st = True
    track_name = entry['name']
    artists = ', '.join(artist['name'] for artist in entry['artists'])
    release_date = re.sub(r'T.*?Z', '', dat['data']['item']['releaseDate'])
    release_type = ['LQ' if m128k_st else None, 'HQ' if hq_st else None,
                    'SQ' if sq_st else None, 'Hi-res' if hires_st else None]

    if m128k_st: type_list.append(f"{COLORS[0]}LQ{COLORS[4]}")
    if hq_st: type_list.append(f"{COLORS[1]}HQ{COLORS[4]}")
    if sq_st: type_list.append(f"{COLORS[2]}SQ{COLORS[4]}")
    if hires_st: type_list.append(f"{COLORS[3]}Hi-res{COLORS[4]}")
    return_txt = ', '.join(type_list)

    return (sequence, track_name, artists, release_date, return_txt, release_type,
            [
                links['soundcloud'][0]['link'] if m128k_st else None,
                links['spotify'][0]['link'] if hq_st else None,
                sq_link if sq_st else None,
                q_link if hires_st else None
            ])


def collect_info_main(query_list, mod: int):
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for entry in query_list:
            query_data = {
                'url': entry['sourceUrl'],
                'country': 'US',
            }
            futures.append(executor.submit(collect_info, query_data, entry, len(futures) + 1, mod))
        concurrent.futures.wait(futures)
    return [future.result() for future in futures]
