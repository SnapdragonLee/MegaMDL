from const.basic import *
from procedure.download import dw_from_main, dw_from_qobuz
from procedure.search import check_procedure, check_connection

if __name__ == '__main__':
    mod = check_connection()

    if mod == 1:
        print('Main Mode Enabled')
    elif mod == 2:
        print('Backup Mode Enabled')
    elif mod == 5:
        print('Slow Hi-Res Download Mode Enabled')
    else:
        raise ConnectionError('Please check your connection or try this app after a server recover')

    query_input = input('Please input search words: ')
    query_list = check_procedure(query_input, mod)

    if query_list is None:
        print('Please try it again or change searching keyword')  # todo: Need to modify the structure of control flow

    select_input = int(input('Please select a song: '))
    song_select = query_list[select_input - 1]

    selectable_list = []
    for i, d_type in enumerate(song_select[5]):
        if d_type is None: continue
        selectable_list.append(f'[{i + 1}] {COLORS[i]}{d_type}{COLORS[4]}')

    print('Please select the quality: \n' + '     '.join(selectable_list))
    quality_input = int(input())
    if not song_select[5][quality_input - 1]:
        print("Please select the download options listed, you are requesting Non-Existent resource")
        exit("Exiting")
    if quality_input == 4:
        if song_select[6][3][8] == 'o':
            rtn = dw_from_main(song_select[1], song_select[2], song_select[6][3])
        else:
            rtn = dw_from_qobuz(song_select[1], song_select[2], song_select[6][3])

    elif quality_input == 3 and (not song_select[5][2]):
        rtn = dw_from_qobuz(song_select[1], song_select[2], song_select[6][4])
    else:
        rtn = dw_from_main(song_select[1], song_select[2], song_select[6][quality_input - 1])

    print('Download procedure finished!' if rtn else 'Download procedure failed. You can wait a while or try it again')

    # todo: should I make it public?
