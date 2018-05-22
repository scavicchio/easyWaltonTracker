import pymysql.cursors
import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse
import ctypes   

#GLOBAL VARIABLES
versionStr = "v1.1"
defaultWalletPath = "C:/Program Files/WTC/"
defaultWIN = ""
defaultLINUX = ""

#Configure MySQL
conn = pymysql.connect(host='waltonchain.ci9smifyvaqf.us-east-2.rds.amazonaws.com',
                        port = 3306,
                        user='salvy',
                        password='',
                        db='BlockChain',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# try to grab from a known Default Linux block
def getDefaultLinux():
    blockString = str(1)
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec web3.toAscii(eth.getBlock("+blockString+").extraData)", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    default = stdout.decode('utf-8')
    return default

# try to grab from a known Default Windows block
def getDefaultWindows():
    blockString = str(1510)
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec web3.toAscii(eth.getBlock("+blockString+").extraData)", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    default = stdout.decode('utf-8')
    return default

#Grabbing data from the blockchain
def getCurrentBlock():
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.blockNumber", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return int(stdout.decode("utf-8").strip())

# Getting all the data from a block
def getAllBlockData(blockNum):
  blockString = str(blockNum)
  p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+")", shell=True, stdout=subprocess.PIPE)
  p.wait()
  data = p.communicate()[0]
  return data

#adding data to the SQL database in the BlockChain table
def insertToDatabase(blockNum,):
    cursor = conn.cursor()
    # needs to be order: block, miner, extra, difficulty, tiemstamp
    query = 'INSERT INTO BlockChain VALUES(%s, %s, %s, %s, %s)'
    cursor.execute(query, (getAllBlockData(blockNum)))
    conn.commit()
    cursor.close()
    return

def getLatestBlockFromDB():
    cursor = conn.cursor()
    query = 'SELECT blockNum FROM BlockChain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    print(latestBlock)
    return latestBlock;

def runUntilCurrent(workingBlock,currentBlock):
    print("running until current, working block: ", workingBlock)
    while (workingBlock < currentBlock):
        insertToDatabase(workingBlock)
        workingBlock = workingBlock+1
        
    return
    
#test to print the get all data
def main():
    workingBlock = 0;

    #get defaults
    defaultWIN = getDefaultWindows().rstrip().strip('"')
    defaultLINUX = getDefaultLinux().rstrip().strip('"')
    print('Set Defaults...')
    print('windows default: ', defaultWIN)
    print('linux default: ', defaultLINUX)
    
    placeholder = getLatestBlockFromDB(); # last one that we got data for in DB
    LatestBlock = placeholder["blockNum"]
    print(LatestBlock)

    workingBlock = LatestBlock+1; # the one we are working on right now
    currentBlock = getCurrentBlock(); # the current latest block being mined
    delay = 10; # how long to wait before checking if up to date

    runUntilCurrent(workingBlock,currentBlock);
    
    #check if we are up to date and get the latest block from the database
    while True:
        currentBlock = getCurrentBlock()
        workingBlock = getLatestBlockFromDB()["blockNum"]+1;
        if (workingBlock<currentBlock):
            runUntilCurrent(workingBlock,currentBlock)
        time.sleep(delay)

    return;

if __name__ == '__main__':
    main()
