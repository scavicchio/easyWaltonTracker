import pymysql.cursors

# Lets make some global vars
with open("clientinfo.txt", "r") as ins:
  data = []
  for line in ins:
    data.append(line)

  host = data[0].strip()
  port = data[1].strip()
  dbUser = data[2].strip()
  dbPassword = data[3].strip()
  database = data[4].strip()
  username = data[5].strip()
  password = data[6].strip()
  difficultyHashMagnitude = float(data[7].strip())

def connect():
	conn = pymysql.connect(host=host,
                        port = int(port),
                        user=dbUser,
                        password=dbPassword,
                        db=database,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
	return conn

conn = connect()

### MAIN PAGES ###
### MAIN PAGES ###
### MAIN PAGES ###
### MAIN PAGES ###
### MAIN PAGES ###

# gets the most recent block that the DB has data for  
def getLatestBlockFromDB(conn):    
    cursor = conn.cursor()
    query = 'SELECT blockNum FROM blockchain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    return latestBlock["blockNum"];

def getLastUpdateTime(conn):    
    cursor = conn.cursor()
    query = 'SELECT timest FROM blockchain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    return latestBlock["timest"];

# gets all data for a specific etherbase
def getDataForMiner(conn, etherbase):
    cursor = conn.cursor()
    query = 'SELECT * FROM blockchain WHERE miner = %s'
    cursor.execute(query, (etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

def getDataForMinerPaginated(conn, etherbase, perPage,page):
    offset = (page-1)*perPage
    cursor = conn.cursor()
    query = 'SELECT * FROM blockchain WHERE miner = %s ORDER BY blockNum DESC LIMIT %s OFFSET %s'
    cursor.execute(query, (etherbase,perPage, offset))
    data = cursor.fetchall()
    cursor.close()

    for x in data:
      x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))

    return data


# gets the total blocks a miner has solved
def getRewardCount(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM blockchain WHERE miner = %s'
    cursor.execute(query, (etherbase))
    data = cursor.fetchone()
    cursor.close()
    return data["COUNT(*)"]

# returns the number of rewards for each unique extraData as a pair.
def getRewardCountByExtra(conn,etherbase):
    cursor = conn.cursor()

    query = 'SELECT extra_data, \
           COUNT(blockNum) as theCount, \
           SUM(case when (timest >= DATE(NOW()) - INTERVAL 7 DAY) then 1 else 0 end) as lastWeek, \
           SUM(case when (timest >= DATE(NOW()) - INTERVAL 1 MONTH) then 1 else 0 end) as lastMonth \
      		FROM blockchain \
     		WHERE miner = %s \
  			GROUP BY extra_data ORDER BY lastWeek DESC'

    cursor.execute(query,(etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

def getLast7Days(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT extra_data, COUNT(blockNum) AS theCount FROM blockchain WHERE miner = %s AND timest >= DATE(NOW()) - INTERVAL 7 DAY GROUP BY extra_data'
    cursor.execute(query,(etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

def getLastMonth(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT extra_data, COUNT(blockNum) AS theCount FROM blockchain WHERE miner = %s AND timest >= DATE(NOW()) - INTERVAL 1 MONTH GROUP BY extra_data'
    cursor.execute(query,(etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

# reurns all info from latest X rewards for a given address
def getLatestNRewards(conn,etherbase,index):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE miner = %s ORDER BY blockNum DESC LIMIT %s'
  cursor.execute(query, (etherbase,index))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
  cursor.close()
  return data

def getLatestAllRewards(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE miner = %s ORDER BY blockNum DESC'
  cursor.execute(query, (etherbase))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))

  cursor.close()
  return data

#gets all blocks, timest and extra for a JS graph for later
def getGraphData(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT blockNum, extra_data, timest FROM blockchain WHERE miner = %s ORDER BY timest ASC'
  cursor.execute(query, (etherbase))
  data = cursor.fetchall()
  cursor.close()
  return data

def getDifficultyGraphData(conn):
  cursor = conn.cursor()
  query = 'SELECT blockNum, difficulty, timest FROM blockchain WHERE ((blockNum-1) % 100 = 0) ORDER BY blockNum ASC'
  cursor.execute(query)
  data = cursor.fetchall()
  cursor.close()
  return data

#gets most recent N blocks, data, and time for homepage
def getLatestNBlocks(conn,index):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain ORDER BY timest DESC LIMIT %s'
  cursor.execute(query, (index))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
  cursor.close()
  return data

def getLatestNBlocksOffset(conn,perPage,page):
  offset = (page-1)*perPage
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain ORDER BY timest DESC LIMIT %s OFFSET %s'
  cursor.execute(query, (perPage,offset))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
  cursor.close()
  return data

#adds a persons email to the alert table
def addEmailAlert(conn,etherbase,email,extra):
        cursor = conn.cursor()
        query = 'INSERT INTO `emailList`(`miner`, `email`, `extra_data`, `confirmed`) VALUES (%s,%s,%s,False)'
        try:
                cursor.execute(query, (etherbase, email, extra))
        except pymysql.Error as e:
                return e
        conn.commit()
        cursor.close()
        return "Sucsess"

def removeEmailAlert(conn,etherbase,email,extra):
        cursor = conn.cursor()
        query = 'DELETE FROM emailList WHERE (miner = %s AND email = %s AND extra_data = %s)'
        try:
                cursor.execute(query, (etherbase, email,extra))
        except pymysql.Error as e:
                cursor.close()
                return e
        conn.commit()
        cursor.close()
        return "Sucsess"

def foundExtra(conn,extra):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM blockchain WHERE extra_data = %s LIMIT 1'
  cursor.execute(query,(extra))
  data = cursor.fetchone()["COUNT(*)"]
  cursor.close()

  if (data == 0):
    return False

  return True

def getDataForExtra(conn,extra):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE extra_data = %s ORDER BY blockNum DESC'
  cursor.execute(query,(extra))
  data = cursor.fetchall()
  cursor.close()

  for x in data:
      x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))


  return data

def getDataForExtraLimited(conn,extra,limit):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE extra_data = %s ORDER BY blockNum DESC LIMIT %s'
  cursor.execute(query,(extra,limit))
  data = cursor.fetchall()
  cursor.close()

  for x in data:
      x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))


  return data

def getTotalByExtra(conn,extra):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM blockchain WHERE extra_data = %s'
  cursor.execute(query,(extra))
  data = cursor.fetchone()
  cursor.close()

  return data["COUNT(*)"]

def getExtraStats(conn,extra):
  cursor = conn.cursor()

  query = 'SELECT  \
           COUNT(blockNum) as theCount, \
           SUM(case when (timest >= DATE(NOW()) - INTERVAL 7 DAY) then 1 else 0 end) as lastWeek, \
           SUM(case when (timest >= DATE(NOW()) - INTERVAL 1 MONTH) then 1 else 0 end) as lastMonth \
          FROM blockchain \
          WHERE extra_data = %s \
           ORDER BY lastWeek DESC'

  cursor.execute(query,(extra))
  data = cursor.fetchall()
  cursor.close()

  return data

def getTopMiners(conn, limit):
	cursor = conn.cursor()
	query = 'SELECT miner, Count(*) AS total FROM blockchain GROUP BY miner ORDER BY total DESC LIMIT %s'
	cursor.execute(query,limit)
	data = cursor.fetchall()
	cursor.close()
	return data

def getTopRigs(conn, limit):
	cursor = conn.cursor()
	query = 'SELECT extra_data, Count(*) AS total FROM blockchain GROUP BY extra_data ORDER BY total DESC LIMIT %s'
	cursor.execute(query,limit)
	data = cursor.fetchall()
	cursor.close()
	return data

def getTopMinersLatest(conn, limit, oldest):
  cursor = conn.cursor()
  query = 'SELECT miner, Count(*) AS total FROM blockchain WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY) GROUP BY miner ORDER BY total DESC LIMIT %s'
  cursor.execute(query,(oldest,limit))
  data = cursor.fetchall()
  cursor.close()
  return data

def getTopRigsLatest(conn, limit,oldest):
  cursor = conn.cursor()
  query = 'SELECT extra_data, Count(*) AS total FROM blockchain WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY) GROUP BY extra_data ORDER BY total DESC LIMIT %s'
  cursor.execute(query,(oldest,limit))
  data = cursor.fetchall()
  cursor.close()
  return data

def getMaxTransactions(conn): 
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS count, DATE(timest) AS day FROM transaction GROUP BY day ORDER BY count DESC LIMIT 1'
  cursor.execute(query)
  data = cursor.fetchone()
  cursor.close()

  return data

def getMaxDifficulty(conn):
  cursor = conn.cursor()
  query = 'SELECT difficulty, blockNum FROM blockchain ORDER BY difficulty DESC LIMIT 1'
  cursor.execute(query)
  data = cursor.fetchone()
  cursor.close()

  return data

def getTotalTransactions(conn):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS total FROM transaction'
  cursor.execute(query)
  data = cursor.fetchone()
  cursor.close()

  return data

def getAverageDifficulty(conn):
  cursor = conn.cursor()
  query = 'SELECT AVG(difficulty) AS average FROM blockchain'
  cursor.execute(query)
  data = cursor.fetchone()
  cursor.close()

  return data

def getActiveWallets(conn):
  cursor = conn.cursor()
  query =  'SELECT COUNT(*) AS total \
            FROM (SELECT DISTINCT(miner) FROM blockchain UNION \
            (SELECT DISTINCT(sender) FROM transaction) UNION \
             (SELECT DISTINCT(reciever) FROM transaction)) AS a'
  cursor.execute(query)
  data = cursor.fetchone()
  cursor.close()

  return data

### FOR 90 DAYS ###

def getMaxTransactions90(conn,days): 
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS count, DATE(timest) AS day FROM transaction WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY) GROUP BY day ORDER BY count DESC LIMIT 1'
  cursor.execute(query,(days))
  data = cursor.fetchone()
  cursor.close()

  return data

def getMaxDifficulty90(conn,days):
  cursor = conn.cursor()
  query = 'SELECT difficulty, blockNum FROM blockchain WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY) ORDER BY difficulty DESC LIMIT 1'
  cursor.execute(query,(days))
  data = cursor.fetchone()
  cursor.close()

  return data

def getTotalTransactions90(conn,days):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS total FROM transaction WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY)'
  cursor.execute(query,(days))
  data = cursor.fetchone()
  cursor.close()

  return data

def getAverageDifficulty90(conn,days):
  cursor = conn.cursor()
  query = 'SELECT AVG(difficulty) AS average FROM blockchain WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY)'
  cursor.execute(query,(days))
  data = cursor.fetchone()
  cursor.close()

  return data

def getActiveWallets90(conn,days):
  cursor = conn.cursor()
  query =  'SELECT COUNT(*) AS total \
            FROM (SELECT DISTINCT(miner) FROM blockchain WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY) UNION \
            (SELECT DISTINCT(sender) FROM transaction WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY)) UNION \
             (SELECT DISTINCT(reciever) FROM transaction WHERE (timest >= DATE(NOW()) - INTERVAL %s DAY))) AS a'
  cursor.execute(query,(days,days,days))
  data = cursor.fetchone()
  cursor.close()

  return data

def getTransactionFrequencyGraph(conn):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS count, DATE(timest) AS day FROM transaction GROUP BY day'
  cursor.execute(query)
  data = cursor.fetchall()
  cursor.close()
  return data

def getTransactionListBlock(conn,block):
  cursor = conn.cursor()
  query = 'SELECT hash FROM transaction WHERE blockNum = %s'
  cursor.execute(query, (block))
  data = cursor.fetchall()
  cursor.close()
  return data

### API ###
### API ###
### API ###
### API ###
### API ###

def getBlock(conn,blockNum): 
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE blockNum = %s'
  cursor.execute(query,(blockNum))
  data = cursor.fetchone()
  cursor.close()
  return data

def getLatestNBlocksAPI(conn,index):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain ORDER BY blockNum DESC LIMIT %s'
  cursor.execute(query, (index))
  data = cursor.fetchall()
  cursor.close()
  return data

def getTransactionAPI(conn,hash):
  cursor = conn.cursor()
  query = 'SELECT * FROM transaction WHERE hash = %s'
  cursor.execute(query, (hash))
  data = cursor.fetchone()
  cursor.close()
  return data

def getTransactionBlockAPI(conn,hash):
  cursor = conn.cursor()
  query = 'SELECT * FROM transaction WHERE blockNum = %s'
  cursor.execute(query, (hash))
  data = cursor.fetchall()
  cursor.close()
  return data

# gets all data for a specific etherbase
def getDataForMiner(conn, etherbase):
    cursor = conn.cursor()
    query = 'SELECT * FROM blockchain WHERE miner = %s'
    cursor.execute(query, (etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

def getDataForExtraAPI(conn,extra):
  cursor = conn.cursor()
  query = 'SELECT * FROM blockchain WHERE extra_data = %s ORDER BY blockNum DESC'
  cursor.execute(query,(extra))
  data = cursor.fetchall()
  cursor.close()
  return data

# gets the most recent block that the DB has data for  
def getLatestBlockFromDB(conn):    
    cursor = conn.cursor()
    query = 'SELECT blockNum FROM blockchain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    return latestBlock["blockNum"];

## EMAIL SERVICE ##

def getEmailsForAlert(conn,blockNum):
    cursor = conn.cursor()
    return data

def setEmailConfirmation(conn,email,confirm):
  cursor = conn.cursor()
  query = 'UPDATE emailList SET confirmed = %s WHERE email = %s'
  cursor.execute(query,(confirm,ID))
  conn.commit()
  cursor.close()
  return "Sucsess"

def isMasternode(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM transaction WHERE value = 5000 AND reciever = %s'
  cursor.execute(query,(etherbase))
  data = cursor.fetchone()['COUNT(*)']
  #print("IS MASTERNODE")
  #print(data)
  cursor.close()
  if data >= 1:
    return True
  return False

def isGuardian(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM GMN_ERC WHERE etherbase IN (SELECT wtctGMN.from FROM wtctGMN WHERE  value =  %s)'
  cursor.execute(query,(etherbase))
  data = cursor.fetchone()['COUNT(*)']
  #print("IS GUARDIAN")
  #print(data)
  cursor.close()
  if data >= 1:
    return True
  return False
  