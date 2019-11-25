# [SwampCTF 2019 Forensics] Cartographer's Capture

## Flavor Text
We've gotten a hold of a file that contains a whole bunch of weird-looking IP addresses by having one of our robo-hounds sniff out some leaking data from a EvilCorp warehouse. We're not sure how to decipher this but we know that this particular warehouse is one of the main sources for location information. 

* Flag: `flag{big_a$$_fl4g}`
* Expected difficulty: hard

## Description
You're given a list of **ip addresses** in a text file. They're obviously in hex. After some useless conversions from the user trying to decode these, they should eventually know that they need to piece it together as a full hex string. Since the flavor text hints towards something with maps and locations they should start thinking towards that. Eventually they will start converting the full hex lines to floats which give pairs of GPS coords. Putting all the coords into an online plotter (maphamster.com for example) they will see that it spells out the flag. 

## Challenge Solution
1) take the **IP addresses** and convert to full hex lines 
2) convert to float (solutions are online as well as in my src folder for this)
3) take every two as GPS coordinate pairs 
4) compile all in an online coordinate plotter (such as maphamster.com) 
	1) formatting them correctly 
5) plot all and it gives the `flag{big_a$$_fl4g}`
