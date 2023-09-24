import time
from urllib.parse import quote

import requests

from const.basic import *


def dw_from_origin(origin_url: str):
    global resp
    origin_trans_url = ripper_page + 'dl?url=' + quote(origin_url) + '&format=mp3&donotshare=true'
    s = requests.session()

    flag_origin = False
    for attempt in range(5):
        try:
            resp = s.get(url=origin_trans_url)
            if resp.status_code == 200:
                flag_origin = True
                break
        except requests.ConnectionError:
            time.sleep(0.5)
            continue
    if not flag_origin:
        raise ConnectionError('Please check your connection or try this app after a while')

    origin_redirect = ripper_page + 'dl/' + resp.json()['id']

    dw_status = False

    while not dw_status:
        try:
            resp = s.get(url=origin_redirect)
            if resp.status_code == 200:
                origin_status = resp.json()['status']
                dw_status = (origin_status == 'done')
                if 'percent' not in resp.json():
                    continue
                origin_percent = resp.json()['percent']
                if origin_status != 'done':
                    process = "\r[%3s%%]: |%-50s|\033[K" % (int(origin_percent), '|' * int(origin_percent / 2))
                    time.sleep(3)
                else:
                    process = "\r[%3s%%]: |%-50s|" % (100, '|' * 50)
                print(process, end='', flush=True)

            else:
                print('Server is down, Please try again or wait a little while')
                break
        except requests.ConnectionError:
            raise ConnectionError('Please check your connection or try this app after a while')


def dw_from_qobuz(qobuz_url: str):
    global resp
    origin_trans_url = ripper_page + 'dl?url=' + quote(qobuz_url) + '&format=mp3&donotshare=true'
    s = requests.session()

    flag_origin = False
    for attempt in range(5):
        try:
            resp = s.get(url=origin_trans_url)
            if resp.status_code == 200:
                flag_origin = True
                break
        except requests.ConnectionError:
            time.sleep(0.5)
            continue
    if not flag_origin:
        raise ConnectionError('Please check your connection or try this app after a while')

    origin_redirect = ripper_page + 'dl/' + resp.json()['id']

    dw_status = False

    while not dw_status:
        try:
            resp = s.get(url=origin_redirect)
            if resp.status_code == 200:
                origin_status = resp.json()['status']
                dw_status = (origin_status == 'done')
                if 'percent' not in resp.json():
                    continue
                origin_percent = resp.json()['percent']
                if origin_status != 'done':
                    process = "\r[%3s%%]: |%-50s|\033[K" % (int(origin_percent), '|' * int(origin_percent / 2))
                    time.sleep(3)
                else:
                    process = "\r[%3s%%]: |%-50s|" % (100, '|' * 50)
                print(process, end='', flush=True)

            else:
                print('Server is down, Please try again or wait a little while')
                break
        except requests.ConnectionError:
            raise ConnectionError('Please check your connection or try this app after a while')


if __name__ == '__main__':
    dw_from_origin('https://listen.tidal.com/track/96970498')
