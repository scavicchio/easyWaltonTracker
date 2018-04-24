import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse
import ctypes   

## Global variables
versionStr = "v1.0"
defaultWalletPath = "C:/Program Files/WTC/"

''' Starts walton.exe to get started '''
'''
def startWalton():
	os.chdir(defaultWalletPath)
	if not os.path.isdir(defaultWalletPath+"node1/"):
		p = subprocess.Popen("walton.exe --datadir node1 init genesis.json")
	p = subprocess.Popen("walton.exe --identity \"development\" --rpc --rpcaddr 127.0.0.1 "+
			  "--rpccorsdomain \"*\"  --cache 2048 --datadir \"node1\" --port \"30303\" "+
			  "--rpcapi \"admin,personal,db,eth,net,web3,miner\" "+
			  " --networkid 999 --rpcport 8545 console")
	p.wait()
	return
'''

''' Sets the current window title to the string specified. '''
def setTitle(title):
	ctypes.windll.kernel32.SetConsoleTitleW(title)

def getCurrentBlock():
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.blockNumber", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return stdout.decode("utf-8").strip()

def getBlockData(blockNum):
    blockString = str(blockNum)
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").extraData", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return stdout.decode("utf-8").strip()

def logData(blockNum):
    blockExtraData = getBlockData(blockNum);
    blockString = str(blockNum)
    dataLog = open("blockDataLog.csv","a");
    dataLog.write(blockString+","+blockExtraData+"\n");
    dataLog.close();
    return

## CONFIG MENU FUNCTIONS

''' Config menu option to tell the menu loop to break. '''
def menu_exit(config):
	return config, True

def main(argv):
	## General variables
    delay = 60
    blockNum = 36998;
    currentBlock = 0;
    every100Blocks = 0;
    ctypes.windll.user32.MessageBoxW(0, "2", "Your title", 1)
    currentBlock = getCurrentBlock();
    currentBlockInt = int(currentBlock)

    while True:
        
        if (int(currentBlock) > blockNum):
            while (blockNum < currentBlockInt):
                logData(blockNum);
                blockNum=blockNum+1;
                every100Blocks=every100Blocks+1;
                
        time.sleep(delay)
        
    return
			
if __name__ == '__main__':
	sys.exit(main(sys.argv))
