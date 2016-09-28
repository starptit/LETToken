#from twilio.rest import TwilioRestClient
from flask import Flask,jsonify,request,url_for,Response,jsonify,json,request
from faker import Factory

import MySQLdb

#from twilio.access_token import AccessToken,IpMessagingGrant

app = Flask(__name__)
#fake = Factory.create()

@app.route('/')
def index():
    return 'Hello World!'

def connectDb():
    db = MySQLdb.connect(host="14.63.219.203",  # your host, usually localhost
                         user="root",  # your username
                         passwd="trams@#",  # your password
                         db="let_company")  # name of the data base
    return db

db = connectDb()
cur = db.cursor()

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/api_hello', methods = ['GET'])
def api_hello():

    data = {
        'hello' : 'world',
        'number':3
    }

    # js = json.dumps(data)
    #
    # resp = Response(js, status=200, mimetype='application/json')
    # resp.headers['Link'] = 'http://trams.co.kr'
    # return resp

    return jsonify(results = data,status = 200)


@app.route('/get_All_Tokens',methods=['GET'])
def getTokens():

    # cur = connectDb()

    sqlGetAll = "Select token,type FROM tokens where STATUS = 0 order by id desc"

    cur.execute(sqlGetAll)

    tokenList = cur.fetchall()

    #print(tokenList)
    list = []

    for row in tokenList:
        #print(row)
        rowValue = {"token":row[0],
                   "type":row[1],
                    "type = 1": "token for reset password",
                    "type = 0": "token for register"
                    }
        list.append(rowValue)

    #return jsonify({
     #   "token" : tokenList,
      #  "type": tokenList,
       # "type = 1":"token for reset password",
        #"type = 0":"token for register"
         #           })

    return  jsonify({"result":list})

if __name__ == "__main__":
    app.run()