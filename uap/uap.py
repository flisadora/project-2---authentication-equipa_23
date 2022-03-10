import os
import re
import cherrypy
import json
import asyncio
import aiohttp
from jinja2 import Environment, FileSystemLoader
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from encrypt import decryptDES, encryptDES, toBinary, doPBKDF2
import hashlib
import base64
env = Environment(loader=FileSystemLoader('templates'))

'''
    post message types:
    1. hello
    2. challenge
    3. challenge + response
    4. end of auth
    5. msg error
    6. username + role
    7. response username + role
'''

USERS = {'jon': 'secret', 'user': 'password'}

class UAP(object):
    @cherrypy.expose
    def index(self,auth_msg=None, url=None, domain=None):

        if url:
            cherrypy.session["url"] = url
            cherrypy.session["domain"] = domain
        
        if auth_msg!=None:
            tmpl = env.get_template('auth_error.html')
            return tmpl.render(auth_msg=auth_msg)

        tmpl = env.get_template('index.html')
        return tmpl.render()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=('POST'))
    def submit_credentials(self, dns, email, password):
        
        valid_user_auth, SESSION_ID = asyncio.run(challenge(cherrypy.session["url"], email, password))      

        # if user is valid make another request to server 'username' and 'role'
        # if user is not valid redirect to login with message of authentication failure
        if valid_user_auth == 0:
            string = "/?auth_msg=Invalid+user.+" + SESSION_ID
            raise cherrypy.HTTPRedirect(string)
        
        if valid_user_auth == -1:
            raise cherrypy.HTTPRedirect("/?auth_msg=Invalid+dns.+" + SESSION_ID)

        username, role = asyncio.run(auth_final_msg(cherrypy.session["url"], SESSION_ID, email))

        if username == -1:
            raise cherrypy.HTTPRedirect("/?auth_msg=User+not+found.+" + role)

        #send response to challege
        raise cherrypy.HTTPRedirect("http://localhost:3000?username="+ username + "&role=" + str(role))

    @cherrypy.expose
    def new_login(self):
        tmpl = env.get_template('new_login.html')
        return tmpl.render(user=cherrypy.session["user"], domain=cherrypy.session["domain"])

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
            password = toBinary(u["password"])
            
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
                
                return data
        return 

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
            password = toBinary(u["password"])

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
        
    
async def auth_final_msg(dns, session_id, email):

    msg = {"type": 6, "email": email}

    async with aiohttp.ClientSession() as session:
        
        try:
            async with session.get(dns + '?PHPSESSID='+ session_id, json=msg, ssl=False) as resp:
                post_response = await resp.text()
                await session.close()
        except aiohttp.ClientConnectorError as e:
          return -1, "Phase+6"

    response = json.loads(post_response)

    if response['type'] == 5:
        if "error" in response:
            return None, "Phase+6"
        return None, "Phase+7"
        
    return response['username'], response['role']


async def challenge(dns, email, password):

    hellomsg = {"type": 1, "email": email}
    valid_user_auth = 1
    url = dns + '?PHPSESSID='
    SESSION_ID = ""

    async with aiohttp.ClientSession() as session:

        try:
            async with session.post(url+ SESSION_ID, json=hellomsg, ssl=False) as resp:
                post_response = await resp.text()
                await session.close()
        except aiohttp.ClientConnectorError as e:
            return -1, "Phase+1"
    
    challenge_json = json.loads(post_response)
    challenge = challenge_json['key']

    if challenge_json['type'] == 5:
        if "error" in challenge_json:
            return 0, "Phase+1"
        return 0, "Phase+2"

    SESSION_ID = challenge_json['session_id']

    async with aiohttp.ClientSession() as session:
        while True:
            if valid_user_auth == 1:
                response = calc_response(challenge, password)
            else:
                response = base64.b64encode(challenge.encode('utf-8'))[0] & 1
            uap_challenge = base64.b64encode(os.urandom(16))

            uap_response = calc_response(uap_challenge.decode(), password)
            chall_resp_msg = {'type': 3, 'key': uap_challenge.decode(), 'response': response}

            try:
                async with session.post(url+ SESSION_ID, json=chall_resp_msg, ssl=False) as resp:
                    post_response = await resp.text()
            except aiohttp.ClientConnectorError as e:
                return -1, "Phase+3"
            
            challenge_json = json.loads(post_response)
            response_from_server = challenge_json['response']
            
            if challenge_json['type'] == 4:
                valid_user_auth = verify_response(uap_response, response_from_server, valid_user_auth)
                valid_user_auth = challenge_json['auth'] & valid_user_auth
                break
            else:
                challenge = challenge_json['key']
            
            # if responses dont match random responses will be sent instead
            valid_user_auth = verify_response(uap_response, response_from_server, valid_user_auth)

    await session.close()

    if valid_user_auth == 0:
        return valid_user_auth, "Phase+4"
    return valid_user_auth, SESSION_ID

def verify_response(uap_response, response_from_server, valid_user_auth):
    if (uap_response != response_from_server) and (valid_user_auth == 1):
        return 0
    return valid_user_auth

def calc_response(challenge, password):
    if isinstance(challenge, str):
        challenge = challenge.encode('utf-8')
    hashed_password = hashlib.md5(password.encode())
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32, salt=challenge, iterations=5, backend=default_backend())
    response = kdf.derive(hashed_password.hexdigest().encode('utf-8'))

    xor_result = base64.b64encode(response)[0] & 1
    #the chosen bit is a xor of all the response bits
    for i in range(1, len(response)):
        xor_result ^= (base64.b64encode(response)[i] & 1)

    return xor_result

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

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
