from flask import Flask,url_for,Response,jsonify,json,request
from datetime import datetime
import MySQLdb

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"



# @app.route("/connectDB")
def connectDb():
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="trams",  # your password
                         db="trams_test")  # name of the data base
    # cur = db.cursor()

    return db

    # cur.execute("SELECT * FROM User")
    #
    # retList = cur.fetchall()
    #
    # row = retList[0]
    #
    # # for row in retList:
    # print row
    #
    # # return "User name %s " % row[1]
    # # return "success"
    #
    # return jsonify(retList)

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

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


@app.route('/get_All_User',methods=['GET'])
def getAllUser():

    # cur = connectDb()

    sqlGetAll = "Select * FROM User"

    cur.execute(sqlGetAll)

    userList = cur.fetchall()

    return jsonify(userList)


@app.route('/get_User_By_UserName',methods =['GET'])
def getByUserName():
    if 'userName' in request.args:

        requestUserName = request.args.get('userName')

        # cur = connectDb()

        sqlGetUser = "SELECT * FROM User where userName = " + requestUserName

        cur.execute(sqlGetUser)

        userList = cur.fetchall()

        return jsonify(userList)

        # return 'Hello ' + request.args['userName']
    else:
        return 'Hello anonymous'

@app.route('/register_User',methods=['POST'])
def registerNewUser():
    if request.headers['Content-Type'] != 'application/json':

        return jsonify({
            "code":400,
            "message": "Application does not support json"
        })

    jsonPosted = request.get_json()

    userName = jsonPosted['userName']
    password = jsonPosted['password']

    createdDate = datetime.now()
    updatedDate = datetime.now()

    if "createdDate" in jsonPosted:
        createdDate = datetime.strptime(jsonPosted['createdDate'], '%Y-%m-%d %H:%M:%S')

    if "updatedDate" in jsonPosted:
        updatedDate = datetime.strptime(jsonPosted['updatedDate'], '%Y-%m-%d %H:%M:%S')

    if "description" in jsonPosted:
        description = jsonPosted['description']


    sqlCheckUser = "SELECT * FROM User where userName = '%s'" %userName
    cur.execute(sqlCheckUser)

    numberOfUserCount = cur.rowcount

    if numberOfUserCount > 0:
        return jsonify({
            "code":400,
            "message": "User Name was registered"
        })

    sqlAddNewUser = "INSERT INTO User(userName,password,createdDate,updatedDate,description) values('%s','%s','%s','%s','%s');" % (userName,password,createdDate,updatedDate,description)

    print(sqlAddNewUser)

    try:
        cur.execute(sqlAddNewUser)
        db.commit()

        # newUser = cur.lastrowid

        return jsonify({
            "code":201,
            "message":"Success fully create",
            # "User":newUser
        })

    except:
        db.rollback()
        return jsonify({
            "code":500,
            "message":"Error when add new User"
        })


    # return jsonify(request.get_json())

@app.route("/delete_User",methods = ['DELETE'])
def deleteCurrentUser():
    if request.headers['Content-Type'] != 'application/json':

        return jsonify({
            "code":400,
            "message": "Application does not support json"
        })

    jsonPosted = request.get_json()

    userName = jsonPosted['userName']

    sqlDelteUser = "DELETE FROM User WHERE userName = '%s'" %userName

    print(sqlDelteUser)

    try:
        cur.execute(sqlDelteUser)
        db.commit()

        # newUser = cur.lastrowid

        return jsonify({
            "code":200,
            "message":"Deleted Successfully",
        })

    except:
        db.rollback()
        return jsonify({
            "code":500,
            "message":"Error when delete User"
        })

@app.route("/update_User",methods=['PUT'])
def updateUser():
    if request.headers['Content-Type'] != 'application/json':

        return jsonify({
            "code":400,
            "message": "Application does not support json"
        })

    jsonPosted = request.get_json()

    userName = ""
    password = ""
    createdDate = ""
    updatedDate = ""
    description = ""

    if "userName" in jsonPosted:
        userName = jsonPosted["userName"]

        sqlGetUser = "SELECT * FROM User where userName = '%s'" %userName

        try:
            cur.execute(sqlGetUser)
            numberOfRow = cur.rowcount

            if numberOfRow <= 0:
                return jsonify({
                    "code": 200,
                    "message": "UserName is invalid",
                })

        except:
            db.rollback()
            return jsonify({
                "code": 500,
                "message": "Error when Update User"
            })

    else:
        return  jsonify({
            "code":400,
            "message":"UserName required"
        })

    sqlUpdate = "Update User set "

    # if "userName" in jsonPosted:
    #     userName = jsonPosted["userName"]
    #     sqlUpdate += ("userName = '%s'," %userName)

    if "password" in jsonPosted:
        password = jsonPosted["password"]
        sqlUpdate += ("password = '%s'," %password)

    if "createdDate" in jsonPosted:
        createdDate = jsonPosted["createdDate"]
        sqlUpdate += ("createdDate = '%s'," % datetime.strptime(jsonPosted['createdDate'], '%Y-%m-%d %H:%M:%S'))

    if "updatedDate" in jsonPosted:
        updatedDate = jsonPosted["updatedDate"]
        sqlUpdate += ("updatedDate = '%s'," % datetime.strptime(jsonPosted['updatedDate'], '%Y-%m-%d %H:%M:%S'))

    if "description" in jsonPosted:
        description = jsonPosted["description"]
        sqlUpdate += ("description = '%s'" %description)


    # password = jsonPosted['password']
    # createdDate = datetime.strptime(jsonPosted['createdDate'], '%Y-%m-%d %H:%M:%S')
    # updatedDate = datetime.strptime(jsonPosted['updatedDate'], '%Y-%m-%d %H:%M:%S')
    # description = jsonPosted['description']

    sqlUpdate += (" where userName = '%s'" % jsonPosted["userName"])


    print(sqlUpdate)

    try:
        cur.execute(sqlUpdate)
        db.commit()
        numberOfRow = cur.rowcount

        print(numberOfRow)

        # newUser = cur.lastrowid

        return jsonify({
            "code":200,
            "message":"Updated Successfully",
        })

    except:
        db.rollback()
        return jsonify({
            "code":500,
            "message":"Error when Update User"
        })

@app.route('/login',methods=['POST'])
def login():
    jsonPosted = request.get_json()

    userName = ""
    password = ""

    if "userName" in jsonPosted:
        userName = jsonPosted['userName']
    else:
        return jsonify({
            "code":400,
            "message": "Please input userName"
        })

    if "password" in jsonPosted:
        password = jsonPosted['password']
    else:
        return jsonify({
            "code":400,
            "message": "Please input password"
        })

    sqlCommand = "SELECT * FROM User where userName='%s' AND password='%s'" %(userName,password)

    print(sqlCommand)

    try:
        cur.execute(sqlCommand)
        numberOfRow = cur.rowcount

        if numberOfRow == 1:
            return jsonify({
                "code": 200,
                "message": "Login Successfully",
            })
        else:
            return jsonify({
                "code":204,
                "message":"Invalid UserName or Password"
            })


    except:
        db.rollback()
        return jsonify({
            "code": 500,
            "message": "Error when Update User"
        })

if __name__ == "__main__":
    app.run()