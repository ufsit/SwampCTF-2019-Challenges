# [SwampCTF 2019 Smart Contract] Hash Slinging Slasher

## Flavor Text

Try to guess the random number I chose. I've hashed the value before storing it in the contract so you can't cheat! You'll never figure this one out :)

* Flag: `flag{0n_th3_b10ckch41n_3v3ryth1ng_15_pub1ic}`
* Expected difficulty: easy

## Description

The goal of this challenge is to reinforce that all data in contracts is publicly available and that sensitive data must still be securely encrypted before being stored on chain.

## Challenge Solution

The solution is the range of potential values the answer can be is limited to a uint8 variable. The competitor must hash values 1-256 and find the correct value.
