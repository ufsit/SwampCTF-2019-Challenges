// Wait for the page to load
window.addEventListener('load', async () => {
    // Checking if Web3 has been injected by the browser (Mist/MetaMask)
    if(window.ethereum && web3.eth.accounts.length === 0) {
        window.web3 = new Web3(ethereum);
        try {
            // Request account access if needed
            await ethereum.enable();
            console.log("Thank you for connecting");
            // Acccounts now exposed
        } catch (error) {
            if(web3.eth.accounts.length === 0) {
                // User denied account access...
                $( "#errorMsg" ).html("<b>Error: </b>" + error);
                $( "#deployBtn" ).addClass( "disabled" );
                $( "#deployBtn" ).html("<s>Deploy</s>");
                $( "#deployBtn" ).attr( "disabled", true );
            }
        }
    }
    else if(window.web3) {
        window.web3 = new Web3(web3.currentProvider);
    }
    else {
        $( "#errorMsg" ).html("<b>Error: </b>No web provider");
    }
    if (typeof web3 !== 'undefined') {
        deployerContract.getNicknameOf(web3.eth.accounts[0], (err, event) => {
            if(err)
                console.log(err);
            else
                $('#profile').html('<a target="_blank" href=' + 'https://ropsten.etherscan.io/address/' + web3.eth.accounts[0] + '>' + '<b>' + (event ? event : web3.eth.accounts[0]) + '</b>');
        });

        // Use Mist/MetaMask's provider
        web3.version.getNetwork((err, netId) => {
            switch (netId) {
                // Network ID = 3 is Ropsten Test Net
                case "3":
                    // If we have access to the account
                    if(web3.eth.accounts.length > 0) {
                        // Check if the user already has a contract deployed
                        var getDeployedAddress = deployerContract.getAddressOf(web3.eth.accounts[0],CHALLENGE_NUM,(err, event) => {
                            if(err) {
                                $( "#errorMsg" ).html("<b>Error: </b>Could not deploy the contract");
                                console.log(err.message);
                            }
                            else {
                                // Contract is deployed, show the user
                                if(event != "0x0000000000000000000000000000000000000000") {
                                    $( "#deployBtn" ).hide();
                                    $( "#notif" ).html("Contract deployed at address: <a><a style='padding-right:5px;overflow-wrap:break-word;' target='_blank' href='https://ropsten.etherscan.io/address/" + event + "'>" + event + "</a><button class='fas btn fa-copy copy-button' onclick=\"copyToClipboard('" + event + "')\"></button></a>");
                                    $( "#checkSolutionContainer" ).show();
                                    $( "#startOverBtn" ).click(() => {
                                        deployChallenge();
                                    });

                                    checkCompletion();

                                    // Set click listener for check solution button
                                    $( "#checkSolutionBtn" ).click(() => {
                                        // Send the checkCompletion transaction to the deployer contract
                                        web3.eth.sendTransaction({to:deployerContractAddress, from:web3.eth.accounts[0], value: 0, data: completeContract[CHALLENGE_NUM]}, (err, event) => {
                                            if(err) {
                                                $( "#errorMsg" ).html("<b>Error: </b>Could not check completion");
                                                console.log(err.message);
                                            }
                                            else {
                                                // Set that spinner going
                                                $( "#check-btn-text" ).hide();
                                                $( "#check-btn-spinner" ).show();
                                                // Wait for on chain transaction receipt then check if completed = true
                                                return getTransactionReceiptMined(web3, event).then(function (receipt) {
                                                    setTimeout(checkCompletion(true), 5000);
                                                }, 5000);
                                            }
                                        });
                                    });
                                }
                            }
                        });
                        // Set the js for clicking deploy button
                        $( "#deployBtn" ).click(function() {
                            if(!$( "#deployBtn" ).hasClass("disabled")) {
                                // Ask MetaMask to have access to users account
                                window.ethereum.enable().then((account) => {
                                    console.log("Thank you for connecting with account " + account);
                                    deployChallenge();
                                });
                            }
                        });
                    }
                    break
                default:
                    // User is not on Ropsten Test Net
                    $( "#deployBtn" ).addClass( "disabled" );
                    $( "#deployBtn" ).html("<s>Deploy</s>");
                    $( "#deployBtn" ).attr( "disabled", true );
                    $( "#errorMsg" ).html("<b>Error: </b>Please connect to the Ropsten Test Network");
                    $( "#wrongNetworkModal" ).modal({show:true});
            }
        });
    } else {
        // Handle the case where the user doesn't have web3. Probably 
        // show them a message telling them to install Metamask in 
        // order to use our app.
        // For example
        // web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
        console.log("No web provider");
        $( "#deployBtn" ).addClass( "disabled" );
        $( "#deployBtn" ).html("<s>Deploy</s>");
        $( "#deployBtn" ).attr( "disabled", true );
        $( "#errorMsg" ).html("<b>Error: </b>No web provider");
    }
});

