import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse
import ctypes   
import csv
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

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

def getBlockExtraData(blockNum):
    blockString = str(blockNum)
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").extraData", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return stdout.decode("utf-8").strip()

def getBlockMiner(blockNum):
        blockString = str(blockNum)
        p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").miner", shell=True, stdout=subprocess.PIPE)
        p.wait()
        stdout = p.communicate()[0]
        return stdout.decode("utf-8").strip()

def logData(blockNum):
    blockExtraData = getBlockExtraData(blockNum);
    blockMiner = getBlockMiner(blockNum);
    blockString = str(blockNum)
    dataLog = open("blockDataLog.csv","a");
    dataLog.write(blockString+","+blockExtraData+","+blockMiner+"\n");
    dataLog.close();
    return

def getLineOfBlock(block):
        file = open("blockDataLog.csv","r")
        csv_f = csv.reader(file)
        rowCount = 0;
        for row in csv_f:
                blockR = row[0]
                if (blockR == str(block)):
                        return rowCount
                rowCount = rowCount + 1;
        print("block not found")
        return
        
def getMinerByBlock(block):
        row = getLineOfBlock(block);
        line = open("blockDataLog.csv","r").readlines()[row]
        block, extra, miner = line.split(',',2)
        return miner

def getExtraDataByBlock(block):
        row = getLineOfBlock(block);
        line = open("blockDataLog.csv","r").readlines()[row]
        block, extra, miner = line.split(',',2)
        return extra
        
def getMinedBlocksByAddress(etherbase):
        theReturn = [];

        file = open("blockDataLog.csv","r")
        csv_f = csv.reader(file)

        for row in csv_f:
                block = row[0]
                extra = row[1]
                miner = row[2]
                if (miner == etherbase):
                        blockInt = int(block)
                        theReturn.append(blockInt)
                        
        return theReturn
	
## CONFIG MENU FUNCTIONS

''' Config menu option to tell the menu loop to break. '''
def menu_exit(config):
	return config, True

def main(argv):
        ## General variables
        delay = 60
        etherbase = "0x197b391d4a7b4306f709177da18ed12a0ac0eaa3"
        ## blockNum is the working block - reps the last recorded data
        workingBlock = 0;
        ## actually getting the block num .... gotta test the printout later to grab just the block.
        if os.path.isfile("blockDataLog.csv"):
                print("opening existing database")
                last_line = open("blockDataLog.csv", "r").readlines()[-1]
                #ctypes.windll.user32.MessageBoxW(0, last_line, "Your title", 1)
                firstLast, secondLast = last_line.split(',', 1)
                #ctypes.windll.user32.MessageBoxW(0, firstLast, "Your title", 1)
                #ctypes.windll.user32.MessageBoxW(0, secondLast, "Your title", 1)
                ## PUT STUFF HERE TO GET JUST THE BLOCK
                workingBlock = workingBlock + (int(firstLast)+1);
                print("latest downloaded block: ")
                print(workingBlock)
        else:
                print("No database detected, must generate")
        #ctypes.windll.user32.MessageBoxW(0, "Working Block: ", "Your title", 1)
        #ctypes.windll.user32.MessageBoxW(0, str(workingBlock), "Your title", 1)
        currentBlock = getCurrentBlock();
        currentBlockInt = int(currentBlock)
        
        while True:
                currentBlockInt = int(currentBlock)
                if (int(currentBlock) > workingBlock):
                        while (workingBlock < currentBlockInt):
                                logData(workingBlock);
                                if(getMinerByBlock(workingBlock) == etherbase):
                                        print("I GOT A BLOCK")
                                        print(workingBlock)
                                        extraData = getExtraDataByBlock(workingBlock)
                                        print("Extra data for mined block: ")
                                        print(extraData)
                                workingBlock=workingBlock+1;
                

            #    miner = getMinerByBlock(37016)
             #   allBlocks = getMinedBlocksByAddress(etherbase)
              #  ctypes.windll.user32.MessageBoxW(0, miner, "Your title", 1)
                
                time.sleep(delay)

                
        return;
if __name__ == '__main__':
	sys.exit(main(sys.argv))
