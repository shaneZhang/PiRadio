#!/bin/sh
#播放电台曲目
if [ $# -lt 1 ]
then
  echo "缺少参数：music_url"
  exit 1
fi
/usr/bin/sox -t mp3 $1 -t wav - | sudo fm -freq 107.5 -audio - 
