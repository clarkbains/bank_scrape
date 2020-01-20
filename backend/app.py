from Messaging import Status
from database import Database
from UserAuthentication import UserAuthentication, User
from flask import Flask, request, render_template,jsonify
from auth import Auth
import json,os,re
template_dir = os.path.abspath('../frontend')
app = Flask(__name__,template_folder=template_dir)
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
    response = app.response_class(        response=json.dumps(ua.login(getContentBody())),        status=200,        mimetype='application/json')
    return response

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

@app.route("/api/describe/accounts", methods=['GET'])
def describeAccounts():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    return Status.json(db.describeAccounts("account_id"))

@app.route("/api/describe/current", methods=['GET'])
def describeCurrent():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    return Status.json(db.describeValues("account_id"))
@app.route("/api/describe/historic", methods=['GET'])
def describeHistoric():
    res = validate()
    if not Status.assertStatus(res,Status.AUTHORIZED):
        return Status.not_authorized("You are not authorized to do this")
    body = getContentBody()
    return Status.json(db.describeHistoricValues(body['account_id']))
routes = {
    'login':'login'

}
defaultFile = 'index.html'

@app.route("/<string:file>", methods=['GET'])
def display_main(file):
    if re.match('\w+\.\w+',file):
        return render_template(file)
    
    return render_template(file+'/'+defaultFile)

@app.route("/login/<string:file>", methods=['GET'])
def display_login(file):
    print(file)
    return render_template('login/'+file)

    
    
def getContentBody():
    if request.json != None:
        return request.json
    if request.form.to_dict() != {}:
        return request.form.to_dict()
    return {}
if __name__=='__main__':
    app.run(port=8000)