# SALVY CAVICCHIO
# EASY WALTON TRACKER DATABASE SIDE
# 
#
#
#IT IS WEDNESDAY MY DUDES
#
#
#


#import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, Response, jsonify
from flask_paginate import Pagination, get_page_args
from flask_bootstrap import Bootstrap
import pymysql.cursors
import re
import smtplib
from momentjs import momentjs
import csv
import math
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#Initialize the app from Flask
app = Flask(__name__)
app.jinja_env.globals['momentjs'] = momentjs
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3000 per hour"]
)

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

########## ########################### ##############   
########## ########################### ##############   
########## ########################### ##############   
########## functions for DB operations ##############   
########## ########################### ##############   
########## ########################### ##############   
########## ########################### ##############   

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
        #check for bad inputs
        if not goodEmail(email):
          return "Please Enter a Valid Email Address"
        if not goodEtherbase(etherbase):
          return "Please Enter a Valid Wallet Address"

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
        #check for bad inputs
        if not goodEmail(email):
          return "Please Enter a Valid Email Address"
        if not goodEtherbase(etherbase):
          return "Please Enter a Valid Wallet Address"

        cursor = conn.cursor()
        query = 'DELETE FROM emailList WHERE (miner = %s AND email = %s AND extra_data = %s)'
        try:
                cursor.execute(query, (etherbase, email,extra))
        except pymysql.Error as e:
                return e
        conn.commit()
        cursor.close()
        return "Sucsess"
        
########## ############################## ##############   
########## ############################## ##############   
########## ############################## ##############   
########## extra functions for repitition ##############   
########## ############################## ##############   
########## ############################## ##############   
########## ############################## ############## 

# checks that email is in correct format (not done)
def goodEmail(email):
  if re.match(r"[^@]+@[^@]+\.[^@]+", email):
    return True

  return False

#checks that etherbase is the right length
def goodEtherbase(etherbase):
  if len(etherbase) == 42:
    return True

  return False

def sendUnsubstribeConfirmation(etherbase,email):
  fromaddr = username
  toaddrs  = email
  msg = 'You have sucesssfully unsubscribed from the EasyWaltonMiner email alert system. \n \n' \
  'We are sorry to see you go! You will no longer recieve email alerts for your wallet: ' + etherbase + '.\n \n' + \
  'If you had an issue with this service, please respond to this email and let us know so that we can address it.'
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddrs, msg)
  server.quit()

  return

def sendSignupConfirmation(etherbase,email,extra):
  fromaddr = username
  toaddrs  = email
  msg = 'You have sucesssfully subscribed to the EasyWaltonMiner email alert system. \n \n' \
  'You will now recieve email alerts for blocks mined to wallet: ' + etherbase + '.\n \n'
  if (extra):
    msg = msg + 'You will recieve alerts only when the extra_data flag of a block matches: ' + extra + '\n \n'
  else:
    msg = msg + 'You will recieve a message for every new block mined to your wallet. \n \n'

  msg = msg + 'If you have any problems with this service, please notify us at this email address. Thanks you!'

  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, toaddrs, msg)
  server.quit()
  return

########## ######################## ##############   
########## ######################## ##############   
########## ######################## ##############   
########## functions for FLASK app  ##############   
########## ######################## ##############   
########## ######################## ##############   
########## ######################## ##############   

#Define route for homepage
@app.route('/')
def homepage(error="None"):
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 5
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    lastUpdate = getLastUpdateTime(conn)
    lastTen = getLatestNBlocksOffset(conn,per_page,page)
    graph = getDifficultyGraphData(conn)

    conn.close()

    for x in graph:
      x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
    #pagination = Pagination(page=page, per_page=per_page, total = int(latestBlock),
    #                       css_framework='bootstrap4')

    if (error != "None"):
      return render_template('home.html',graph=graph,latestBlock=latestBlock,lastTen=lastTen,lastUpdate=lastUpdate,error=error)

    return render_template('home.html',graph=graph,latestBlock=latestBlock,lastUpdate=lastUpdate,lastTen=lastTen)

#about page
#@app.route('/about')
#def about1():
#    return redirect("/#About")

#about page
@app.route('/About')
def about():
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    conn.close()
    return render_template('about.html',latestBlock=latestBlock)

#howto page
@app.route('/HowTo')
def howto2():
    return redirect("/howto")

@app.route('/FAQ')
def faq1():
    return redirect("/#FAQ")

def foundExtra(conn,extra):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) FROM blockchain WHERE extra_data = %s LIMIT 1'
  cursor.execute(query,(extra))
  data = cursor.fetchone()["COUNT(*)"]
  cursor.close()

  if (data == 0):
    return False

  return True

