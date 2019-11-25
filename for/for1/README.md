# [SwampCTF 2019 Forensics] The Cyber War Continues

## Flavor Text

As you and your convoy circle the barren lands on your light cycles you notice something strange in the distance.
Upon further investigation you find what seems to be the remnants of a battle. Bodies, robotic and organic alike, 
are strewn all over the place. You begin scavenging for supplies and weapons, suddenly a man near death thrusts his 
hand and grabs your arm. "Please" he croaks, "find my friends". He hands you a USB as he takes his last breath. 
You plug the drive into your mechanical arm and the contents start flooding your HUD. It contains this message and
an ecrypted file.   

* Flag: `flag{war_never_changes}`
* Expected difficulty: medium

## Description
In this challenge the user is presented with a block of cipher text and a passprotected zipped pcap. The user is to figure out what cipher I used which 
reveals the password for the zipped file. Once the pcap file is obtained the user needs to recognize that usb traffic is being captured. Once the user finds 
applicable keyboard codes that translate the usb keystrokes the flag will be revealed.  
Files given are the cipher text (txt file) and the pcap file, openable in wireshark. 

## Challenge Solution
For this forensics challenge the cipher text is going to be implemented with a railfence cipher, with a key of 3. In terms of indicativeness the user will just have to try multiple ciphers until they figure out its railfence. This gives them the password for the zip file. They unlock the zip file. Within the zip is one pcap file. When opened there will be two sorts of traffic, traffic from the keyboard and from the mouse. Once the user realizes the difference they will need to isolate the traffic from the keyboard. 
`tshark -r <pcap file> | grep < usb keyboard address >`
Once they isolate the keyboard traffic they will need to do some googling and find a solution to translate keyboard stroke codes in the pcap to ASCII. Once they do this they will get the flag. 
