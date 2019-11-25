#!/usr/bin/env python3
import multiprocessing
from multiprocessing import Pool
import os
import sys
import glob
import time
from subprocess import Popen, PIPE, STDOUT
from collections import OrderedDict

input_file = "ghidra_nsa_training.mp4"
SECONDS = 15*60*60 + 30*60 + 13
SEC_BATCH = 60
FFMPEG = "ffmpeg"
TESS = "tesseract"

def tots(t):
    timestamp = "%02d:%02d:%02d.00" % (t / 3600, t/60 % 60, t % 60)
    return timestamp

def run_ffmpeg(inp, t, frames, output):
    timestamp = tots(t)

    args = [FFMPEG, '-ss', timestamp, '-i', inp, '-vf', 'fps=1', '-vframes', str(frames), output]

    p = run_cmd(args)
    stdout, stderr = p.communicate()
    code = p.returncode

    if code != 0:
        print("ERROR RUNNING")
        print(stderr)

def run_tess(frame_list):
    args = [TESS, '-', '-']

    p = run_cmd_pipe(args)
    flist = "\n".join(frame_list)
    stdout, stderr = p.communicate(input=flist.encode())
    code = p.returncode

    if code != 0:
        print("ERROR RUNNING")
        print(stderr)
        return None
    else:
        return stdout.decode()

def run_cmd(args):
    #print("RUN: %s"% " ".join(args))
    return Popen(args, stdout=PIPE, stderr=PIPE)

def run_cmd_pipe(args):
    #print("RUN: %s"% " ".join(args))
    return Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def main():
    sec = range(SECONDS)[::SEC_BATCH]
    job_id = 0

    start = time.time()
    jobs = multiprocessing.cpu_count() - 1

    with Pool(processes=jobs) as pool:
        pool.map(job, sec, 1)

    end = time.time()

    print("Processed %d seconds in %.2f" % (len(sec), end-start))

def job(sec):
    timestamp = tots(sec)
    output_file = 'output/%s'% timestamp

    if os.access(output_file, os.R_OK):
        #print("Skipping %s" % output_file)
        return

    proc = multiprocessing.current_process()
    job_id = proc._identity[0]
    base_dir = "tmpframes/"+ str(job_id) + "/"

    try:
        os.mkdir(base_dir)
    except OSError:
        pass

    start = time.time()
    # BMP is huge, but faster to extract due to no JPG encoding
    # A tmpfs filesystem is STRONGLY recommened to avoid killing disk IO

    outputpat = os.path.join(base_dir, "f%07d.bmp")
    run_ffmpeg(input_file, sec, SEC_BATCH, outputpat)
    files = sorted(glob.glob(base_dir + "*"))
    text = run_tess(files)

    uniq = OrderedDict()
    for line in text.split("\n"):
        uniq[line] = 1

    uniq = list(uniq.keys())

    with open(output_file, 'w') as fp:
        fp.write("\n".join(uniq))

    print("%s DONE %.2f" % (timestamp, time.time()-start))

if __name__ == "__main__":
    main()
