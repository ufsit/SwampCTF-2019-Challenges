# [SwampCTF 2019 Forensics] Free your mind

## Flavor Text

“You have to let it all go, Neo. Fear, doubt, and disbelief. Free your mind (and your stego tools).” - Morpheus, probably

* Flag: `flag{FR33_Y0UR_M1ND}`
* Expected difficulty: easy

## Description
User needs to find a flag hidden in an image. Tools like binwalk and exif show that there's more than meets the eye. After a few rounds of extracting files we get the flag that's in a JPEG itself. 

## Challenge Solution
`exif leap_of_faith.jpeg` or `binwalk leap_of_faith.jpeg` 
	both will lead you down the right path but I will be using exif 
`exif -e leap_of_faith.jpeg --output output`
`file output` <- reveals that's it another jpeg, we rename to jpg 
`exif output.jpeg` <- if the user is lucky they can see the thumbnail before the challenge is loaded  
Repeat the above extracion process and we get the flag in another jpeg 
Binwalk can probably solve this challenge in one shot, but either way its a good leg stretch for stego tools 
