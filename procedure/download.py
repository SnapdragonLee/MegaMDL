import time
from urllib.parse import quote

import requests

from const.basic import *


def dw_from_main(name, artist, origin_url: str) -> bool:
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
        print('Please check your connection or try this app after a while')
        return False

    origin_redirect = ripper_page + 'dl/' + resp.json()['id']

    dw_status = False

    while not dw_status:
        try:
            resp = s.get(url=origin_redirect)
            if resp.status_code == 200:
                content = resp.json()
                origin_status = content['status']
                dw_status = (origin_status == 'done')
                if 'percent' not in content:
                    continue
                origin_percent = content['percent']
                if origin_status != 'done':
                    process = "\r[%3s%%]: |%-50s|\033[K" % (int(origin_percent), '|' * int(origin_percent / 2))
                    time.sleep(3)
                else:
                    process = "\r[%3s%%]: |%-50s|" % (100, '|' * 50)
                print(process, end='', flush=True)

            else:
                print('Server is down, Please try again or wait a little while')
                return False
        except requests.ConnectionError:
            print('Please check your connection or try this app after a while')
            return False

    print()
    times = -1
    while times < 8:
        times += 1
        time.sleep(1)
        try:
            resp = s.get(url=ripper_page + content['url'][2:])
            if resp.status_code == 200:
                filename = os.path.basename(
                    name + ' - ' + artist + content['url'][content['url'].rfind('.'):]
                )
                file_path = os.path.join(save_dir, filename)
                with open(file_path, 'wb') as mp3_file:
                    mp3_file.write(resp.content)
                print(f"\nThe download is completed and saved in {file_path}")
                break
        except requests.ConnectionError:
            continue
    return True


def dw_from_qobuz(name, artist, qobuz_url: str):
    s = requests.session()

    flag_qobuz = False
    for attempt in range(3):
        try:
            resp = s.get(url=qobuz_url)
            if resp.status_code == 200:
                flag_qobuz = True
                break
        except requests.ConnectionError:
            time.sleep(0.5)
            continue

    if not flag_qobuz:
        print('Please check your connection or try this app after a while')
        return False
    filename = os.path.basename(name + ' - ' + artist + '.flac')
    file_path = os.path.join(save_dir, filename)
    with open(file_path, 'wb') as hires_file:
        hires_file.write(resp.content)
    print(f"\nThe download is completed and saved in {file_path}")
    return True


if __name__ == '__main__':
    dw_from_main('https://listen.tidal.com/track/96970498')
