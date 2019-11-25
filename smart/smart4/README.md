# [SwampCTF 2019 Smart Contract] Loan Bank

## Flavor Text

I've created an autonomous loan bank to handle payment tracking for loans to your friends. The contract works on good faith (or many threats) that your borrower will pay back with interest. However, you've noticed there's a short period of time where loans are in limbo waiting to be claimed. Find a way to drain the contract of all its Ether.

* Flag: `flag{w4tch_0ut_f0r_uniniti41iz3d_5t0r4g3_p0int3r5}`
* Expected difficulty: hard

## Description

The goal of this challenge is to get the competitor to understand the EVM memory layout. The exploit involves understanding the difference between memory and storage variables and where they point in memory. It also shows one of the dangers of not correctly initializing storage variables. Also requires the competitor to be able to convert variables into other types.

## Challenge Solution

The solution is realized through the `makeLoan` function. The storage variable `Loan storage l` is declared but not initialized, therefore it pointer points to storage starting at slot `0x0`, which conflicts with the variables declared at the top of the contract. Since a `Loan` struct has multiple properties that are all 32 bytes in size, these each point to successive 32 byte slots in storage where the contract variables live. The function stores user input directly into these slots which can be manipulated by the attacker to overwrite the values with arbitrary data.

    ...
    Loan storage l; // <-- Unsafe initialization
    l.id = bytes32(_id); // <-- Points to storage slot 0x0 (done to prevent the user from overwriting the implementation address in the Proxy contract)
    l.receiver = receiver; // <-- Points to storage slot 0x40 (largestLoaner). Recall the Loan struct declares amount variable first
    l.amount = amount; // <-- Points to storage slot 0x20 (owner)
    ...

  The solution is to call the `makeLoan` function with the competitors own address as the `receiver` and the `amount` equal to their address converted to a uint256 value, since the storage slot `0x20` (owner) is where `l.amount` is pointing to. Wei equal to the amount / `CONVERSION_RATE` must also be sent with the transaction to slightly obfuscate the solution. Once owner priveleges are gained, the `changeDebt` function can be called to change the loaned amount to the token value of the contracts balance, and `receiveLoan` can be called to retrieve the loan amount, which drains the contract of its funds.
