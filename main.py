from procedure.download import dw_from_main, dw_from_qobuz
from procedure.search import check_procedure, check_connection

if __name__ == '__main__':
    mod = check_connection()

    if mod == 1:
        print('Main Mode Enabled')
    elif mod == 2:
        print('Backup Mode Enabled')
    elif mod == 5:
        print('No Hi-Res Mode Enabled')
    else:
        raise ConnectionError('Please check your connection or try this app after a while')

    query_input = input('Please input search words: ')
    query_list = check_procedure(query_input)

    if query_list is None:
        print('Please try it again or change searching keyword')  # todo: Need to modify the structure of control flow

    select_input = int(input('Please select a song: '))
    song_select = query_list[select_input - 1]

    quality_input = int(input('Please select the quality: '))
    if quality_input == 4:
        rtn = dw_from_qobuz(song_select[1], song_select[2], song_select[5][3])
    elif quality_input == 3 and song_select[5][quality_input - 1] is None:
        rtn = dw_from_qobuz(song_select[1], song_select[2], song_select[5][4])
    else:
        rtn = dw_from_main(song_select[1], song_select[2], song_select[5][quality_input - 1])
