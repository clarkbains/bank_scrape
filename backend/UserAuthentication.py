import mysql.connector
import random, string
from Messaging import Status
import hashlib
import time

class UserAuthentication:
    """Class to create, validate and destroy sessions. Also implements basic permissions (admin or not).
        Implements primitive hashing, for a bit of
    """
    def __init__(self,opts):
        self.db = mysql.connector.connect(**opts)
        self.cursor = self.db.cursor()
        self.sessionLength = 3600
    def addUser(self,user):
        try:
            password = self._hash(user['password'],user['user_name'])
            userData = [
                user['user_name'],
                password,
                user['email']
            ]
            loginCheck = [
                user['user_name'],
                user['email']
            ]
        except KeyError as e:
            return
        self.cursor.execute("SELECT id FROM users WHERE `user_name`= %s or `email`= %s",loginCheck)
        res = self.cursor.fetchall()
        if len(res)>0:
            return Status.warn("Account Already Exists")
        self.cursor.execute("INSERT INTO users (`user_name`,`password_hash`,`email`) VALUES (%s,%s,%s)",userData)
        self.db.commit()
        
    def login(self,user):
        if 'user_name' not in user or 'password' not in user:
            return Status.error('Must Provide Both Username and Password')
        login = [
            user['user_name'],
            self._hash(user['password'],user['user_name'])
        ]
        self.cursor.execute("SELECT id,enabled FROM users WHERE `user_name`= %s and `password_hash`= %s",login)
        res = self.cursor.fetchall()
        if len(res) == 0:
            return Status.not_authorized("Your login has failed")
        if res[0][1] == 0:
            return Status.not_authorized("Your Account is not yet validated")
        newSession = self._generateSessionId()
        expiresOn = time.time() + self.sessionLength
        self.cursor.execute("UPDATE users set session_token = %s, expires_on = %s WHERE `user_name`= %s and `password_hash`= %s",[newSession,expiresOn] + login)
        self.db.commit()
        return Status.authorized('You have logged in',newSession)

    def validateSession (self,token):
        if len(token) < 1:
            return Status.error("Your `x-auth` header must least 1 character")
        now = time.time()
        self.cursor.execute("SELECT expires_on FROM users WHERE `session_token`= %s and `expires_on`>%s and `enabled`=1",[token,now])
        res = self.cursor.fetchall()
        if len(res) == 0:
            return Status.not_authorized("Your validation has failed")
        expiresOn = now + self.sessionLength
        self.cursor.execute("UPDATE users set expires_on = %s WHERE `session_token`= %s",[expiresOn,token])
        self.db.commit()
        return Status.authorized("Your token is good",token)

    def validateAdminSession(self,token):
        res = self.validateSession(token)
        if Status.assertStatus(res,Status.AUTHORIZED):
            self.cursor.execute("SELECT admin FROM users WHERE `session_token`= %s",[token])
            res = self.cursor.fetchall()
            if len(res) != 0:
                if res[0][0]==1:
                    return Status.authorized("You are an administrator",token)
        return Status.not_authorized('You are not an administrator')

    def destroySession (self,token):
        self.cursor.execute("UPDATE users set session_token = '', expires_on = 0 WHERE `session_token`= %s",[token])
        self.db.commit()
        return Status.ok("You have been logged out") 

    def _generateSessionId(self):
        #Not really ever going to be any collisions with a 50 character string and like 3 accounts.
        while True:
            session = self._generateRandomId()
            self.cursor.execute("SELECT id FROM users WHERE `session_token`= %s",[session])
            res = self.cursor.fetchall()
            if len(res)==0:
                return session

    def _generateRandomId(self):
        letters = string.ascii_lowercase+"0123456789"
        return ''.join(random.choice(letters) for i in range(50))

    def _hash(self,password,user_name):
        hashstr = str(password)+str(user_name)
        hashstr = hashstr.encode('utf-8')
        return hashlib.sha224(hashstr).hexdigest()


class User:
    def __init__(self,request):
        self.req = request
    def getToken(self):
        print ('x-auth' in self.req.headers,self.req.method,self.req.get_json(silent=True))
        if self.req.headers.get('x-auth')!=None:

            return self.req.headers.get('x-auth')
        elif self.req.method=='POST':
            if self.req.get_json(silent=True) and 'x-auth' in self.req.get_json(silent=True):
                print (self.req.json['x-auth'])
                return self.req.json['x-auth']
        return ""