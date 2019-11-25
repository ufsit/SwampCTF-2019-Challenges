pragma solidity ^0.4.24;

contract HashSlingingSlasher {
    
    bytes32 answer = 0xed2a0ca74e236c332625ad7f4db75b63d2a2ee7e3fe52c2c93c8dbc4e06906d1;
    
    constructor() public payable {
        require(msg.value == 0.5 ether, "Must send 0.5 Ether");        
    }

    /** Guess the hashed number. Refunds ether if guessed correctly
     */
    function guess(uint16 number) public payable {
        require(msg.value == 0.25 ether);
        if(keccak256(abi.encodePacked(number)) == answer) {
            msg.sender.transfer(address(this).balance);
        }
    }
    
    /** Returns balance of this contract
     */
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    /** CTF helper function
     *  Used to check if challenge is complete
     */
    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }
    
}