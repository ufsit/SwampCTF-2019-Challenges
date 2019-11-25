#!/bin/sh
# convert all text to video training files
./encode.py

# concat all input files
ffmpeg -f concat -i files.txt -c copy output.mp4

# overlay flag subtitles
ffmpeg -y -i output.mp4 -vf subtitles=flag.ass -c:a copy ghidra_nsa_training.mp4
