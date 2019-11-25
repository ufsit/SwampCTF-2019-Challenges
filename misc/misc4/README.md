# [SwampCTF 2019 Miscellaneous] Ghidra Release

## Flavor Text

> **Meanwhile at the NSA on a Friday afternoon**
> Manager: Hey, we're going to be releasing our internal video training for Ghidra and we need you to watch it all to flag any content that needs to be redacted before release.
> Manager: The release is next Monday. Hope you didn't have any weekend plans!
> You: Uhhh, sure bu-
> Manager: Great! Thanks. Make sure nothing gets out.
> You: ... *looks at clock. It reads 3:45PM*
> You: *Mutters to self* No way am I watching all of this. There's got to be a better way...

* Flag: `flag{l34kfr33_n4tion4l_s3cur1ty}`
* Expected difficulty: medium

## Description
This challenge is a scripting challenge that requires the competitors to find any "redacted" data in a long video file.
The video length is quite long so either you can assign a super bored teammate
to watch it all or use some ffmpeg magic to extract out frames. Except there
are around 1.3 million frames so even this will be difficult! What about each second?
Well there are about 52K frames. More managable, but what does the flag look
like? How can we filter frames? Well the easiest trick would be to throw all
frames into an OCR solution then just grep all of the text for "flag".
A good OCR solution is [tesseract](https://github.com/tesseract-ocr/tesseract/).
It's easily scripted via bash or Python subprocess.

## Challenge Solution

Create a script to batch process ffmpeg frames into text. Search through text for flag indicators.
The real challenge is making your script efficient (or having the compute resources) enough to complete in a timely manner.
The blocking part is the OCR script. If a faster OCR than tesseract is used, then this will take a lot less time.
The solution was tested on 40 cores and it took 674 seconds. For a single core machine this would be more like 7.5 hours.
Still manageable.  The solution is included in the `ocr/job.py` file.

### Resources used

* https://waldo.jaquith.org/blog/2011/02/ocr-video/
* https://johnvansickle.com/ffmpeg/
* https://www.ffmpeg.org/ffmpeg-devices.html#lavfi
* https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
* https://trac.ffmpeg.org/wiki/Create%20a%20thumbnail%20image%20every%20X%20seconds%20of%20the%20video
* https://stackoverflow.com/questions/11640458/how-can-i-generate-a-video-file-directly-from-an-ffmpeg-filter-with-no-actual-in
* https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg
* https://stackoverflow.com/questions/6195872/applying-multiple-filters-at-once-with-ffmpeg
* https://stackoverflow.com/questions/10918907/how-to-add-transparent-watermark-in-center-of-a-video-with-ffmpeg
* https://stackoverflow.com/questions/50735335/ffmpeg-adding-text-to-a-video-between-two-times
* https://stackoverflow.com/questions/25870169/how-to-set-background-to-subtitle-in-ffmpeg
