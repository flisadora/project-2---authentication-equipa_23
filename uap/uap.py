import cherrypy
from cherrypy.lib import auth_digest
import json
import requests
import asyncio
import aiohttp
#import requests_async as requests
from random import randint
from jinja2 import Environment, FileSystemLoader
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import os
from Crypto.Cipher import AES
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

USERS = {'jon': 'secret'}

class UAP(object):
    @cherrypy.expose
    def index(self, auth_msg=None):
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
        
        if auth_msg!=None:
            tmpl = env.get_template('auth_error.html')
            return tmpl.render(passwords=passwords, auth_msg=auth_msg)

        tmpl = env.get_template('index.html')
        return tmpl.render(passwords=passwords)

    @cherrypy.expose
    def new_login(self):
        tmpl = env.get_template('new_login.html')
        return tmpl.render(title="New Login")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=('POST'))
    def add_login(self, inputDns=None, inputEmail1=None, inputUsername=None, inputPassword=None):
        f = open('passwords.json')
        d = json.load(f)
        f.close()
        login = {"dns": inputDns, "username": inputUsername, "email": inputEmail1, "password": inputPassword}
        d.append(login)
        #d = json.dumps(d)
        with open('passwords.json', 'w') as f:
            json.dump(d, f)
            # f.write(d)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=('POST'))
    def submit_credentials(self, dns, email, password):
        #ciclo com mensagens
        
        #diffie
        #asyncio.run(startDiffieHellman())
        #hello
        valid_user_auth, SESSION_ID = asyncio.run(challenge(email, password))      
        print("AUTH: " + str(valid_user_auth))

        # if user is valid make another request to server 'username' and 'role'
        # if user is not valid redirect to login with message of authentication failure
        if not valid_user_auth:
            raise cherrypy.HTTPRedirect("/?auth_msg=Invalid+user")

        username, role = asyncio.run(auth_final_msg(SESSION_ID, email))
        print(username, role)

        #send response to challege
        raise cherrypy.HTTPRedirect("http://localhost:3000?username="+ username + "&role=" + str(role))

    
async def auth_final_msg(session_id, email):

    msg = {"type": 6, "email": email}

    async with aiohttp.ClientSession() as session:

        async with session.get('http://localhost:8080/server/login.php?PHPSESSID='+ session_id, json=msg) as resp:
            post_response = await resp.text()
            await session.close()
    response = json.loads(post_response)

    if response['type'] == 5:
        return None, None
        
    return response['username'], response['role']


async def challenge(email, password):

    hellomsg = {"type":1, "email": email}
    valid_user_auth = 1
    url = 'http://localhost:8080/server/login.php?PHPSESSID='
    SESSION_ID = ""

    async with aiohttp.ClientSession() as session:

        async with session.post(url+ SESSION_ID, json=hellomsg) as resp:
            post_response = await resp.text()
            print(post_response)
            await session.close()
    
    challenge_json = json.loads(post_response)
    print("Challenge", challenge_json)
    challenge = challenge_json['key']

    if challenge_json['type']==5:
        return 0

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

            async with session.post(url+ SESSION_ID, json=chall_resp_msg) as resp:
                post_response = await resp.text()
            
            challenge_json = json.loads(post_response)
            response_from_server = challenge_json['response']
            print("JSON FROM PHP: ", challenge_json)
            if challenge_json['type']==4:
                valid_user_auth = verify_response(uap_response, response_from_server, valid_user_auth)
                valid_user_auth = challenge_json['auth'] & valid_user_auth
                break
            else:
                challenge = challenge_json['key']
            
            # if responses dont match random responses will be sent in stead
            valid_user_auth = verify_response(uap_response, response_from_server, valid_user_auth)

            print("------------------------------------------------")
    await session.close()

    print(">>>>>>>>>>>>>>end of verification<<<<<<<<<<<")
    return valid_user_auth, SESSION_ID

def verify_response(uap_response, response_from_server, valid_user_auth):
    if (uap_response != response_from_server) and (valid_user_auth == 1):
        print("invalid user<<<<<<<<<<<<<<<<<<<")
        return 0
    return valid_user_auth

def calc_response(challenge, password):
    if isinstance(challenge, str):
        challenge = challenge.encode('utf-8')
    hashed_password = hashlib.md5(password.encode())
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32, salt=challenge, iterations=500000, backend=default_backend())
    response = kdf.derive(hashed_password.hexdigest().encode('utf-8'))

    xor_result = base64.b64encode(response)[0] & 1
    #the chosen bit is a xor of all the response bits
    for i in range(1, len(response)):
        xor_result ^= (base64.b64encode(response)[i] & 1)
    
    print(base64.b64encode(response)[0])
    print("bit challenge")
    print(xor_result)

    return xor_result


async def startDiffieHellman():
    # prime number
    P = 23
    # base
    G = 5
    
    temp_private_key = randint(2, P)
    print(temp_private_key)

    # shared key by UAP and app server
    public_key =  int(pow(G,temp_private_key, P))

    # POST request
    req_json = {'diffieHellman' : public_key}
    print(req_json)

    async with aiohttp.ClientSession() as session:

        async with session.post(url+ SESSION_ID, json=req_json) as resp:
            post_response = await resp.text()
            print(post_response)

    resp_json = json.loads(post_response)

    # uap private key
    private_key = int(pow(int(resp_json['diffieHellman']), temp_private_key, P))
    print(private_key)
    return req_json
        
# TODO: ask password
# TODO: encrypt data with password and salt

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"


if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_port': 8443,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': "cert.pem",
        'server.ssl_private_key': "privkey.pem",}
    )
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)
    
    conf = {
    '/': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
        'tools.auth_digest.key': 'a565c27146791cfb',
        'tools.auth_basic.accept_charset': 'UTF-8',
        'tools.secureheaders.on': True,
        }
    }
    
    cherrypy.quickstart(UAP(), "/", conf)