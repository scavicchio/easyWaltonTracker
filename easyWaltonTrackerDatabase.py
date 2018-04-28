#import pymysql.cursors
import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse
import ctypes   
import csv

#GLOBAL VARIABLES
versionStr = "v1.1"
defaultWalletPath = "C:/Program Files/WTC/"

#Configure MySQL
conn = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        db='waltonchain',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

#Grabbing data from the blockchain
def getCurrentBlock():
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.blockNumber", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return int(stdout.decode("utf-8").strip())

def getBlockExtraData(blockNum):
    blockString = str(blockNum)
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec web3.toAscii(eth.getBlock("+blockString+").extraData)", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return stdout.decode("utf-8").strip()

def getBlockMiner(blockNum):
        blockString = str(blockNum)
        p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").miner", shell=True, stdout=subprocess.PIPE)
        p.wait()
        stdout = p.communicate()[0]
        return stdout.decode("utf-8").strip()

def getBlockDifficulty(blockNum):
        blockString = str(blockNum)
        p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").difficulty", shell=True, stdout=subprocess.PIPE)
        p.wait()
        stdout = p.communicate()[0]
        return stdout.decode("utf-8").strip()

def getBlockTimeStamp(blockNum):
        blockString = str(blockNum)
        p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+").timestamp", shell=True, stdout=subprocess.PIPE)
        p.wait()
        stdout = p.communicate()[0]
        return stdout.decode("utf-8").strip()

def getAllBlockData(blockNum):
    extraData = getBlockExtraData(blockNum)
    miner = getBlockMiner(blockNum)
    difficulty = getBlockDifficulty(blockNum)
    timestamp = getBlockTimeStamp(blockNum)

    return (extraData,miner,difficulty,timestamp)

#adding data to the SQL database in the BlockChain table
def insertToDatabase(blockNum,miner,extraData,difficulty,timest):
    cursor = conn.cursor()
    query = 'INSERT INTO BlockChain VALUES(%s, %s, %s, %s, %s)'
    cursor.execute(query, (blockNum,miner,extraData,difficulty,timest))
    conn.commit()
    cursor.close()
    return

def getLatestBlockFromDB():
    cursor = conn.cursor()
    query = 'SELECT blockNum FROM BlockChain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    return latestBlock;

def checkForInitialSetup():
    cursor = conn.cursor()
    query = 'SELECT COUNT(blockNum) FROM BlockChain'
    cursor.execute(query)
    data = cursor.fetchone()
    if (query == 0): #must get all database data
        return True;
    
    return False;

# won't really work since the current block will advance while we run this setup, but we can fix that later when the main updates. 
def runInitialSetup():
    block = 1 #start at the top!
    currentBlock = getCurrentBlock()

    while (block <= currentBlock):
        insertToDatabase(block,getAllBlockData(block))
        block = block +1;

    return


#test to print the get all data
def main():
    
    #check initial setup (basically if this is the first time this program is run it needs to create the database)
    if checkForInitialSetup():
        runInitialSetup();

    int LatestBlock = getLatestBlockFromDB(); # last one that we got data for in DB
    int workingBlock = LatestBlock+1; # the one we are working on right now
    int currentBlock = getCurrentBlock(); # the current latest block being mined
    int delay = 60; # how long to wait before checking if up to date

    #check if we are up to date and get the latest block from the database
    while True:
        if (workingBlock<currentBlock):
            insertToDatabase(workingBlock,getAllBlockData(workingBlock))
            workingBlock=workingBlock+1;
        time.sleep(delay)

    return;

if __name__ == '__main__':
    main()