# [SwampCTF 2019 Forensics] Neo

## Flavor Text
We hacked one of EvilCorps sentries and found something interesting. A single picture, we're not sure what to do with this but we know this sentry was fond of his abilities to hide things in plain site. 

* Flag: flag{f011ow_th3_wh1t3_rabb17}
* Expected difficulty: easy

## Description
This challenge is a rather easy stegonography challenge. A flag is hidden as a thumbnail in a jpg, but that jpg is hidden as a thumbnail in another jpg. Layers of obfuscation bring this challenge from a trivial to an easy. 

## Challenge Solution
Running `exif < file name >.jpg` we see that there is a huge thumbnail, which should be weird to the player. We extract that with 
`exif -e < file name >.jpg --output output` and once we look at `output` in a file explorer we see it's another jpg. We can also see that 
the output is a picture via `file output`. 
Running `exif < extracted file >.jpg` we see this one has another thumbnail, we extract again but the file explorer doesn't show a pic. 
We `cat < second extracted file >` and we see the flag.   
