import requests
from tabulate import tabulate

from const.basic import *
from procedure.multi import collect_info_main

mod = 0


def check_connection() -> bool:
    global mod
    url = search_page
    s = requests.session()

    try:
        resp = s.get(url)
        if resp.status_code != 200:
            return False
    except requests.ConnectionError:
        return False

    url = ripper_page
    flag_ripper = False
    for attempt in range(5):
        try:
            resp = s.get(url)
            if resp.status_code == 200:
                flag_ripper = True
                mod += 1
                break
        except requests.ConnectionError:
            continue
    if not flag_ripper:
        mod += 2

    url = qobuz_page
    try:
        resp = s.get(url)
        if resp.status_code != 200:
            mod += 4
    except requests.ConnectionError:
        mod += 4
    if mod < 6:
        return True


def search_song(query: str):
    # Build the API request URL
    search_url = search_page + f'api/songwhip/search?q={query}&country=US&limit=6'
    session = requests.session()

    try:
        response = session.get(url=search_url)
        if response.status_code == 200:
            # Decode the JSON response
            dat = response.json()
        else:
            return f'Request failed with status code: {response.status_code}. Please check your network.'
    except Exception as e:
        return f'An exception occurred: {e}'

    query_list = dat['data']['tracks']
    return collect_info_main(query_list)


if __name__ == '__main__':
    if check_connection():
        print(f'Connect to domains successfully')
    else:
        raise ConnectionError('Please check your connection or try this app after a while')

    if mod == 1:
        print('Enable Main Mode')
    elif mod == 2:
        print('Enable Backup Mode 1')
    elif mod == 5:
        print('Enable no Hi-Res Mode 2')

    user_input = '青花瓷'  # input('Please input search words: ')
    query_final = search_song(user_input)

    # 打印表格
    if len(query_final):
        heads = ['Track Name', 'Artist(s)', 'Release Data', 'Release Type']
        print(tabulate(query_final, heads, tablefmt='psql', colalign=("center", "center", "center", "center")))

    print(mod)
