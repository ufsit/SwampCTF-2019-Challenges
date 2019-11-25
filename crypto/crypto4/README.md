# [SwampCTF 2019 Crypto] We Three Keys

## Flavor Text

In this modern world of cyber, keys are the new kings of the world. In fact, we will let you use the 3 best keys that I could find, make sure to see what they offer to you!

* Flag: `flag{w0w_wh4t_l4zy_k3yz_much_w34k_crypt0_f41ls!}`
* Expected difficulty: easy

## Description

This challenge was created to show how AES-CBC is vulnerable if the IV matches the key.
The IV can be found if there is a way to encrypt and decrypt data, but if the key matches the IV this could be dangerous for forging text.
Additionally, data must be sent in its hex representation because not all bytes will be printable. Participants must learn how to do this efficiently in a language like python.

## Challenge Solution

In order to solve this challenge, first the python code should be audited and competitors should realize two major things, AES-CBC is used and the key equals the IV.
Both encryption and decryption are allowed, so we have a strong decryption oracle, and the structure of CBC is important.
When decrypting, the decryption of one block is the AES decryption in standard (ECB) mode, then this is xored with the previous ciphertext.
The exception to this is that the first block is xored with the IV instead of the previous ciphertext.
If a block is set to null bytes and then decrypted, the next block would be decrypted with AES and xored with nothing.
The trick is that we will send the first and third decrypted blocks to be the same, and these xored together will be the IV (and key).
This should be repeated for all of the three keys, and each should be recognized as part of the flag.
In all honestly, we do not have to encrypt the plaintext first, as any decryption in which the first and third blocks and the second is null should work.
However, I do this in my exploit to demonstrate why this works and see how the initial encrypted blocks are created.