@app.route('/searchExtra',methods=['GET','POST'])
def searchExtra():
        extra = request.form.get('extra')
        conn = connect()

        if foundExtra(conn,extra):
          returnUrl = 'extra/'+extra+''
          return redirect(returnUrl)

        
        latestBlock = getLatestBlockFromDB(conn)
        lastTen = getLatestNBlocks(conn,10)
        lastUpdate = getLastUpdateTime(conn)
        conn.close()
        error = "Extra Data Key Not Found! (This means your computer has not mined a block yet.)"
        return homepage(error)

# for homepage search bar
@app.route('/searchMiner', methods=['GET','POST'])
def searchMiner():
        etherbase = request.form.get('etherbase')

        if goodEtherbase(etherbase):
          returnUrl = 'miner/'+etherbase+''
          return redirect(returnUrl)

        conn = connect()
        latestBlock = getLatestBlockFromDB(conn)
        lastTen = getLatestNBlocks(conn,10)
        lastUpdate = getLastUpdateTime(conn)
        conn.close()
        error = "Please Enter a Valid Wallet Address"
        return homepage(error)


@app.route('/alerts', methods=['GET','POST'])
def alert():
        conn = connect()
        latestBlock = getLatestBlockFromDB(conn)
        conn.close()
        return render_template('alerts.html',latestBlock=latestBlock)

@app.route('/emailSubmit',methods=['GET','POST'])
def emailSubmit():
        conn = connect()
        etherbase = request.form.get('etherbase')
        email = request.form.get('email')
        extra = request.form.get('extra')
        message = addEmailAlert(conn,etherbase,email,extra)
        latestBlock = getLatestBlockFromDB(conn)
        conn.close()

        if message == "Sucsess":
                message = "Sucsess! Please check your email to confirm your signup."

                
                try:
                  sendSignupConfirmation(etherbase,email,extra)
                except error as e:
                  return render_template('alerts.html',latestBlock=latestBlock,error=e)
                return render_template('alerts.html',latestBlock=latestBlock,message=message)
        else:
                return render_template('alerts.html',latestBlock=latestBlock,error=message)
        
        return render_template('alerts.html',latestBlock=latestBlock)

@app.route('/emailRemove',methods=['GET','POST'])
def emailRemove():
        conn = connect()
        etherbase = request.form.get('etherbaseRemove')
        email = request.form.get('emailRemove')
        extra = request.form.get('extraRemove')
        message = removeEmailAlert(conn,etherbase,email,extra)
        latestBlock = getLatestBlockFromDB(conn)
        conn.close()

        if message == "Sucsess":
                try:
                  sendUnsubstribeConfirmation(etherbase,email)
                except error as e:
                  return render_template('alerts.html',latestBlock=latestBlock,error=e)
                message = "Sucsess! Please check your email for removal confirmation."
                return render_template('alerts.html',latestBlock=latestBlock,message=message)
        else:
                return render_template('alerts.html',latestBlock=latestBlock,error=message)
        
        return render_template('alerts.html',latestBlock=latestBlock)
'''
# route for miner data page
@app.route('/miner/<etherbase>',methods=['GET'])
def miner(etherbase):
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 10
    # always connect first 
    conn = connect()

    # get all the data for the template
    latestBlock = getLatestBlockFromDB(conn)
    #data = getDataForMinerPaginated(conn,etherbase,perPage)
    num = getRewardCount(conn,etherbase)
    data3 = getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = getDataForMinerPaginated(conn,etherbase,per_page,page)
    #graphData = getGraphData(conn,etherbase)
    lastUpdate = getLastUpdateTime(conn)
    #close the connection so data will refresh each page
    conn.close()

    pagination = Pagination(page=page, per_page=per_page, total = num,
                            css_framework='bootstrap4')


    return render_template('miner.html',pagination=pagination,pagedBlocks="True",lastFive=lastFive,lastUpdate=lastUpdate,latestBlock=latestBlock,etherbase=etherbase,blockCount=num,data3=data3)
'''
def getMinerRank(conn,miner):
	return

def getExtraRank(conn,extra):
	return

