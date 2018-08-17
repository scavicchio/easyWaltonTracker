from flask import jsonify,Blueprint, request
import databaseFuctions as db
import google_analytics as ga

api_legacy = Blueprint('api_legacy', __name__)

### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###
### APP ROUTES FOR API ###

def getIP():
  return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

@api_legacy.route("/api/getBlock/<path:blockNum>")
def apiGetBlock(blockNum):
  conn = db.connect() 
  data = db.getBlock(conn,blockNum)
  ga.track_event(
        user = getIP(),
        category='API',
        action='/getBlock',
        label=blockNum,
        )
  return jsonify(data)

@api_legacy.route("/api/getLastBlocks/<path:num>")
def apiGetLastBlocks(num): 
  conn = db.connect()
  data = db.getLatestNBlocksAPI(conn,int(num))
  ga.track_event(
        user = getIP(),
        category='API',
        action='/getLastBlocks',
        label=num,
        )
  return jsonify(data)

@api_legacy.route("/api/miningRewards/<path:etherbase>")
def apiGetMiningRewards(etherbase): 
  conn = db.connect()
  data = db.getDataForMiner(conn,etherbase)
  ga.track_event(
        user = getIP(),
        category='API',
        action='/miningRewards',
        label=etherbase,
        )
  return jsonify(data)

@api_legacy.route("/api/miningRewards/extra/<path:extra>")
def apiGetExtraRewards(extra): 
  conn = db.connect()
  data = db.getDataForExtraAPI(conn,extra)
  ga.track_event(
        user = getIP(),
        category='API',
        action='/miningRewards/extra',
        label=extra,
        )
  return jsonify(data)

@api_legacy.route("/api/getTransaction/<path:hash>")
def apiGetTransaction(hash): 
  conn = db.connect()
  data = db.getTransactionAPI(conn,hash)
  ga.track_event(
        user = getIP(),
        category='API',
        action='getTransaction',
        label=hash,
        )
  return jsonify(data)

@api_legacy.route("/api/getBlockTransactions/<path:block>")
def apiGetTransactions(block): 
  conn = db.connect()
  data = db.getTransactionBlockAPI(conn,block)
  ga.track_event(
        user = getIP(),
        category='API',
        action='getBlockTransactions',
        label=block,
        )
  return jsonify(data)

@api_legacy.route("/api/getLatestBlock")
def apiGetLatestBlock(): 
  conn = db.connect()
  data = db.getLatestBlockFromDB(conn)
  ga.track_event(
        user = getIP(),
        category='API',
        action='getLatestBlock'
        )
  return jsonify(data)
