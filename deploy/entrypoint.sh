#!/bin/bash

wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz.md5
md5sum -c ffmpeg-release-amd64-static.tar.xz.md5
tar xvf ffmpeg-release-amd64-static.tar.xz
mkdir -p ffmpeg/bin
cp ffmpeg-6.0-amd64-static/ffmpeg ffmpeg/bin


cd /home/venv
python3 -m virtualenv -p /usr/bin/python3 py3
source /home/venv/py3/bin/activate


pip3 install -r /requirements.txt -t /home/dist/python

rm -rf /home/dist/python/__pycache__

cd /home/dist
zip -r output.zip ./python