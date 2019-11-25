# [SwampCTF 2019 Cryptography] 4096

## Flavor Text

I was sent a file by three random guys on AOL chat and compiled all the text together. It seems like my Windows 95 machine can't take such processing power. Can you help me understand what's going on?

* Flag: **flag{R1v35t_Sh4m1r_Adl3m4N}**
* Expected difficulty: medium

## Description

This challenge is an RSA challenge that requires the use of different RSA related software to understand fundamental concepts on how RSA works and what software would go well with doing RSA activities in the future. It aims to teach how easy RSA can be cracked if one does not take care of not only their keys, but also uses faulty keys that are not well implemented into the code. This challenge aims at people using Python and OpenSSL.

## Challenge Solution

- Step one: Look at all the files and eliminate anything that does not have a public key that ends with the same number.
- Step two: Run the remaining public keys through OpenSSL to determine if they are valid using 
```
openssl rsa -noout -text -inform PEM -in publicX.pem -pubin
```
- Step three: The only valid key should be public0.pem. Run this key through Python
```
>>> from Crypto.PublicKey import RSA
>>> f = open("public.pem", "r")
>>> key = RSA.importKey(f.read())
>>> print key.n
>>> print key.e
```
- Step four: factor out the n to get the totient, which then gives you the d value you need.
Step five: decode c0 from base64 back to ascii, which should give you the RSA value for c0. Put c0 into the equation with d and n to decode c0 and the hint should tell you what other cipher texts are needed to be decoded. Considering the only working public key is public0.pem, it is implied that using the same values as before, one would simply decrypt those cipher texts mentioned, which are: c44, c50, and c55.
- Step six: assemble and submit the flag
