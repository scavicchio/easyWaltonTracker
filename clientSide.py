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
import pymysql.cursors


#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='waltonchain',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define route for login
@app.route('/')
def homepage():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/search', methods=['GET','POST'])
def searchMiner():
        etherbase = request.form.get('etherbase')
        return miner(etherbase)
        
@app.route('/miner/<etherbase>',methods=['GET'])
def miner(etherbase):
        cursor = conn.cursor()
        query = 'SELECT * FROM BlockChain WHERE miner = %s'
        cursor.execute(query, (etherbase))
        data = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query2 = 'SELECT COUNT(*) FROM BlockChain WHERE miner = %s'
        cursor.execute(query2, (etherbase))
        data2 = cursor.fetchone()
        cursor.close()
        num = data2["COUNT(*)"]

        cursor = conn.cursor()
        query3 = 'SELECT extra_data, COUNT(blockNum) AS theCount FROM blockchain WHERE miner = %s GROUP BY extra_data'
        cursor.execute(query3,(etherbase))
        data3 = cursor.fetchall()
        cursor.close()
        print(data3)

        return render_template('miner.html',data=data,etherbase=etherbase,blockCount=num,data3=data3)

@app.route('/miner/<etherbase>/<key>',methods=['GET'])
def minerKey(etherbase,key):
        print("will grab data for below etherbase:")
        print(etherbase)
        cursor = conn.cursor()
        query = 'SELECT * FROM BlockChain WHERE miner = %s'
        cursor.execute(query, (etherbase))
        data = cursor.fetchall()
        cursor.close()

        print(data)
        return render_template('miner.html',data=data,etherbase=etherbase)

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
