const express = require('express');
const fs = require('fs');
var bodyParser = require('body-parser');
var morgan = require('morgan');
const sigUtil = require('eth-sig-util');
const web3 = require('web3');
const Store = require('data-store');
const crypto = require('crypto');

const store = new Store({ path: 'completed.json' });

web3js = new web3(new web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws/v3/6651d8e65df847fab210600abf9efbf6"));

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(morgan('combined'));

app.enable('trust proxy');
app.set('trust proxy', true);

// Homepage
app.get('/', (request, response) => {
    fs.readFile("src/index.html", function(err, data){
        response.writeHead(200, {'Content-Type': 'text/html'});
        response.write(data);
        response.end();
    });
});

// FAQ
app.get('/faq', (request, response) => {
    fs.readFile("src/faq.html", function(err, data){
        response.writeHead(200, {'Content-Type': 'text/html'});
        response.write(data);
        response.end();
    });
});

// Challenge Pages
app.get('/challenge/:challengeId', (request, response) => {
    switch(request.params.challengeId) {
        case '1':
            fs.readFile("src/challenges/challenge1.html", function(err, data){
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.write(data);
                response.end();
            });
            break;
        case '2':
            fs.readFile("src/challenges/challenge2.html", function(err, data){
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.write(data);
                response.end();
            });
            break;
        case '3':
            fs.readFile("src/challenges/challenge3.html", function(err, data){
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.write(data);
                response.end();
            });
            break;
        case '4':
            fs.readFile("src/challenges/challenge4.html", function(err, data){
                response.writeHead(200, {'Content-Type': 'text/html'});
                response.write(data);
                response.end();
            });
            break;
        case '5':
            response.send("WIP");
            // fs.readFile("src/challenges/challenge5.html", function(err, data){
            //     response.writeHead(200, {'Content-Type': 'text/html'});
            //     response.write(data);
            //     response.end();
            // });
            break;
        default:
            // Challenge doesn't exist, redirect to homepage
            response.redirect("/");
    }
});

// Get flag API endpoint
app.post('/api/getflag', (request, response) => {
    // Custom message value signed
    const msgParams = [
        {
            type: 'string',
            name: 'Message',
            value: 'Give me the flag!'
        },
        {
            type: 'uint8',
            name: 'ChallengeNumber',
            value: request.body.challengeNum
        }
    ];

    // Recover signers public address
    let recovered;
    try {
        recovered = sigUtil.recoverTypedSignature({
            data: msgParams,
            sig: request.body.signedMsg
        });

        var challengeNum = parseInt(request.body.challengeNum)

        var cache_id = crypto.createHash('md5').update(recovered + challengeNum).digest('hex');

        // See if the user completion is cached
        if (store.get(cache_id)) {
            response.status(200).send(getFlag(challengeNum));
        }
        else {
            // Check if the address has completed the requested challenge
            deployerContract.methods.checkCompletionOf(recovered, challengeNum).call({},(err, event) => {
                if (err) {
                    // Something went wrong, show the user
                    console.log(err.message);
                    response.status(403).send("You have not completed this challenge!");
                }
                else {
                    // Successfully completed challenge
                    if (event == true) {
                        store.set(cache_id, true); 
                        
                        response.status(200).send(getFlag(parseInt(request.body.challengeNum)));
                    } else {
                        response.status(403).send("You have not completed this challenge!");
                    }
                }
            });            
        }
    } catch(err) {
        response.status(403).send("Malformed message");
    }
});

function getFlag(challengeNum) {
    switch(challengeNum) {
        case 0:
            return process.env.FLAG_1;
        case 1:
            return process.env.FLAG_2;
        case 2:
            return process.env.FLAG_3;
        case 3:
            return process.env.FLAG_4;
        case 4:
            return process.env.FLAG_5;
        default:
            return "<b>Error: </b>This challenge does not exist!";
    }
}

// Route js and css files
app.use("/", express.static('src/js'));
app.use("/", express.static('src/css'));

app.get('*', (request, response) => {
    response.redirect('/');
});

app.listen(port, (err) => {
    if (err) {
        return console.log('something bad happened', err);
    }

    console.log(`server is listening on ${port}`);
});

//contract abi is the array that you can get from the ethereum wallet or etherscan
var deployerABI;
try {
    deployerABI = [
    {
        "constant": false,
        "inputs": [
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "completeChallenge",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "deployChallenge",
        "outputs": [],
        "payable": true,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "name",
                "type": "string"
            }
        ],
        "name": "setNickname",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "newAddress",
                "type": "address"
            },
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "updateChallenge",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "challenge1",
                "type": "address"
            },
            {
                "name": "challenge2",
                "type": "address"
            },
            {
                "name": "challenge3",
                "type": "address"
            },
            {
                "name": "challenge4",
                "type": "address"
            },
            {
                "name": "challenge5",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "player",
                "type": "address"
            },
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "checkCompletionOf",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "player",
                "type": "address"
            },
            {
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "getAddressOf",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "player",
                "type": "address"
            }
        ],
        "name": "getNicknameOf",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "isOwner",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
];

// Address of Deployer contract
var deployerContractAddress = "0xd0b9a0e8635f70b6505e6217cad9a6a0ca456494";
// Creating contract object
var deployerContract = new web3js.eth.Contract(deployerABI, deployerContractAddress);
}
catch(error) {console.log(error);}
