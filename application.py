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
from flask import Flask, render_template, request, session, url_for, redirect
from flask_bootstrap import Bootstrap
import pymysql.cursors
import re
import smtplib

#Initialize the app from Flask
app = Flask(__name__)

#GLOBAL VARS FOR EMAIL
username = 'easyWaltonMiner@gmail.com'
password = ''
difficultyHashMagnitude = 1000000000

#Configure MySQL
conn = pymysql.connect(host='waltonchain.ci9smifyvaqf.us-east-2.rds.amazonaws.com',
                       port = 3306,
                       user='remoteclient',
                       password='',
                       db='waltonchain',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def connect():
        conn = pymysql.connect(host='waltonchain.ci9smifyvaqf.us-east-2.rds.amazonaws.com',
                       port = 3306,
                       user='remoteclient',
                       password='',
                       db='waltonchain',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
        return conn

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
    query = 'SELECT blockNum FROM BlockChain ORDER BY blockNum DESC LIMIT 1'
    cursor.execute(query)
    latestBlock = cursor.fetchone()
    cursor.close()
    return latestBlock["blockNum"];

# gets all data for a specific etherbase
def getDataForMiner(conn, etherbase):
    cursor = conn.cursor()
    query = 'SELECT * FROM BlockChain WHERE miner = %s'
    cursor.execute(query, (etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

# gets the total blocks a miner has solved
def getRewardCount(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM BlockChain WHERE miner = %s'
    cursor.execute(query, (etherbase))
    data = cursor.fetchone()
    cursor.close()
    return data["COUNT(*)"]

# returns the number of rewards for each unique extraData as a pair.
def getRewardCountByExtra(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT extra_data, COUNT(blockNum) AS theCount FROM BlockChain WHERE miner =%s GROUP BY extra_data ORDER BY theCount DESC'
    cursor.execute(query,(etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

def getLast7Days(conn,etherbase):
    cursor = conn.cursor()
    query = 'SELECT COUNT(blockNum) AS theCount FROM BlockChain WHERE miner = %s AND timest >= DATE(NOW()) - INTERVAL 7 DAY GROUP BY extra_data'
    cursor.execute(query,(etherbase))
    data = cursor.fetchall()
    cursor.close()
    return data

# reurns all info from latest X rewards for a given address
def getLatestNRewards(conn,etherbase,index):
  cursor = conn.cursor()
  query = 'SELECT * FROM BlockChain WHERE miner = %s ORDER BY blockNum DESC LIMIT %s'
  cursor.execute(query, (etherbase,index))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
  cursor.close()
  return data

def getLatestAllRewards(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT * FROM BlockChain WHERE miner = %s ORDER BY blockNum DESC'
  cursor.execute(query, (etherbase))
  data = cursor.fetchall()
  for x in data:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))

  cursor.close()
  return data

#gets all blocks, timest and extra for a JS graph for later
def getGraphData(conn,etherbase):
  cursor = conn.cursor()
  query = 'SELECT blockNum, extra_data, timest FROM BlockChain WHERE miner = %s ORDER BY timest ASC'
  cursor.execute(query, (etherbase))
  data = cursor.fetchall()
  cursor.close()
  return data

#gets most recent N blocks, data, and time for homepage
def getLatestNBlocks(conn,index):
  cursor = conn.cursor()
  query = 'SELECT * FROM BlockChain ORDER BY timest DESC LIMIT %s'
  cursor.execute(query, (index))
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
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    lastTen = getLatestNBlocks(conn,10)
    conn.close()
    if (error != "None"):
      return render_template('home.html',latestBlock=latestBlock,lastTen=lastTen,error=error)

    return render_template('home.html',latestBlock=latestBlock,lastTen=lastTen)

#about page
@app.route('/about')
def about():
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    blockData = getLatestNBlocks(conn,10)
    conn.close()
    return render_template('about.html',latestBlock=latestBlock)

# for homepage search bar
@app.route('/search', methods=['GET','POST'])
def searchMiner():
        etherbase = request.form.get('etherbase')

        if goodEtherbase(etherbase):
          returnUrl = 'miner/'+etherbase+''
          return redirect(returnUrl)

        conn = connect()
        latestBlock = getLatestBlockFromDB(conn)
        lastTen = getLatestNBlocks(conn,10)
        conn.close()
        error = "Please Enter a Valid Wallet Address"
        return render_template('home.html',latestBlock=latestBlock,lastTen=lastTen,error=error)


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
        

# route for miner data page
@app.route('/miner/<etherbase>',methods=['GET'])
def miner(etherbase):
    # always connect first 
    conn = connect()

    # get all the data for the template
    latestBlock = getLatestBlockFromDB(conn)
    data = getDataForMiner(conn,etherbase)
    num = getRewardCount(conn,etherbase)
    data3 = getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = getLatestAllRewards(conn,etherbase)
    graphData = getGraphData(conn,etherbase)

    #cloe the connection so data will refresh each page
    conn.close()

    return render_template('minerChart.html',lastFive=lastFive,latestBlock=latestBlock,data=data,etherbase=etherbase,graphData=graphData,blockCount=num,data3=data3)

@app.route('/howto',methods=['GET'])
def howto():
    conn = connect()
    latestBlock = getLatestBlockFromDB(conn)
    conn.close()
    
    return render_template('howto.html',latestBlock=latestBlock)



if __name__ == "__main__":
        app.run('127.0.0.1', 5000, debug = True)