@app.route('/miner/all/<path:etherbase>',methods=['GET'])
def minerAll(etherbase):
    allBlocks = True
    # always connect first 
    conn = connect()

    # get all the data for the template
    latestBlock = getLatestBlockFromDB(conn)
    #data = getLatestAllRewards(conn,etherbase)
    num = getRewardCount(conn,etherbase)
    data3 = getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = getLatestAllRewards(conn,etherbase)
    #graphData = getGraphData(conn,etherbase)
    lastUpdate = getLastUpdateTime(conn)
    lastMined = lastFive[0]['timest']
    #close the connection so data will refresh each page
    conn.close()

    return render_template('miner.html',lastMined=lastMined,allBlocks=allBlocks,lastFive=lastFive,lastUpdate=lastUpdate,latestBlock=latestBlock,data=data,etherbase=etherbase,blockCount=num,data3=data3)



@app.route('/miner/<path:etherbase>',methods=['GET'])
@app.route('/miner/<path:etherbase>/', defaults={'page': 1},methods=['GET'])
@app.route('/miner/<path:etherbase>/<int:page>',methods=['GET'])
def miner(etherbase,page=1):
    perPage = 10;
    # always connect first 
    conn = connect()

    # get all the data for the template
    latestBlock = getLatestBlockFromDB(conn)
    #data = getLatestAllRewards(conn,etherbase)
    num = getRewardCount(conn,etherbase)
    data3 = getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = getDataForMinerPaginated(conn,etherbase,perPage,page)
    #graphData = getGraphData(conn,etherbase)
    lastUpdate = getLastUpdateTime(conn)
    #close the connection so data will refresh each page
    conn.close()

    lastMined = lastFive[0]['timest']

    nextURL = '/miner/'+etherbase+'/'+str(page+1)
    if (page>=2):
      previous = '/miner/'+etherbase+'/'+str(page-1)
      return render_template('miner.html',lastMined=lastMined,page=page,prev_url=previous,next_url=nextURL,lastFive=lastFive,lastUpdate=lastUpdate,latestBlock=latestBlock,data=data,etherbase=etherbase,blockCount=num,data3=data3)


    return render_template('miner.html',lastMined=lastMined,page=page,next_url=nextURL,lastFive=lastFive,lastUpdate=lastUpdate,latestBlock=latestBlock,data=data,etherbase=etherbase,blockCount=num,data3=data3)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

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

@app.route('/extra/<path:extra>',methods=['GET'])
def extra(extra):
    
    # always connect first 
    conn = connect()
    #stuff for the template
    latestBlock = getLatestBlockFromDB(conn)
    lastUpdate = getLastUpdateTime(conn)
    total = getTotalByExtra(conn,extra)


    #extra stuff
    stats = getExtraStats(conn,extra)

    if (extra == 'Windows'):
      warning = 'Will only display 100 recent results for Default'
      limit = 100
      data = getDataForExtraLimited(conn,extra,limit)
      lastMined = data[0]['timest']
      return render_template('extra.html',lastMined=lastMined,warning=warning,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)

    if (extra == 'Linux'):
      warning = 'Will only display 100 recent results for Default'
      limit = 100
      data = getDataForExtraLimited(conn,extra,limit)
      lastMined = data[0]['timest']
      return render_template('extra.html',lastMined=lastMined,warning=warning,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)

    data = getDataForExtra(conn,extra)
    lastMined = data[0]['timest']

    conn.close()
    
    return render_template('extra.html',lastMined=lastMined,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)


@app.route('/howto',methods=['GET'])
def howto():
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    conn.close()
    
    return render_template('howto.html',latestBlock=latestBlock)

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

@app.route("/highscores")
def highScores():
  conn = connect()
  latestBlock = getLatestBlockFromDB(conn)
  day = 1
  week = 7
  month = 31
  limit = 50
  lastUpdate = getLastUpdateTime(conn)
  topWallets = getTopMiners(conn,limit)
  topRigs = getTopRigs(conn,limit)
  topWallets24 = getTopMinersLatest(conn,limit,day)
  topRigs24 = getTopRigsLatest(conn,limit,day)
  topWalletsWeek = getTopMinersLatest(conn,limit,week)
  topRigsWeek = getTopRigsLatest(conn,limit,week)
  topWalletsMonth = getTopMinersLatest(conn,limit,month)
  topRigsMonth = getTopRigsLatest(conn,limit,month)
  conn.close()

  return render_template('highscores.html',latestBlock = latestBlock, lastUpdate = lastUpdate, topWallets = topWallets, topRigs = topRigs,topWallets24 = topWallets24, topRigs24 = topRigs24,topWalletsWeek = topWalletsWeek, topRigsWeek = topRigsWeek,topWalletsMonth = topWalletsMonth, topRigsMonth = topRigsMonth)

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

