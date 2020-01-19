from Messaging import Status
from database import Database
from UserAuthentication import UserAuthentication, User
from flask import Flask, request
from auth import Auth
import json
app = Flask(__name__)
opts = {
        'host':Auth.host,
        'user':Auth.user,
        'passwd':Auth.password,
        'database':Auth.database,
        'auth_plugin':"mysql_native_password"
    }

db = Database(opts)
ua = UserAuthentication(opts)


@app.route("/api/create", methods=['POST'])
def createUser():
    return ua.addUser(getContentBody())

@app.route("/api/login", methods=['POST'])
def login():
    return ua.login(getContentBody())

@app.route("/api/logout", methods=['POST'])
def logout():
    token = User(request).getToken()
    return ua.destroySession(token)

@app.route("/api/validate", methods=['POST'])
def validate():
    token = User(request).getToken()
    return ua.validateSession(token)

@app.route("/api/validateadmin", methods=['POST'])
def validateadmin():
    token = User(request).getToken()
    return ua.validateAdminSession(token)

@app.route("/api/describe/accounts", methods=['POST'])
def describeAccounts():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    return Status.json(db.describeAccounts("account_id"))

@app.route("/api/describe/current", methods=['POST'])
def describeCurrent():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    return Status.json(db.describeValues("account_id"))
@app.route("/api/describe/historic", methods=['POST'])
def describeHistoric():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    body = getContentBody()
    return Status.json(db.describeHistoricValues(body['account_id']))

    
def getContentBody():
    return request.json
if __name__=='__main__':
    app.run(port=8080)