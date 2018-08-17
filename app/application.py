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
from flask_cors import CORS
from api_legacy import api_legacy
import databaseFuctions as db

#Initialize the app from Flask
app = Flask(__name__)
CORS(app)
app.jinja_env.globals['momentjs'] = momentjs
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3000 per hour"]
)

app.register_blueprint(api_legacy)

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

########## ########################### ##############   
########## ########################### ##############   
########## ########################### ##############   
########## functions for DB operations ##############   
########## ########################### ##############   
########## ########################### ##############   
########## ########################### ##############   

        
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
    conn = db.connect()
    latestBlock = db.getLatestBlockFromDB(conn)
    lastUpdate = db.getLastUpdateTime(conn)
    lastTen = db.getLatestNBlocksOffset(conn,per_page,page)
    graph = db.getDifficultyGraphData(conn)
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
    conn = db.connect()
    latestBlock = db.getLatestBlockFromDB(conn)
    conn.close()
    return render_template('about.html',latestBlock=latestBlock)

#howto page
@app.route('/HowTo')
def howto2():
    return redirect("/howto")

@app.route('/FAQ')
def faq1():
    return redirect("/#FAQ")

@app.route('/searchExtra',methods=['GET','POST'])
def searchExtra():
        extra = request.form.get('extra')
        conn = db.connect()

        if db.foundExtra(conn,extra):
          returnUrl = 'extra/'+extra+''
          return redirect(returnUrl)

        
        latestBlock = db.getLatestBlockFromDB(conn)
        lastTen = db.getLatestNBlocks(conn,10)
        lastUpdate = db.getLastUpdateTime(conn)
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

        conn = db.connect()
        latestBlock = db.getLatestBlockFromDB(conn)
        lastTen = db.getLatestNBlocks(conn,10)
        lastUpdate = db.getLastUpdateTime(conn)
        conn.close()
        error = "Please Enter a Valid Wallet Address"
        return homepage(error)


@app.route('/alerts', methods=['GET','POST'])
def alert():
        conn = db.connect()
        latestBlock = db.getLatestBlockFromDB(conn)
        conn.close()
        return render_template('alerts.html',latestBlock=latestBlock)

@app.route('/emailSubmit',methods=['GET','POST'])
def emailSubmit():
        conn = db.connect()
        etherbase = request.form.get('etherbase')
        email = request.form.get('email')
        extra = request.form.get('extra')
        message = db.addEmailAlert(conn,etherbase,email,extra)
        latestBlock = db.getLatestBlockFromDB(conn)
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
        conn = db.connect()
        etherbase = request.form.get('etherbaseRemove')
        email = request.form.get('emailRemove')
        extra = request.form.get('extraRemove')
        message = db.removeEmailAlert(conn,etherbase,email,extra)
        latestBlock = db.getLatestBlockFromDB(conn)
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
    conn = db.connect()

    # get all the data for the template
    latestBlock = db.getLatestBlockFromDB(conn)
    #data = getLatestAllRewards(conn,etherbase)
    num = db.getRewardCount(conn,etherbase)
    data3 = db.getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = db.getLatestAllRewards(conn,etherbase)
    #graphData = getGraphData(conn,etherbase)
    lastUpdate = db.getLastUpdateTime(conn)
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
    conn = db.connect()

    # get all the data for the template
    latestBlock = db.getLatestBlockFromDB(conn)
    #data = getLatestAllRewards(conn,etherbase)
    num = db.getRewardCount(conn,etherbase)
    data3 = db.getRewardCountByExtra(conn,etherbase)
    #last7 = getLast7Days(conn,etherbase)
    lastFive = db.getDataForMinerPaginated(conn,etherbase,perPage,page)
    #graphData = getGraphData(conn,etherbase)
    lastUpdate = db.getLastUpdateTime(conn)
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


@app.route('/extra/<path:extra>',methods=['GET'])
def extra(extra):
    
    # always connect first 
    conn = db.connect()
    #stuff for the template
    latestBlock = db.getLatestBlockFromDB(conn)
    lastUpdate = db.getLastUpdateTime(conn)
    total = db.getTotalByExtra(conn,extra)


    #extra stuff
    stats = db.getExtraStats(conn,extra)

    if (extra == 'Windows'):
      warning = 'Will only display 100 recent results for Default'
      limit = 100
      data = db.getDataForExtraLimited(conn,extra,limit)
      lastMined = data[0]['timest']
      return render_template('extra.html',lastMined=lastMined,warning=warning,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)

    if (extra == 'Linux'):
      warning = 'Will only display 100 recent results for Default'
      limit = 100
      data = db.getDataForExtraLimited(conn,extra,limit)
      lastMined = data[0]['timest']
      return render_template('extra.html',lastMined=lastMined,warning=warning,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)

    data = db.getDataForExtra(conn,extra)
    lastMined = data[0]['timest']

    conn.close()
    
    return render_template('extra.html',lastMined=lastMined,latestBlock=latestBlock, lastUpdate=lastUpdate, data = data,extra=extra,total=total,stats=stats)


