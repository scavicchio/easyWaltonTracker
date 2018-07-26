# easyWaltonTracker
# wtcexplorer.io

Server to track and give notifications for block mining rigs.

Website address: http://wtcexplorer.io

If you would like to collaborate on this project or connect it to an existing project you maintain send me an email at salvy@easywaltonminer.com

If you need help or see an issue on the site, please email support@easywaltonminer.com

*Recent Updates*
- Started implementing API
- Updated database to include transaction data
- Added chartsjs!
- Added statistics pages
- Moved to our new domain!
- Miner page now shows rig counts by last week and month
- Now showing latest update time on miner page
- Site now optimized for mobile phones (tested on iPhone 8)
- DB updater now uses connect info from offline text file
- Changed time to users local time using moment.js
- Switched table layout on miner.html

# API 
We have started working on a free API for developers to grab waltonchain blockchain data. The documentation is below.

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
