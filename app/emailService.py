from flask import Blueprint,request,render_template
emailService = Blueprint('emailService', __name__)
import databaseFuctions as db
import smtplib
import re

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

@emailService.route('/emailSubmit',methods=['GET','POST'])
def emailSubmit():
        conn = db.connect()
        etherbase = request.form.get('etherbase')
        email = request.form.get('email')
        extra = request.form.get('extra')
        message = db.addEmailAlert(conn,etherbase,email,extra)
        latestBlock = db.getLatestBlockFromDB(conn)
        conn.close()

        if message == "Sucsess":
        	sendSignupConfirmation(etherbase,email,extra)
        	return render_template('alerts.html',latestBlock=latestBlock,message=message)
        else:
        	return render_template('alerts.html',latestBlock=latestBlock,error=error)
       

@emailService.route('/emailRemove',methods=['GET','POST'])
def emailRemove():
        conn = db.connect()
        etherbase = request.form.get('etherbaseRemove')
        email = request.form.get('emailRemove')
        extra = request.form.get('extraRemove')
        message = db.removeEmailAlert(conn,etherbase,email,extra)
        latestBlock = db.getLatestBlockFromDB(conn)
        conn.close()

        if message == "Sucsess":
        	sendUnsubstribeConfirmation(etherbase,email)
        	return render_template('alerts.html',latestBlock=latestBlock,message=message)
        else:
        	return render_template('alerts.html',latestBlock=latestBlock,error=error)