function deployChallenge() {
    // Deploy the challenge to the ropsten network
    web3.eth.sendTransaction({to:deployerContractAddress, from:web3.eth.accounts[0], value: web3.toWei(0.5), data: deployContract[CHALLENGE_NUM]}, (err, event) => {
        if(err) {
            // Something went wrong, show the user
            $( "#errorMsg" ).html("<b>Error: </b>Could not deploy contract");
            console.log(err.message);
        }
        else {
            // Set the spinners going
            $( "#errorMsg" ).html("");
            $( "#deploy-btn-text" ).hide();
            $( "#deploy-btn-spinner" ).show();
            $( "#check-btn-text" ).hide();
            $( "#check-btn-spinner" ).show();

            // Wait for the on chain transaction receipt
            return getTransactionReceiptMined(web3, event).then(function (receipt) {
                setTimeout(() => {
                    // Check if the user has completed the challenge
                    checkCompletion();

                    // Get the address the challenge is deployed at
                    var getDeployedAddress = deployerContract.getAddressOf(web3.eth.accounts[0],CHALLENGE_NUM,(err, event) => {
                        if(err) {
                            $( "#errorMsg" ).html("<b>Error: </b>Could not retrieve contract address.");
                            console.log(err);
                        }
                        else {
                            // If the challenge is deployed
                            if(event != "0x0000000000000000000000000000000000000000") {
                                $( "#deployBtn" ).hide();
                                $( "#notif" ).html("Contract deployed at address: <a><a style='padding-right:5px;overflow-wrap:break-word;'  target='_blank' href='https://ropsten.etherscan.io/address/" + event + "'>" + event + "</a><button class='fas btn fa-copy copy-button' onclick=\"copyToClipboard('" + event + "')\"></button></a>");
                                $( "#checkSolutionContainer" ).show();
                            }
                            // The challenge isn't deployed, try to get the address again
                            else {
                                setTimeout(() => {
                                    deployerContract.getAddressOf(web3.eth.accounts[0],CHALLENGE_NUM,(err, event) => {
                                        if(event != "0x0000000000000000000000000000000000000000") {
                                            $( "#deployBtn" ).hide();
                                            $( "#notif" ).html("Contract deployed at address: <a><a style='padding-right:5px;overflow-wrap:break-word;' target='_blank' href='https://ropsten.etherscan.io/address/" + event + "'>" + event + "</a><button class='fas btn fa-copy copy-button' onclick=\"copyToClipboard('" + event + "')\"></button></a>");
                                            $( "#checkSolutionContainer" ).show();
                                        } else {
                                            $( "#errorMsg" ).html("<b>Error: </b>Could not retrieve contract address.");
                                        }
                                    });
                                }, 5000);
                            }
                        }
                        // Done, reset spinners
                        $( "#deploy-btn-text" ).show();
                        $( "#deploy-btn-spinner" ).hide();
                        $( "#check-btn-text" ).show();
                        $( "#check-btn-spinner" ).hide();
                    });
                }, 5000);
            });
            
        }
    });
}

const copyToClipboard = str => {
    const el = document.createElement('textarea');  // Create a <textarea> element
    el.value = str;                                 // Set its value to the string that you want copied
    el.setAttribute('readonly', '');                // Make it readonly to be tamper-proof
    el.style.position = 'absolute';                 
    el.style.left = '-9999px';                      // Move outside the screen to make it invisible
    document.body.appendChild(el);                  // Append the <textarea> element to the HTML document
    const selected =            
      document.getSelection().rangeCount > 0        // Check if there is any content selected previously
        ? document.getSelection().getRangeAt(0)     // Store selection if found
        : false;                                    // Mark as false to know no selection existed before
    el.select();                                    // Select the <textarea> content
    document.execCommand('copy');                   // Copy - only works as a result of a user action (e.g. click events)
    document.body.removeChild(el);                  // Remove the <textarea> element
    if (selected) {                                 // If a selection existed before copying
      document.getSelection().removeAllRanges();    // Unselect everything on the HTML document
      document.getSelection().addRange(selected);   // Restore the original selection
    }
};

function checkCompletion(showErr) {
    // Check if user has completed contract
    deployerContract.checkCompletionOf(web3.eth.accounts[0],CHALLENGE_NUM,(err, event) => {
        if(err) {
            // Something went wrong, show the user
            $( "#errorMsg" ).html("<b>Error: </b>Something went wrong, refresh the page");
            console.log(err.message);
        }
        else {
            // Successfully completed challenge
            if(event == true) {
                surprise();
                $( "#checkSolutionBtn" ).hide();
                $( "#getFlagBtn" ).show();
                $( "#getFlagBtn" ).click(() => {
                    const msgParams = [
                        {
                            type: 'string',      // Any valid solidity type
                            name: 'Message',     // Any string label you want
                            value: 'Give me the flag!'  // The value to sign
                        },
                        {
                            type: 'uint8',
                            name: 'ChallengeNumber',
                            value: CHALLENGE_NUM
                        }
                    ];
                    web3.currentProvider.sendAsync({
                        method: 'eth_signTypedData',
                        params: [msgParams, web3.eth.accounts[0]],
                        from: web3.eth.accounts[0],
                    }, (err, result) => {
                        if (err) {
                            $( "#errorMsg" ).html("<b>Error: </b> Something went wrong!");
                            return console.error(err);
                        }
                        if (result.error) {
                            $( "#errorMsg" ).html("<b>Error: </b>User denied message signature.");
                            return;
                        }
                        let signed = result.result;
                        $.ajax({
                            url: "/api/getflag",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({
                                challengeNum: CHALLENGE_NUM,
                                signedMsg: signed
                            }), success: function (result) {
                                alert(result);
                            },
                            error: function(err) {
                                console.log(err);
                            }
                        });
                    });
                });
                $( "#challenge-title" ).css({"text-decoration": "line-through"});
            }
            else {
                // Error won't be shown if user didn't call this through Check Completion button
                if(showErr) {
                    $( "#errorMsg").html("<b>Incorrect:</b> Please try again or try refreshing the page");
                }
                // Challenge isn't completed, no check mark for you
                $( "#checkmark" ).hide();
                $( "#challenge-title" ).css({"text-decoration": ""});
            }
            // Reset that spinner
            $( "#check-btn-text" ).show();
            $( "#check-btn-spinner" ).hide();
        }
    });
}