#!/usr/bin/env python3
import multiprocessing
from multiprocessing import Pool
import os
import sys
import glob
import time
import re
from subprocess import Popen, PIPE, STDOUT
from collections import OrderedDict

# get the binary build for a newish ffmpeg (needed for some video filtering)
FFMPEG = "./ffmpeg-git-20190320-amd64-static/ffmpeg"

def tots(t):
    timestamp = "%02d:%02d:%02d.00" % (t / 3600, t/60 % 60, t % 60)
    return timestamp

def run_ffmpeg(seconds, video_filter, output_file):
    args = [FFMPEG, '-y', '-f', 'lavfi', '-i', 'color=color=black']
    
    args += ['-vf', video_filter]
    args += ['-t', str(seconds)]
    args += [output_file]

    p = run_cmd(args)
    stdout, stderr = p.communicate()
    code = p.returncode

    if code != 0:
        print("ERROR RUNNING FFMPEG")
        print(stderr.decode())

def run_cmd(args):
    #print("RUN: %s"% " ".join(args))
    return Popen(args, stdout=PIPE, stderr=PIPE)

def run_cmd_pipe(args):
    #print("RUN: %s"% " ".join(args))
    return Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
                for text in _nsre.split(s)] 

def main():
    doc_input = sorted(glob.glob("doc_pdf/" + "*.txt"), key=natural_sort_key)

    job_id = 0

    print("Got %d text files as input" % len(doc_input))

    bundles = []

    # 25 videos of four text files each
    for i in range(25):
        bundles += [[i, doc_input[i*4:i*4+4]]]

    start = time.time()
    jobs = multiprocessing.cpu_count() - 1

    print("Encoding NSA training videos using %d threads" % jobs)
    with Pool(processes=jobs) as pool:
        pool.map(job, bundles, 1)

    end = time.time()

    print("Processed %d bundles in %.2f" % (len(bundles), end-start))

def job(credits):
    video_id = credits[0]
    credit_files = credits[1]
    proc = multiprocessing.current_process()
    job_id = proc._identity[0]

    output_file = 'output/ghidra_training_%d.mp4' % video_id

    if os.access(output_file, os.R_OK):
        print("Skipping %s" % output_file)
        return

    combined_credit_file = '%scredit.txt' % job_id

    total_credits = ""
    for credit in credit_files:
        with open(credit, 'rb') as fp:
            total_credits += fp.read().decode('ascii', 'ignore')

    with open(combined_credit_file, 'w') as fp:
        fp.write(total_credits)

    video_name = 'GHIDRA Training %d' % video_id
    total_lines = len(total_credits.split("\n"))
    seconds = int(total_lines*1.3) + 60

    other_filters = [
        "drawtext='fontsize=22:fontfile=FreeSerif.ttf:fontcolor=white:text='"'%s'"':x=(w-text_w)/2-10:y=h-40:enable=lt(t\,8)'" % video_name,
        "drawtext='fontsize=15:fontfile=DejaVuSansMono:fontcolor=white:text='"'TOP SECRET//CYBER//NOFORN'"':y=h-line_h:x=-50*t+300'",
        "drawtext='fontsize=20:fontfile=FreeSerif.ttf:line_spacing=5:fontcolor=white:textfile=%s:y=h-20*(t-12):x=10'" % (combined_credit_file),
        "drawtext='fontsize=22:fontfile=FreeSerif.ttf:fontcolor=white:text='"'%s'"':x=(w-text_w)/2-10:y=h-40:enable=lt(t\,8)'" % video_name,
    ]

    all_filters = ",".join(other_filters)

    MAIN_FILTER = "movie=watermarklogo.png,scale=180:180 [logo]; [in][logo] overlay=(W-w)/2:(H-h)/2-20, fade=in:0:25, fade=out:200:25, %s [out]" % all_filters

    start = time.time()

    print(output_file)
    run_ffmpeg(seconds, MAIN_FILTER, output_file)

    try:
        os.unlink(combined_credit_file)
    except OSError: 
        pass

    print("(%s, sec=%d, lines=%d) DONE in %.2f seconds" % (output_file, seconds, total_lines, time.time()-start))

if __name__ == "__main__":
    main()
