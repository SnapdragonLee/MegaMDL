import json
import os

str1 = '穮谁镋城밎絠闙筪䗴酾⣎'
str2 = '鄓봏舳䶠蕩藸饹鈏眂繦䷒艣䜄酿逖너缨臣睛诶'
str3 = '者隁鯙矎艥翧獬访襲阄밃腢铖䁨紅兲餈砒瑚郔稹'
str4 = '鄓봏舳䶠蕦礇莃鳌ꨏ砧藒罟諵鑺鼄眍瑭䷒艣䛵醈霋렀猨鋣獝苐'
str5 = '鄓봏舳䶠癩賳蹶贎븁筞䳥腪ៀ'

with open('config/config.json', 'rb') as f:
    config = json.load(f)
f.close()

save_dir = config.get('save_dir', '')

if not os.path.isabs(save_dir):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_dir = os.path.join(script_dir, save_dir)

os.makedirs(save_dir, exist_ok=True)

key = [0x1791, 0x1e71, 0x489f, 0x2211, 0x11fa, 0x0ef9, 0x289f]


def inter(inp: str):
    hex_string = ''
    for i, char in enumerate(inp):
        decrypted_char = chr(ord(char) - key[(len(inp) - i * 4) % 7])
        hex_string += hex(ord(decrypted_char))[2:]
    return bytes.fromhex(hex_string).decode('utf-8')


search_page = inter(str1)
detail_page = inter(str2)
q_page = inter(str3)
q_dw = inter(str4)
ripper_page = inter(str5)

# def m(oup: str):
#     original_string = oup
#     hex_string = original_string.encode('utf-8').hex()
#     print(hex_string)
#     utf16_characters = [chr(int(hex_string[i:i + 4], 16) + key[(int((len(hex_string) + 3) / 4) - i) % 7]) for i in
#                         range(0, len(hex_string), 4)]
#     return ''.join(utf16_characters)
