# MegaMDL - Enjoy online music in console 

[TOC]

## Support & Features


- [x] Online music searching

- [x] Music download with different quality: `Low Quality(LQ)`，`High Quality(HQ)`, `Super Quality(SQ)`, `Hi-res Quality(Hi-res)`

  | Quality | Parameter            | Format  |
  | ------- | -------------------- | ------- |
  | LQ      | 128kbps              | MP3     |
  | HQ      | 320kbps,             | MP3/OGG |
  | SQ      | 16bit 44.1kHz,       | FLAC    |
  | Hi-res  | 24bit 44.1/96/192kHz | FLAC    |

  

- [x] Support multithreaded to accelerate estimation on all resources in different service

- [x] Algorithm to analyze quality of audio

- [x] Metadata included

- [ ] Metadata fix with info from other sources

- [ ] Exception judgement precisely

- [ ] Add support for other audio origin services

- [ ] Fix plenty of bugs about format in console

- [ ] Other



***This repo contains lots of bugs, and it's still a semi-finished product. If anything you wanna help me, send me request or contact with me.***



## Usage

1. Install all dependencies from `requirements.txt` using pip:

   ```bash
   pip install ./requirements.txt
   ```

2. Start it with python 3.6 or above:

   ```bash
   python ./main.py
   ```

> ###### *Due to server issues and judge incorrect, you may stuck at some time. Be free to wait a while or `Ctrl+C` to break the program and try it again!



## License

Apache 2.0



## Chinese left

这下终于摆脱QQ、网易音乐的各种版本解码问题了，闲暇的时间可以试试下一下歌曲，老便捷了。
