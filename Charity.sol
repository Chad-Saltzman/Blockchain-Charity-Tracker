
pragma solidity >=0.7.0 <0.9.0;


/**
 * @title Charity
 * @dev Implements the tracking of a charities donation ammount and status of donations
 */
 
 contract Charity {
     
     struct Status{
         string donationAddress;
         string status;
     }
     
     struct Contributer {
         address personalAddress;
         uint256 totalDonated;
     }
     
     struct CharityDetails {
         address charityAdd;
         string charityName;
         uint256 totalDonation;
     }
     
     Status[] statuses;
     CharityDetails[] charities;
     Contributer[] contributers;
     address[] private charityAddresses;
     
     
     
     constructor(string[] memory CharityName, address[] memory CharityAdd) payable {
         require(CharityName.length == CharityAdd.length, "Number of Charities is not equal to the number of addresses");
         
         for (uint256 i = 0; i < CharityAdd.length; i++){
             charityAddresses.push(CharityAdd[i]);
         }
         for (uint256 i = 0; i < CharityName.length; i++){
                charities.push(CharityDetails({
                charityAdd: CharityAdd[i],
                charityName: CharityName[i],
                totalDonation: 0
            }));
         }
     } 
     
     
     
     // Takes a donation value as input and stores it
     function contributeDonation(uint256 num, string memory trx, string memory CharityName) public 
     {
      /*  address contributeradd = msg.sender;
        bool found = false;
        require(contributeradd.balance >= num, "Unfortunately there are insufficient funds for a donation of that size");
        */
        for (uint256 i = 0; i < charities.length; i++){
             if (keccak256(bytes(charities[i].charityName)) == keccak256(bytes(CharityName))){
                 charities[i].totalDonation += num;
             }
         }
        
        
        address contributeradd = msg.sender;
        bool found = false; // Resets found variable for next check
        for (uint256 i = 0; i < contributers.length; i++){
            if (contributers[i].personalAddress == contributeradd){
                found = true;
                break;
            }
        }
        
        // creates a new contributer if it does not exist already
        if (found == false){ 
            contributers.push(Contributer({
                personalAddress: contributeradd,
                totalDonated: 0
            }));
        }
        // Adds donation ammount to contributers total donated
         for (uint256 i = 0; i < contributers.length; i++){
            if (contributers[i].personalAddress == contributeradd){
                contributers[i].totalDonated += num;
                break;
            }
         }
         // creates inital status 
         statuses.push(Status({
                donationAddress: trx,
                status: "Initial Donation"
            }));
           
         
    }
    
    // Takes a transaction address and status value as input and updates the status of the transaction
     function updateStatus(string memory newStatus, string memory trx) public {
        bool found = false;
        for (uint i = 0; i < statuses.length; i++) {
            if(keccak256(bytes(statuses[i].donationAddress)) == keccak256(bytes(trx))){
                statuses[i].status = newStatus;
                found = true;
                break;
            }
        }
        if (found == false){
            // 'Status({...})' creates a temporary
            // Status object and 'statuses.push(...)'
            // appends it to the end of 'statuses'.
            statuses.push(Status({
                donationAddress: trx,
                status: newStatus
            }));
        }
    }
    
    function getStatus(string memory trx) public view 
            returns (string memory status)
    {
        bool found = false;
        for (uint i = 0; i < statuses.length; i++) {
            if(keccak256(bytes(statuses[i].donationAddress)) == keccak256(bytes(trx))){
                status = statuses[i].status;
                found = true;
            }   
        }
        require(found, "the transaction hash was not found");
    }
     
    function getCharityAddress(string memory searchCharityName) public view
            returns (address tempAdd)
    {
        for (uint i = 0; i < charities.length; i++){
            if (keccak256(bytes(charities[i].charityName)) == keccak256(bytes(searchCharityName))  ){
                tempAdd = charities[i].charityAdd;
            }
        }
        
    }
     
    function getBalance(address UserAddress) public view
            returns (uint256)
    {
        return UserAddress.balance;   
        
    }
     
    function getTotalDonated(string memory searchCharityName) public view
            returns (uint256 runningTotal)
        {
            runningTotal = 1;
            for (uint256 i = 0; i < charities.length; i++){
                if (keccak256(bytes(charities[i].charityName)) == keccak256(bytes(searchCharityName))  ) {
                     runningTotal = charities[i].totalDonation;
                }
            }
        }
                 

     
     
     
     
     
     
     
     
     
     
     
 }