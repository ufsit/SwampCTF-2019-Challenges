# [SwampCTF 2019 Smart Contract] Refundable Purchase

## Flavor Text

I've created a contract to make buying items online safer! (for the buyer at least) The funds stay in escrow in the contract until the buyer has received the item, in which they report they've received it (people are always honest, right!?). If they never receive the item, they can call refund to return their spent ether. Find a way to drain this contract of all pending refunds.

* Flag: `flag{c411_15_n0t_s4f3_w1th_n0_g45_1imit}`
* Expected difficulty: medium

## Description

The goal of this challenge is to get the competitor to write a contract that will interact with the challenge contract. This requires the competitor learn how to call a function of a contract from another contract and forward funds. It also requires the competitor to understand reentrancy, a bug where an untrusted contract is called before state changes are made.

## Challenge Solution

The solution is to write a contract which can forward funds to the challenge contract. The sent Ethers must evenly divide the total Ether in the target contract since the number of times the refund function is repeated must be an integer. The `refund` function executes `msg.sender.call.value(amount)("");` before changing the `refund` mapping value to `0`, so the exploit contract can override the default payable function and call the `refund` function again before the state is updated. This means the `require(refunds[msg.sender] > 0);` check will pass as many times as we call `refund` again in our default payable function. The only thing left is to add a if statement to check the target contracts balance is greater than 0 so the loop doesn't execute forever and revert due to being out of gas.
