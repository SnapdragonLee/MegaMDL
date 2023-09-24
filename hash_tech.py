from pydub import AudioSegment
from pydub.playback import play


def generate_fingerprint(audio_file):
    audio = AudioSegment.from_file(audio_file)
    # 使用简单的时间窗口生成指纹
    fingerprint = audio[::1000]  # 每秒生成一个样本
    return fingerprint


def compare_audio(audio_file1, audio_file2):
    fingerprint1 = generate_fingerprint(audio_file1)
    fingerprint2 = generate_fingerprint(audio_file2)

    # 比较音频指纹是否相似
    print("0:" + fingerprint1)
    print("1:" + fingerprint2)

    similarity = fingerprint1 == fingerprint2

    return similarity


# 替换为要比较的音频文件路径
file1 = 'Michael Jackson - Heal the World myfreemp3.vip .mp3'
file2 = 'Heal the World - Michael Jackson.flac'

result = compare_audio(file1, file2)

if result:
    print("0")
else:
    print("1")
