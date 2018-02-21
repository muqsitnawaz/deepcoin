reate a wallet using password 't t t t t' (5 words)
$ curl -X POST --header 'Content-Type: application/json' -d '{ "password": "t t t t t"  }' 'http://localhost:3001/operator/wallets'
{"id":"a2fb4d3f93ea3d4624243c03f507295c0c7cb5b78291a651e5575dcd03dfeeeb","addresses":[]}

# Create two addresses for the wallet created (replace walletId)
$ curl -X POST --header 'Content-Type: application/json' --header 'password: t t t t t' 'http://localhost:3001/operator/wallets/a2fb4d3f93ea3d4624243c03f507295c0c7cb5b78291a651e5575dcd03dfeeeb/addresses'
{"address":"e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"}

$ curl -X POST --header 'Content-Type: application/json' --header 'password: t t t t t' 'http://localhost:3001/operator/wallets/a2fb4d3f93ea3d4624243c03f507295c0c7cb5b78291a651e5575dcd03dfeeeb/addresses'
{"address":"c3c96504e432e35caa94c30034e70994663988ab80f94e4b526829c99958afa8"}

# Mine a block to the address 1 so we can have some coins
$ curl -X POST --header 'Content-Type: application/json' -d '{ "rewardAddress": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"  }' 'http://localhost:3001/miner/mine'
{
    "index": 1,
    "nonce": 1,
    "previousHash": "c4e0b8df46ce5cb2bcb0379ab0840228536cf4cd489783532a7c9d199754d1ed",
    "timestamp": 1493475731.692,
    "transactions": [
    {
            "id": "ab872b412afe62a087f3a8c354a27377f5fda33d7c98a1db3b1b0985801a6784",
            "hash": "423bae0bd2f4782f34c770df5be21f856b468a45bf88bb146da8ec2fe0fd3d21",
            "type": "reward",
            "data": {
                "inputs": [],
                "outputs": [
                {
                        "amount": 5000000000,
                        "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
                    
                }
                
                ]
            
            }
        
    }
    
    ],
    "hash": "0311a3a89198ccf888c76337cc190e2db238b67a7db0d5062aac97d14fb679b4"

}

# Create a transaction that transfer 1000000000 satoshis from address 1 to address 2
$ curl -X POST --header 'Content-Type: application/json' --header 'password: t t t t t' -d '{ "fromAddress": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c", "toAddress": "c3c96504e432e35caa94c30034e70994663988ab80f94e4b526829c99958afa8", "amount": 1000000000, "changeAddress": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"  }' 'http://localhost:3001/operator/wallets/a2fb4d3f93ea3d4624243c03f507295c0c7cb5b78291a651e5575dcd03dfeeeb/transactions'
{
  "id": "c3c1e6fbff949042b065dc9e22d065a54ab826595fd8877d2be8ddb8cbb0e27f",
  "hash": "3b5bbf698031e437787fe7b31f098e214a1eeff01fee9b95c22bccf20146982c",
  "type": "regular",
  "data": {
    "inputs": [
    {
        "transaction": "ab872b412afe62a087f3a8c354a27377f5fda33d7c98a1db3b1b0985801a6784",
        "index": "0",
        "amount": 5000000000,
        "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c",
        "signature": "4500f432d6b400811d83364224ce62bccd042ad92299118c0672bc5bc1390ffdfdbef135f36927d8bd77843f3a0b868d9ed3a5346dcbeda6c06f33876cfae00d"
      
    }
    
    ],
    "outputs": [
    {
        "amount": 1000000000,
        "address": "c3c96504e432e35caa94c30034e70994663988ab80f94e4b526829c99958afa8"
      
    },
    {
        "amount": 3999999999,
        "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
      
    }
    
    ]
  
  }

}

