# API 
We have started working on a free API for developers to grab waltonchain blockchain data. The documentation is below.
NOTE THAT ALL SITE REQUESTS ARE LIMITED TO 3000 PER HOUR. Please contact us if you are having issues. 
## Single Block
You can use this to request the information for a block by block number.

Usage:

  >> curl http://wtcexplorer.io/api/getBlock/150000
  
Sample Output:

    {
      "blockNum": 161924, 
      "difficulty": 992116588580, 
      "extra_data": "Windows", 
      "gasUsed": 0, 
      "hash": "0xf3e1aebc0e16ef37726e9de830e9bf07b277569a5c1ac7dc56629f584d08c597", 
      "miner": "0x8cfb846942e9103550051d703d746dc3b8101822", 
      "nonce": "0xca0a929c499cef95", 
      "timest": "Thu, 26 Jul 2018 01:42:40 GMT", 
      "totaldifficulty": 77397208677506629
    }
## Most Recent Block
You can use this to request the information for a block by block number.

Usage:

  >> curl http://wtcexplorer.io/api/getLatestBlock
  
Sample Output:

    161948
## Single Transaction
You can use this to request the information for a transaction by hash.

Usage:

  >> curl http://wtcexplorer.io/api/getTransaction/{{hash}}
  
Sample Output:

    [
    {
      "blockHash": "0xaded4329c8267810c3e33d50e2b7f0152154388785b2cefc7a1cfd154923d30c", 
      "blockNum": 161071, 
      "gas": "18000000000", 
      "hash": "0xd25653785e0b922fb9e945bfe414874d471bc2a2958f54cc1d0c8003923a9683", 
      "inputData": "0x", 
      "r": "0xd87f9ac7349ad244aae66139d65f8e018ebd2480d4592a70a8a7dcad3a1e0944", 
      "reciever": "0xc4f0b0e754d6c2fa499bc2cc532c6068902b3705", 
      "s": "0x2527e1a5e48c2b4081613083f9abaedcf9088327ebd4d4bd62d8a7446fe27466", 
      "sender": "0xbb1ac81c5864f550f6e82f703f2bed275e89ff6e", 
      "timest": "Wed, 25 Jul 2018 10:21:40 GMT", 
      "value": "0.1"
    }
    ] 
## Transactions per Block
You can use this to request the information for all transactions in a block.

Usage:

  >> curl http://wtcexplorer.io/api/getBlockTransactions/{{path:block}}
  
Sample Output:

    [
    {
      "blockHash": "0x230efcba65e7c64f9cba8ec8879761293641d7304b42b920ee25a18ef67f9891", 
      "blockNum": 159551, 
      "gas": "18000000000", 
      "hash": "0x2c0870aff2c20e6e64a54e60e1e4f7fdeefaf37a0ba1d3e9265e66a7028af5e4", 
      "inputData": "0x", 
      "r": "0x2226cbe6a51d0f3cd85ff31fd3f07f54a15a93dc96ab24b05144824757805def", 
      "reciever": "0x9d556a85b1ec834427b9b9da5c796ab0c8fe7d6d", 
      "s": "0x36aefc989ad9d5d02e9f19229b5728a7993ced06a6c5e083d72ea9b09a30c6e1", 
      "sender": "0xbb1ac81c5864f550f6e82f703f2bed275e89ff6e", 
      "timest": "Tue, 24 Jul 2018 07:13:52 GMT", 
      "value": "0.0001"
    }, 
    {
      "blockHash": "0x230efcba65e7c64f9cba8ec8879761293641d7304b42b920ee25a18ef67f9891", 
      "blockNum": 159551, 
      "gas": "18000000000", 
      "hash": "0x4d1ddc4be0c60d53778288786d96c64460d324895544a4e20cadb17827fafd13", 
      "inputData": "0x", 
      "r": "0x3afd5d70cb991034d4415917b022a4b4b764f9e10b251130e7a659bff1902219", 
      "reciever": "0x9d556a85b1ec834427b9b9da5c796ab0c8fe7d6d", 
      "s": "0x627554559c4971f46a5980fa73198d644933a0da01f5844c5d59a2c4c30ed372", 
      "sender": "0xbb1ac81c5864f550f6e82f703f2bed275e89ff6e", 
      "timest": "Tue, 24 Jul 2018 07:13:52 GMT", 
      "value": "0.0001"
    }, 
    {
      "blockHash": "0x230efcba65e7c64f9cba8ec8879761293641d7304b42b920ee25a18ef67f9891", 
      "blockNum": 159551, 
      "gas": "18000000000", 
      "hash": "0x9da2ac9b80001802f092882feacd921b18eaaedf1c1f9720a5a0a2da6459077a", 
      "inputData": "0x", 
      "r": "0x11a3d383970a2cd4d8adcf474543fa24ea48bd826da04af82c9ad05ab9f75e08", 
      "reciever": "0x9d556a85b1ec834427b9b9da5c796ab0c8fe7d6d", 
      "s": "0x793f9656558d06fab7cabee128f7fe1b8d973d0f92158631f798f876d53855fc", 
      "sender": "0xbb1ac81c5864f550f6e82f703f2bed275e89ff6e", 
      "timest": "Tue, 24 Jul 2018 07:13:52 GMT", 
      "value": "0.0001"
    }
    ] 