@app.route('/howto',methods=['GET'])
def howto():
    conn = db.connect()
    latestBlock = db.getLatestBlockFromDB(conn)
    conn.close()
    
    return render_template('howto.html',latestBlock=latestBlock)

@app.route("/highscores")
def highScores():
  conn = db.connect()
  latestBlock = db.getLatestBlockFromDB(conn)
  day = 1
  week = 7
  month = 31
  limit = 50
  lastUpdate = db.getLastUpdateTime(conn)
  topWallets = db.getTopMiners(conn,limit)
  topRigs = db.getTopRigs(conn,limit)
  topWallets24 = db.getTopMinersLatest(conn,limit,day)
  topRigs24 = db.getTopRigsLatest(conn,limit,day)
  topWalletsWeek = db.getTopMinersLatest(conn,limit,week)
  topRigsWeek = db.getTopRigsLatest(conn,limit,week)
  topWalletsMonth = db.getTopMinersLatest(conn,limit,month)
  topRigsMonth = db.getTopRigsLatest(conn,limit,month)
  conn.close()

  return render_template('highscores.html',latestBlock = latestBlock, lastUpdate = lastUpdate, topWallets = topWallets, topRigs = topRigs,topWallets24 = topWallets24, topRigs24 = topRigs24,topWalletsWeek = topWalletsWeek, topRigsWeek = topRigsWeek,topWalletsMonth = topWalletsMonth, topRigsMonth = topRigsMonth)

@app.route("/statistics")
def statistics():
  conn = db.connect()
  latestBlock = db.getLatestBlockFromDB(conn)
  lastUpdate = db.getLastUpdateTime(conn)
  days = 30

  maxTransactions = db.getMaxTransactions(conn)
  maxDifficulty = db.getMaxDifficulty(conn) 
  maxDifficulty['difficulty'] = maxDifficulty['difficulty']/difficultyHashMagnitude
  maxDifficulty['difficulty'] = '%.2f'%(maxDifficulty['difficulty'])
  activeWallets = db.getActiveWallets(conn)
  totalTransactions = db.getTotalTransactions(conn)
  averageDifficulty = db.getAverageDifficulty(conn)
  averageDifficulty['average'] = float(averageDifficulty['average'])/difficultyHashMagnitude
  averageDifficulty['average'] = '%.2f'%(averageDifficulty['average'])

  maxTransactions90 = db.getMaxTransactions90(conn,days)
  maxDifficulty90 = db.getMaxDifficulty90(conn,days) 
  maxDifficulty90['difficulty'] = maxDifficulty90['difficulty']/difficultyHashMagnitude
  maxDifficulty90['difficulty'] = '%.2f'%(maxDifficulty90['difficulty'])
  activeWallets90 = db.getActiveWallets90(conn,days)
  totalTransactions90 = db.getTotalTransactions90(conn,days)
  averageDifficulty90 = db.getAverageDifficulty90(conn,days)
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
  conn = db.connect()
  latestBlock = db.getLatestBlockFromDB(conn)
  lastUpdate = db.getLastUpdateTime(conn)
  difficultyGraph = db.getDifficultyGraphData(conn)
  
  conn.close()

  for x in difficultyGraph:
    x['difficulty'] = float("{0:.2f}".format(x['difficulty']/difficultyHashMagnitude))
    
  return render_template('charts/difficulty.html',latestBlock = latestBlock, lastUpdate = lastUpdate,difficultyGraph=difficultyGraph)


@app.route("/charts/transactions")
def transactionChart():
  conn = db.connect()
  latestBlock = db.getLatestBlockFromDB(conn)
  lastUpdate = db.getLastUpdateTime(conn)
  transactionGraph = db.getTransactionFrequencyGraph(conn)
  conn.close()
    
  return render_template('charts/transactions.html',transactionGraph=transactionGraph,latestBlock = latestBlock, lastUpdate = lastUpdate)

@app.route("/countdown")
def countdown(): 
  conn = db.connect()
  latestBlock = db.getLatestBlockFromDB(conn)
  lastUpdate = db.getLastUpdateTime(conn)
  conn.close()
  return render_template('countdown.html',latestBlock=latestBlock,lastUpdate=lastUpdate)


if __name__ == "__main__":
        app.run('127.0.0.1', 5000, debug = True)