@app.route("/statistics")
def statistics():
  conn = connect()
  latestBlock = getLatestBlockFromDB(conn)
  lastUpdate = getLastUpdateTime(conn)
  days = 30

  maxTransactions = getMaxTransactions(conn)
  maxDifficulty = getMaxDifficulty(conn) 
  maxDifficulty['difficulty'] = maxDifficulty['difficulty']/difficultyHashMagnitude
  maxDifficulty['difficulty'] = '%.2f'%(maxDifficulty['difficulty'])
  activeWallets = getActiveWallets(conn)
  totalTransactions = getTotalTransactions(conn)
  averageDifficulty = getAverageDifficulty(conn)
  averageDifficulty['average'] = float(averageDifficulty['average'])/difficultyHashMagnitude
  averageDifficulty['average'] = '%.2f'%(averageDifficulty['average'])

  maxTransactions90 = getMaxTransactions90(conn,days)
  maxDifficulty90 = getMaxDifficulty90(conn,days) 
  maxDifficulty90['difficulty'] = maxDifficulty90['difficulty']/difficultyHashMagnitude
  maxDifficulty90['difficulty'] = '%.2f'%(maxDifficulty90['difficulty'])
  activeWallets90 = getActiveWallets90(conn,days)
  totalTransactions90 = getTotalTransactions90(conn,days)
  averageDifficulty90 = getAverageDifficulty90(conn,days)
  averageDifficulty90['average'] = float(averageDifficulty90['average'])/difficultyHashMagnitude
  averageDifficulty90['average'] = '%.2f'%(averageDifficulty90['average'])

  #averageTransactins = getAverageTransactions(conn)

  conn.close()
    
  return render_template('stats.html',days=days,averageDifficulty=averageDifficulty, \
    totalTransactions=totalTransactions, activeWallets=activeWallets,highestDifficulty=maxDifficulty, \
    peakTransactions=maxTransactions,latestBlock = latestBlock, lastUpdate = lastUpdate, \
    averageDifficulty90=averageDifficulty90, \
    totalTransactions90=totalTransactions90, activeWallets90=activeWallets90,highestDifficulty90=maxDifficulty90, \
    peakTransactions90=maxTransactions90)


@app.route("/charts/difficulty")
def difficultyPage():
  conn = connect()
  latestBlock = getLatestBlockFromDB(conn)
  lastUpdate = getLastUpdateTime(conn)
  difficultyGraph = getDifficultyGraphData(conn)
  
  conn.close()

  for x in difficultyGraph:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
    
  return render_template('charts/difficulty.html',latestBlock = latestBlock, lastUpdate = lastUpdate,difficultyGraph=difficultyGraph)

def getTransactionFrequencyGraph(conn):
  cursor = conn.cursor()
  query = 'SELECT COUNT(*) AS count, DATE(timest) AS day FROM transaction GROUP BY day'
  cursor.execute(query)
  data = cursor.fetchall()
  cursor.close()
  return data


@app.route("/charts/transactions")
def transactionChart():
  conn = connect()
  latestBlock = getLatestBlockFromDB(conn)
  lastUpdate = getLastUpdateTime(conn)
  transactionGraph = getTransactionFrequencyGraph(conn)
  conn.close()
    
  return render_template('charts/transactions.html',transactionGraph=transactionGraph,latestBlock = latestBlock, lastUpdate = lastUpdate)

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

### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###

@app.route("/api/getBlock/<path:blockNum>")
def apiGetBlock(blockNum):
  conn = connect() 
  data = getBlock(conn,blockNum)
  return jsonify(data)

@app.route("/api/getLastBlocks/<path:num>")
def apiGetLastBlocks(num): 
  conn = connect()
  data = getLatestNBlocksAPI(conn,int(num))
  return jsonify(data)

@app.route("/api/miningRewards/<path:etherbase>")
def apiGetMiningRewards(etherbase): 
  conn = connect()
  data = getDataForMiner(conn,etherbase)
  return jsonify(data)

@app.route("/api/miningRewards/extra/<path:extra>")
def apiGetExtraRewards(extra): 
  conn = connect()
  data = getDataForExtra(conn,extra)
  return jsonify(data)

@app.route("/api/getTransaction/<path:hash>")
def apiGetTransaction(hash): 
  conn = connect()
  data = getTransactionAPI(conn,hash)
  return jsonify(data)

@app.route("/api/getBlockTransactions/<path:block>")
def apiGetTransactions(block): 
  conn = connect()
  data = getTransactionBlockAPI(conn,block)
  return jsonify(data)

@app.route("/api/getLatestBlock")
def apiGetLatestBlock(): 
  conn = connect()
  data = getLatestBlockFromDB(conn)
  return jsonify(data)

if __name__ == "__main__":
        app.run('127.0.0.1', 5000, debug = True)
