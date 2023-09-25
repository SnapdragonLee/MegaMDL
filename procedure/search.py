import requests
from tabulate import tabulate
from wcwidth import wcswidth

from const.basic import *
from procedure.multi import collect_info_main


def check_connection():
    url = search_page
    s = requests.session()
    mod = 0

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
            resp = s.get(url, timeout=2)
            if resp.status_code == 200:
                flag_ripper = True
                mod += 1
                break
        except Exception:
            continue
    if not flag_ripper:
        mod += 2

    url = q_page
    try:
        resp = s.get(url)
        if resp.status_code != 200:
            mod += 4
    except requests.ConnectionError:
        mod += 4
    if mod < 6:
        return mod


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


def check_procedure(input_str: str):
    query_final = search_song(input_str)

    if len(query_final):
        selected_column = [row[:-1] for row in query_final]
        heads = ['', 'Track Name', 'Artist(s)', 'Release Data', 'Download Type']
        column_widths = [wcswidth(str(header)) for header in heads]
        for row in selected_column:
            for i, value in enumerate(row):
                if i > 4: continue
                column_widths[i] = max(column_widths[i], wcswidth(str(value)))

        alignments = ["center" for _ in heads]
        print(tabulate(selected_column, heads, colalign=alignments, tablefmt='fancy_grid',
                       maxcolwidths=column_widths))
        return query_final
    else:
        return None
