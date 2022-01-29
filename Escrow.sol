// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract Escrow {

    //VARIABLES
    enum State {SETUP, NOT_INITIATED, AWAITING_PAYMENT, AWAITING_DELIVERY, COMPLETED, DISPUTED}

    State public currState;
    bool public isBuyerin;
    bool public isSellerin;

    uint public price;
    address public buyer;
    address public owner;
    address payable public seller;

    //MODIFIERS
    modifier beforeSetup(){
        require(currState == State.SETUP, "ESCROW has been SETUP!");
        _;
    }

    modifier onlyBuyer(){
        require(msg.sender == buyer, "Only Buyer can call the function!");
        _;
    }

    modifier onlyOwner(){
        require(msg.sender == owner, "Only Owner can call the function!");
        _;
    }

    modifier escrowNotStarted(){
        require(currState == State.NOT_INITIATED, "ESCROW has been initiated!");
        _;
    }

    //FUNCTIONS
    constructor() public{
        owner = msg.sender;
    }

    function setupContract(address _buyer, address payable _seller, uint _price) public onlyOwner beforeSetup {
        buyer = _buyer;
        seller = _seller;
        price = _price * (1 ether);
        currState = State.NOT_INITIATED;
    }

    function initContract() escrowNotStarted public{
        if(msg.sender == buyer){
            isBuyerin = true;
        }
        if(msg.sender == seller){
            isSellerin = true;
        }
        if(isBuyerin && isSellerin){
            currState = State.AWAITING_PAYMENT;
        }

    }

    function deposit() public payable onlyBuyer{
        require(currState == State.AWAITING_PAYMENT, "Payment Already Paid or NOT Initiated");
        require(msg.value == price, "Amount not same as agreed upon");
        currState = State.AWAITING_DELIVERY;
    }

    function confirmDelivery() public payable onlyBuyer{
        require(currState == State.AWAITING_DELIVERY, "Payment NOT deposited or NOT Initiated!");
        seller.transfer(price);
        currState = State.COMPLETED;
    }

    function withdraw() public payable onlyBuyer{
        require(currState == State.AWAITING_DELIVERY, "Payment cannot be withdrawn at this stage!");
        payable(msg.sender).transfer(price);
        currState = State.DISPUTED;
    }
}