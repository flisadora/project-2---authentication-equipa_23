import os
import re
import cherrypy
import json
from jinja2 import Environment, FileSystemLoader
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
import base64
from encrypt import decryptDES, encryptDES, toBinary, doPBKDF2
env = Environment(loader=FileSystemLoader('templates'))


USERS = {'jon': 'secret', 'user': 'password'}

class UAP(object):
    @cherrypy.expose
    def index(self):
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
        
        tmpl = env.get_template('index.html')
        for u in passwords["users"]:
            salt = toBinary(u["salt"])
            # print("PASSWORD", u["password"])
            password = toBinary(u["password"])
            # print(password)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt = salt,
                iterations=500000,
                backend=default_backend()
            )

            try:
                username = toBinary(u["username"])
                kdf.verify((cherrypy.session["user"]).encode('utf-8'), username)

                data = []
                for cred in u["logins"]:
                    nonce = toBinary(cred["salt"])
                    values = cred
                    del values["salt"]
                    decrypted = decryptDES(nonce, password, values)

                    data.append({
                        "dns": decrypted["dns"],
                        "email": decrypted["email"],
                        "password": decrypted["password"],
                    })
                #print(data)
                return tmpl.render(passwords=data)
            except cryptography.exceptions.InvalidKey:
                pass
        return # tmpl.render(passwords=passwords["users"])

    @cherrypy.expose
    def new_login(self):
        tmpl = env.get_template('new_login.html')
        return tmpl.render(user=cherrypy.session["user"])

@cherrypy.expose
@cherrypy.config(**{'tools.CORS.on': True})
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class UAPWebService(object):

    def GET(self):
        with open("passwords.json", "r") as f:
            passwords = json.load(f)

        for u in passwords["users"]:
            salt = toBinary(u["salt"])
            # print("PASSWORD", u["password"])
            password = toBinary(u["password"])
            # print(password)
            
            isUser = doPBKDF2(salt, (cherrypy.session["user"].encode('utf-8')), toBinary(u["username"]))
            
            if isUser:
                data = []
                for cred in u["logins"]:
                    nonce = toBinary(cred["salt"])
                    values = cred
                    del values["salt"]
                    decrypted = decryptDES(nonce, password, values)
                    
                    data.append({
                        "dns": decrypted["dns"],
                        "email": decrypted["email"],
                        "password": decrypted["password"],
                    })
                #print(data)
                return data
        return # tmpl.render(passwords=passwords["users"])

    def POST(self):
        # data from request
        request = cherrypy.request.json
        user = request["user"]
        inputDns = request["inputDns"]
        inputEmail1 = request["inputEmail1"]
        inputPassword = request["inputPassword"]

        # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not inputDns or not inputEmail1 or not inputPassword:
            return {"state": "Invalid values"}

        if not re.fullmatch(email_regex, inputEmail1):
            return {"state": "Invalid email"}

        with open("passwords.json", "r") as f:
            d = json.load(f)

        login = {}
        for u in d["users"]:
            salt = toBinary(u["salt"])
            # print("PASSWORD", u["password"])
            password = toBinary(u["password"])
            # print(password)

            isUser = doPBKDF2(salt, user.encode('utf-8'), toBinary(u["username"]))
            
            if isUser:
                values = {"dns": inputDns, "email": inputEmail1, "password": inputPassword}
                res = encryptDES(password, values)

                login["dns"] = res["dns"]
                login["email"] = res["email"]
                login["password"] = res["password"]
                login["salt"] = res["salt"]
                u["logins"].append(login)

                # save new login
                with open("passwords.json", "w") as f:
                    json.dump(d, f)
                return {"state": "success"}
                # return tmpl.render(passwords=data)
        return {"state": "Failed to Add New Login"}
        

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

def checkpassword(realm, username, password):
    with open("passwords.json") as credentials:
        logins = json.load(credentials)
        for u in logins["users"]:
            salt = toBinary(u["salt"])
            user = toBinary(u["username"])

            isUser = doPBKDF2(salt, username.encode('utf-8'), user)
            
            if isUser:
                passw = toBinary(u["password"])

                isPassword = doPBKDF2(salt, password.encode('utf-8'), passw)
                
                if isPassword:
                    cherrypy.session["user"] = username
                    return True  
    return False

def CORS():
    if cherrypy.request.method == 'OPTIONS':
        # preflign request 
        # see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
        # tell CherryPy no avoid normal handler
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_port': 8443,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': "cert.pem",
        'server.ssl_private_key': "privkey.pem",
        }
    )
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)
    
    conf = {
    '/': {
        'tools.CORS.on': True,
        'tools.sessions.on': True,
        'tools.auth_basic.on': True,
        'tools.auth_basic.realm': 'localhost',
        'tools.auth_basic.checkpassword': checkpassword,
        'tools.auth_basic.accept_charset': 'UTF-8',
        'tools.secureheaders.on': True,
        'tools.response_headers.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
    '/api': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './public'
        }
    }
    
    cherrypy.tools.secureheaders = cherrypy.Tool('before_handler', secureheaders)
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)

    webapp = UAP()
    webapp.api = UAPWebService()
    cherrypy.quickstart(webapp, "/", conf)