## Last X Blocks
You can use this to request the information for the last X block.

Usage:

  >> curl http://wtcexplorer.io/api/getLastBlocks/2
  
Sample Output:

    [
    {
      "blockNum": 161924, 
      "difficulty": 992116588580, 
      "extra_data": "Windows", 
      "gasUsed": 0, 
      "hash": "0xf3e1aebc0e16ef37726e9de830e9bf07b277569a5c1ac7dc56629f584d08c597", 
      "miner": "0x8cfb846942e9103550051d703d746dc3b8101822", 
      "nonce": "0xca0a929c499cef95", 
      "timest": "Thu, 26 Jul 2018 01:42:40 GMT", 
      "totaldifficulty": 77397208677506629
    }, 
    {
      "blockNum": 161923, 
      "difficulty": 993086399516, 
      "extra_data": "pfd", 
      "gasUsed": 0, 
      "hash": "0xb1fd945872813db4e55d0fc34399df742c20b300a2cddc1629bfc0ea93a835d0", 
      "miner": "0x8d8fb1033310cd709182cc9181be8b567eee09a7", 
      "nonce": "0x94c8e2c6288b00d7", 
      "timest": "Thu, 26 Jul 2018 01:41:15 GMT", 
      "totaldifficulty": 77396216560918049
    }
    ]
## Get Mining Rewards for a Wallet
You can use this to request the information for the last X block.

Usage:

  >> curl http://wtcexplorer.io/api/miningRewards/{{wallet}}
  
Sample Output:

    [
    {
    "blockNum": 140413, 
    "difficulty": 966090015162, 
    "extra_data": "salvyCPU", 
    "gasUsed": 0, 
    "hash": "0x9ed56d198a4c757e17caab58fc7b1d4f7331c08aef70a26215e173b08e292ecc", 
    "miner": "0x197b391d4a7b4306f709177da18ed12a0ac0eaa3", 
    "nonce": "0x65f3e6f7616ad970", 
    "timest": "Tue, 10 Jul 2018 01:19:19 GMT", 
    "totaldifficulty": 56199573890653109
    }, 
    {
      "blockNum": 155271, 
      "difficulty": 945341666027, 
      "extra_data": "salvyGPU", 
      "gasUsed": 0, 
      "hash": "0x3e00c72f4b546113c15db7ac5942c5264f347e55f42f7bada2e1850e82171bf0", 
      "miner": "0x197b391d4a7b4306f709177da18ed12a0ac0eaa3", 
      "nonce": "0x2db6b1d14ae86f96", 
      "timest": "Sat, 21 Jul 2018 03:06:15 GMT", 
      "totaldifficulty": 70787460153164773
    }
    ]
## Get Mining Rewards for Extra data
You can use this to request the information for the last X block.

Usage:

  >> curl http://wtcexplorer.io/api/miningRewards/extra/{{extraData}}
  
Sample Output:

    [
    {
    "blockNum": 68073, 
    "difficulty": 340.16, 
    "extra_data": "salvyCPU", 
    "gasUsed": 0, 
    "hash": "0xd315e94ed4a8c3da48f9a1f769330061dbeb26bc89d0c90f76956e37e8216938", 
    "miner": "0x197b391d4a7b4306f709177da18ed12a0ac0eaa3", 
    "nonce": "0x4cf0a70de8144836", 
    "timest": "Thu, 17 May 2018 10:01:00 GMT", 
    "totaldifficulty": 10257290002596135
    }, 
    {
      "blockNum": 66622, 
      "difficulty": 347.86, 
      "extra_data": "salvyCPU", 
      "gasUsed": 0, 
      "hash": "0xd385e59e83172aa7a142cf247454728edacba18062813eeb16eb19b9cb8f31c6", 
      "miner": "0x197b391d4a7b4306f709177da18ed12a0ac0eaa3", 
      "nonce": "0x3f43e4c4bb71daab", 
      "timest": "Wed, 16 May 2018 08:00:18 GMT", 
      "totaldifficulty": 9756432852558335
    }
    ]