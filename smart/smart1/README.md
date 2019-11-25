# [SwampCTF 2019 Smart Contract] Multi-Owner Contract

## Flavor Text

My friend wanted to create a new type of ownable contract where multiple people can be owners. However, when he deployed it for his token sale, someone managed to add themself and many other owners and they minted tons of their own tokens! Luckily the sale hasn't started yet, help him find the bug so he can deploy a new contract and save his ICO.

* Flag: `flag{3v3ryb0dy5_hum4n_r34d_c10s31y}`
* Expected difficulty: trivial

## Description

The goal of this challenge is to teach the basics of creating an Ethereum account and interacting with contracts in the wild.

## Challenge Solution

The solution is the function `contructor` is mispelled, leading to the code block not being called on contract instantiation but being able to be called normally as a function. All the competitor has to do is call the `contructor` function on the on-chain contract.
