# Solidity Challenges Frontend for SwampCTF

## Deployment

`npm install`

`npm run start`

## What is this?
This is a site for deploying and checking completion of Solidity challenges for SwampCTF. We need a way to securely verify competitors have completed a challenge. Best way to see if competitors were able to understand and execute an exploit for the challenge is to have them exploit an actual live contract on the test network.

## Why is this?
CTFd doesn't support smart contract challenges and we need a way to securely verify competitors have completed the challenges. Best way to see if they were able to complete and understand a challenge is to have them exploit an actual live contract on the test network. Smart contract handles deployment and completion checking of contracts for competitors. Backend will return the flag to the user after sending an on chain transaction to check the user has completed the challenge.

## How do I compete?
Create an Ethereum account using the [MetaMask](https://metamask.io/) extension. Change your network to `Ropsten Test Network`. Copy the challenge contract code into a file on [Remix](https://remix.ethereum.org) and paste the deployed contracts address into the `At Address` space in the `Run` tab. You can interact with the contract through remix. Make sure your environment in Remix is `Inject Web3` on `Ropsten`. Get Ether at [Ropsten Faucet](https://faucet.metamask.io/)
