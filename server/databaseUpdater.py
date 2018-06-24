# coding=utf-8
import pymysql.cursors
import ctypes
import os.path
import time
import datetime
import sys
import subprocess
import argparse
import ctypes   
import ast
import json
import base64

#GLOBAL VARIABLES
versionStr = "v1.1"
defaultWalletPath = "C:/Program Files/WTC/"
defaultLINUX = "d783010700846765746887676f312e392e32856c696e7578"
defaultWIN = "d883010700846765746886676f312e31308777696e646f7773"


#Configure MySQL
def connect(host,port,username,password,database):
	conn = pymysql.connect(host=host,
                        port = int(port),
                        user=username,
                        password=password,
                        db=database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
	return conn

# try to grab from a known Default Linux block
def getDefaultLinux():
	data = getBlockData(1)['extraData'][2:]
	#print(type(data))
	return data

def getDefaultWindows():
	data = getBlockData(1510)['extraData'][2:]
	#print(type(data))
	return data

# try to grab from a known Default Windows block
#def getDefaultWindows():
#    blockString = str(1510)
#    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec web3.toAscii(eth.getBlock("+blockString+").extraData)", shell=True, stdout=subprocess.PIPE)
#    p.wait()
#    stdout = p.communicate()[0]
#    default = stdout.decode('utf-8')
#    return default

    
#Grabbing data from the blockchain
def getCurrentBlock():
    p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.blockNumber", shell=True, stdout=subprocess.PIPE)
    p.wait()
    stdout = p.communicate()[0]
    return int(stdout.decode("utf-8").strip())

def getRawBlockData(blockNum):
        blockString = str(blockNum)
        p = subprocess.Popen("\""+defaultWalletPath+"walton.exe\" attach http://127.0.0.1:8545 --exec eth.getBlock("+blockString+")", shell=True, stdout=subprocess.PIPE)
        #p.wait()
        data = p.communicate()[0].decode()
        return data

def cleanBlockData(rawData):
	stripped = rawData.strip()
	theList = stripped.split()
	theList = theList[1:-1]
	stripIt = ([x.strip().strip('"').strip(':').strip(',').strip('"') for x in theList])
	theReturn = dict(zip(stripIt[::2], stripIt[1::2]))
	return theReturn

def getBlockData(blockNum):
	data = getRawBlockData(blockNum)
	theList = cleanBlockData(data)
	return theList

def databaseData(blockNum):
	data = getBlockData(blockNum)

	if (data["extraData"][2:] == defaultLINUX):
		#print('default LIN found')
		data["extraData"][2:] = "Linux"
	elif (data["extraData"][2:] == defaultWIN):
		#print('default WIN found')
		data["extraData"][2:] = "Windows"
	else:
		try:
			extra_data = bytearray.fromhex(extra_data).decode().strip()
		except ValueError:
			print("Found error decoding extra data, will insert original.")

	data["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timest)))

	return data

# all string
#def printDictDataTypes(dictionary):
	types1 = [type(k) for k in dictionary.keys()]
	print(types1)

#adding data to the SQL database in the BlockChain table
def insertToDatabase(blockNum):
	data = databaseData(blockNum)
	
	cursor = conn.cursor()
	# needs to be order: block, miner, extra, difficulty, tiemstamp, gas
	query = 'INSERT INTO BlockChain VALUES(%s, %s, %s, %s, %s, %s)'
	cursor.execute(query, (blockNum, miner, extra, difficulty, timest, gas))
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
    	print(workingBlock)
    	insertToDatabase(workingBlock)
    	workingBlock = workingBlock+1
        
    return

# so I can upload to github and not worry about hacking
with open("Ignore/databaseUpdaterInfo.txt", "r") as ins:
	data = []
	for line in ins:
		data.append(line)

	host = data[0].strip()
	port = data[1].strip()
	username = data[2].strip()
	password = data[3].strip()
	database = data[4].strip()

	print(host,port,username,password,database)

conn = connect(host,port,username,password,database)

#test to print the get all data
def main():
    

    workingBlock = 0;
    #problem block was 17743 fixed by removing p.wait() after communicate
    # seems like data is still OK.....
    #print(getRawBlockData(17743))
    LatestBlock = 0;
    #get defaults
    defaultWIN = getDefaultWindows().rstrip().strip('"')
    defaultLINUX = getDefaultLinux().rstrip().strip('"')
    print('Set Defaults...')
    print('windows default: ', defaultWIN)
    print('linux default: ', defaultLINUX)

    placeholder = getLatestBlockFromDB(); # last one that we got data for in DB
    if placeholder is None:
    	print('Initial Setup')
    else:
    	LatestBlock = placeholder["blockNum"]

    print(LatestBlock)

    workingBlock = LatestBlock+1; # the one we are working on right now
    currentBlock = getCurrentBlock(); # the current latest block being mined
    delay = 10; # how long to wait before checking if up to date

    runUntilCurrent(workingBlock,currentBlock);
    
    #check if we are up to date and get the latest block from the database
    while True:
    	try:
    		print(currentBlock)
    		currentBlock = getCurrentBlock()
    		workingBlock = getLatestBlockFromDB()["blockNum"]+1;
    		if (workingBlock<currentBlock):
    			runUntilCurrent(workingBlock,currentBlock)
    	except:
    		print('Error Updating DB: Will try again in 10s.')
    		
    	time.sleep(delay)
    return;

if __name__ == '__main__':
    main()