# Mine a new block containing that transaction
$ curl -X POST --header 'Content-Type: application/json' -d '{ "rewardAddress": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"  }' 'http://localhost:3001/miner/mine'
{
  "index": 2,
  "nonce": 6,
  "previousHash": "0311a3a89198ccf888c76337cc190e2db238b67a7db0d5062aac97d14fb679b4",
  "timestamp": 1493475953.226,
  "transactions": [
  {
      "id": "c3c1e6fbff949042b065dc9e22d065a54ab826595fd8877d2be8ddb8cbb0e27f",
      "hash": "3b5bbf698031e437787fe7b31f098e214a1eeff01fee9b95c22bccf20146982c",
      "type": "regular",
      "data": {
        "inputs": [
        {
            "transaction": "ab872b412afe62a087f3a8c354a27377f5fda33d7c98a1db3b1b0985801a6784",
            "index": "0",
            "amount": 5000000000,
            "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c",
            "signature": "4500f432d6b400811d83364224ce62bccd042ad92299118c0672bc5bc1390ffdfdbef135f36927d8bd77843f3a0b868d9ed3a5346dcbeda6c06f33876cfae00d"
          
        }
        
        ],
        "outputs": [
        {
            "amount": 1000000000,
            "address": "c3c96504e432e35caa94c30034e70994663988ab80f94e4b526829c99958afa8"
          
        },
        {
            "amount": 3999999999,
            "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
          
        }
        
        ]
      
      }
    
  },
  {
      "id": "6b55b1e85369743f360edd5bedc3467eba81b35c2b88490686eee90946231dd6",
      "hash": "86f5b4a40c027e1ef7e060dd9b9ab7ae48258f3a43dfc19d9d8111c396463b8c",
      "type": "fee",
      "data": {
        "inputs": [],
        "outputs": [
        {
            "amount": 1,
            "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
          
        }
        
        ]
      
      }
    
  },
  {
      "id": "0f6f6c04602ac1bea15157a1a86978d46488a7865fa3db3bfc581a1407950599",
      "hash": "f9fa281fbf9ffd3d63dd0c3503588fe3010dd6740a4a960b98d1be4aa1fa7a05",
      "type": "reward",
      "data": {
        "inputs": [],
        "outputs": [
        {
            "amount": 5000000000,
            "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
          
        }
        
        ]
      
      }
    
  }
  
  ],
  "hash": "08861fc4864ba0bf7a899db9ffaaa39376ad3857b1115951db074e3d06f93a5f"

}

# Check how many confirmations that transaction has.
$ curl -X GET --header 'Content-Type: application/json' 'http://localhost:3001/node/transactions/c3c1e6fbff949042b065dc9e22d065a54ab826595fd8877d2be8ddb8cbb0e27f/confirmations'
{"confirmations":1}

# Get address 1 balance
$ curl -X GET --header 'Content-Type: application/json' 'http://localhost:3001/operator/e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c/balance'
{"balance":9000000000}

# Get address 2 balance
$ curl -X GET --header 'Content-Type: application/json' 'http://localhost:3001/operator/c574de33acfd82f2146d2f45f37ce95b7bdca133b8ad310adbd46938c75992c8/balance'
{"balance":1000000000}

# Get unspent transactions for address 1
$ curl -X GET --header 'Content-Type: application/json' 'http://localhost:3001/blockchain/transactions/unspent?address=e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c'
[
{
    "transaction": "c3c1e6fbff949042b065dc9e22d065a54ab826595fd8877d2be8ddb8cbb0e27f",
    "index": "1",
    "amount": 3999999999,
    "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
  
},
{
    "transaction": "6b55b1e85369743f360edd5bedc3467eba81b35c2b88490686eee90946231dd6",
    "index": "0",
    "amount": 1,
    "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
  
},
{
    "transaction": "0f6f6c04602ac1bea15157a1a86978d46488a7865fa3db3bfc581a1407950599",
    "index": "0",
    "amount": 5000000000,
    "address": "e155df3a1bac05f88321b73931b48b54ea4300be9d1225e0b62638f537e5544c"
  
}

]
