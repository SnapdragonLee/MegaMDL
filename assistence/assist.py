import requests
import json
import time
import re
import random
from urllib import parse

callback = {
    'callback': 'jQuery_' + str(random.randint(20000000000000000000, 30000000000000000000)) + "_" + str(
        int(time.time() * 1000))
}

o = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', '1',
     '2', '3']

main_host = 'https://new.myfreemp3juices.cc/'

dw_host = ''  # Could be modified at some time

headerDm = {
    'Accept': 'text/plain'
}

headerX = {  # search
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/15.4 Safari/605.1.15',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

data = {
    'q': 'main theme (Arr.Bateman) maksim',
    'page': '0'
}

search_byte = b'downloadServerUrl:window.location.protocol+"//'


def encode_formdata(obj):
    str_t = []
    for key in obj:
        str_t.append(parse.quote(key, encoding='utf-8') + '=' + parse.quote(obj[key], encoding='utf-8'))

    return_str = '&'.join(str_t)
    return return_str


def d(t):
    length = len(o)
    e = ''

    if t == 0:
        return o[0]

    if t < 0:
        t *= -1
        e += '-'

    while t > 0:
        val = t % length
        t = t // length
        e += o[val]

    return e


def check():
    global dw_host

    session = requests.session()
    js_for_parse = main_host + '/myfreemp3juice.cc.js'
    resp_domain = session.get(url=js_for_parse, headers=headerDm, stream=True)

    if resp_domain.status_code == 200:
        for chunk in resp_domain.iter_content(chunk_size=512):
            if chunk and search_byte in chunk:
                start_index = chunk.find(search_byte) + len(search_byte) + 1
                end_index = chunk.find(b'",', start_index)
                dw_host = 'https://' + chunk[start_index:end_index].decode('utf-8')

                print(f'downloadServerUrl: {dw_host}')
                break
    else:
        raise ConnectionError("Please Check Internet Connection, or create an issue on repo page")

    # Search songs
    search_word = encode_formdata(callback)
    search_url = main_host + 'api/api_search.php?' + search_word

    resp_sch = session.post(url=search_url, data=data, headers=headerX)

    search_data = resp_sch.content.decode('utf-8')
    start_index = search_data.find('(')
    end_index = search_data.rfind(')')
    extracted_data = search_data[start_index + 1:end_index]

    verify = json.loads(extracted_data)['response']
    print(verify)

    select = 1
    select_data = verify[select]
    dw_url = dw_host + d(select_data['owner_id']) + ':' + d(select_data['id'])

    dw_resp = session.get(url=dw_url, headers=headerX)
    filename = select_data['title'] + ' - ' + select_data['artist'] + '.mp3'
    filename = re.sub(r'[\\/:*?<>|"]', '', filename)
    with open(filename, 'wb') as file:
        file.write(dw_resp.content)
    print(select_data)


if __name__ == '__main__':
    check()
