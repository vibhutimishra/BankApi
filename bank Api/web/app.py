from flask import Flask,jsonify,request
from flask_restful import Api,Resource
import os

from pymongo import MongoClient
import bcrypt

app=Flask(__name__)
api=Api(app)

client=MongoClient("mongodb://db:27017")

db=client.BankAPI

users=db["Users"]
def UserExist(unsername):
    if users.find({"username":username}).count()==0:
        return False
    else:
        return True

class Register(Resource):
    def post(username):
        if UserExist(username):
            retJson={
                "status":301,
                "msg": "Username already Exist"
            }
            return jsonify(retJson)
        else:
            hashpw=bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt)
            db.insert({
                "username":username,
                "password":hashpw,
                "balance":0,
                "debt":0
            })
            retJson={
                "status":200,
                "msg":"You have succesfully registered"
            }
            return jsonify(retJson)
def verifyPassword(username,password):
    if UserExist(username):
        haspw=users.find({
            "username":username
        })[0]["password"]

        if bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt)==hashpw:
            return True
        else:
            return False
    else:
        return False

def cashWithUser(username):
        balance=users.find({
        "username":username
        })[0]["balance"]

        return balance

def debtOfUser(username):
    debt=users.find({
    "username":username
    })[0]["dept"]

    return dept

def generateDictionary(status,msg):
    retJson={
        "status":status,
        "msg":msg
    }

    return jsonify(retJson)

def verifyCredential(username,password):
    if not UserExist(unsername):
        return generateDictionary(301, " Invalid Username"),True

    if not verifyPassword(username,password):
        return generateDictionary(302, "Invalid Username and password"),True
    else:
        return generateDictionary(200,"Ok"),False

def updateAccount(username,password):
    users.update({
        "username":username
    },{
        "balance":balance
    })

def deptUpdate(username,password):
    users.update({
        "username":username
    },{
        "dept":dept
    })

class Add(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        amount=postedData["amount"]

        retJson,error= verifyCredential(username,password)

        if error:
            return jsonify(retJson)
        if amount<=0:
            retJson=generateDictionary(304,"The amount entered should be greater than 0")
        cash=cashWithUser(username)
        money-=1
        bankCash=cashWithUser("Bank")
        updateAccount("Bank",bankCash+1)
        updateAccount(username,cash+1)

        retJson = generateDictionary(200," amount added succesfully")

class Transfer(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        username2=postedData["username2"]
        amount=postedData["amount"]

        retJson,error= verifyCredential(username,password)
        error2 = UserExist(unsername2)

        if error1:
            return jsonify(retJson)
        cash= cashWithUser(username)
        if cash<=0:
            return jsonify(generateDictionary(304,"You are out of money, please add or take loan"))
        if not error2:
            return jsonify(generateDictionary(301,"Invalid Username"))
        if amount>=cash:
            return jsonify(generateDictionary(301," your account does not have enough money for this transaction"))
        cashFrom=cashWithUser(username)

        cashTo=cashWithUser(username2)

        bankCash=cashWithUser("Bank")

        updateAccount("Bank",bankCash+1)
        updateAccount(username,cashFrom-amount)
        updateAccount(username2, cashTo+money-1)

        return jsonify(generateDictionary(200,"Amount transfered"))

class Balance(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]

        retJson,error= verifyCredential(username,password)

        if error:
            return jsonify(retJson)
        else:
            msg={
                "balance":cashWithUser(username),
                "dept":deptOfUser(username)

            }
            return jsonify(generateDictionary(200,msg))

class TakeLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        amount=postedData["amount"]

        retJson,error= verifyCredential(username,password)

        if error:
            return jsonify(retJson)
        cash= cashWithUser(username)
        dept=deptOfUser(username)

        updateAccount(username,cash+amount)
        deptUpdate(username,dept+money)

        return jsonify(generateDictionary(200,"Loan added to the account"))

class PayLoan(Resource):
    def post(self):
        postedData=request.get_json()

        username=postedData["username"]
        password=postedData["password"]
        amount=postedData["amount"]

        if error:
            return jsonify(retJson)
        cash= cashWithUser(username)
        dept=deptOfUser(username)

        if cash<money:
            return jsonify(generateDictionary(303,"Not enough money to pay"))

        updateAccount(username,cash-amount)
        deptUpdate(username,dept-money)

        return jsonify(generateDictionary(200,"Loan paid to the Bank"))

api.add_resource(Register,'/register')
api.add_resource(Add,'/add')
api.add_resource(Transfer,'/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan,'/takeloan')
api.add_resource(PayLoan,'/payloan')


if __name__=="__main__":
    port = int(os.environ.get('MYAPP_PORT', 5000))
    app.run(host='0.0.0.0',port=port)
