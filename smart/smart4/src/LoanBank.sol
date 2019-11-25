pragma solidity ^0.4.24;

contract LoanBank {
    
    bytes32 _id;
    address public owner;
    
    // TODO: Add functionality for variables
    uint256 totalLoans;
    address public largestLoaner;
    
    uint256 CONVERSION_RATE;
    uint256 LOAN_INTEREST; // Represented in percentage / 100
    
    mapping(address => Loan) public loans;

    struct Loan {
        bytes32 id;
        uint256 amount;
        address receiver;
        bool received;
    }

    constructor() public payable {
        require(msg.value == 0.5 ether, "Must send 0.5 ether");
        owner = msg.sender;
    }

    function init() public {
        CONVERSION_RATE = 10**18 * 1 ether;
        LOAN_INTEREST = 5;
    }

    /** Function called to loan eth to an address
     */
    function makeLoan(address receiver, uint256 amount) public payable {
        require(msg.value == tokenToWei(amount));
        require(msg.value > 0);

        Loan storage l;
        l.id = bytes32(_id);
        l.receiver = receiver;
        l.amount = amount;

        loans[msg.sender] = l;
    }

    /** Call to receive loaned eth
     */
    function receiveLoan(address loaner) public {
        require(!loans[loaner].received);

        loans[loaner].received = true;
        
        msg.sender.transfer(tokenToWei(loans[loaner].amount));
    }

    /** Call to pay off loan back to loaner
     */
    function payOffLoan(address loaner) public payable {
        require(msg.value > tokenToWei(loans[loaner].amount * (LOAN_INTEREST / 100)));
        require(loans[loaner].receiver == msg.sender);

        // Immediately forward funds to loaner
        loaner.transfer(tokenToWei(loans[loaner].amount * (LOAN_INTEREST / 100)));

        delete loans[loaner];
    }

    /** Allows the owner to modify debt amount
     */
    function changeDebt(address loaner, uint256 amount) public onlyOwner {
        loans[loaner].amount = amount;
    }
    
    /** Convert Wei to token amount
     */
    function weiToToken(uint256 amount) internal returns (uint256) {
        return amount * CONVERSION_RATE;
    }
    
    /** Convert token to Wei amount
     */
    function tokenToWei(uint256 amount) internal returns (uint256) {
        return amount / CONVERSION_RATE;
    }

    modifier onlyOwner() {
        require(owner == msg.sender);
        _;
    }
    
    /** CTF helper function
     */
    function getBalance() public view returns (uint256) {
        return this.balance;
    }

    /** CTF helper function. Called to check chalenge is completed
     */
    function isComplete() public view returns (bool) {
        return this.balance == 0;
    }

}
