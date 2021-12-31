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
import hashlib
from Crypto.Cipher import AES
env = Environment(loader=FileSystemLoader('templates'))


USERS = {'jon': 'secret'}

class UAP(object):
    @cherrypy.expose
    def index(self):
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
        
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
    def submit_credentials(self, dns, username, email, password):
        #ciclo com mensagens
        
        #diffie
        #asyncio.run(startDiffieHellman())
        #hello
        asyncio.run(challenge(email, password))
        # #challenge
        # asyncio.run(challenge(password))
        
        

        #send response to challege
        tmpl = env.get_template('authentication.html')
        return tmpl.render()

    
    

async def challenge(email, password):

    hellomsg = {"email": email}

    async with aiohttp.ClientSession() as session:

        async with session.post('http://localhost:8080/server/login.php', json=hellomsg) as resp:
            post_response = await resp.text()
            print(post_response)

    challenge_json = json.loads(post_response)
    print("Challenge", challenge_json)

    challenge = challenge_json['key']

    hashed_password = hashlib.md5(password)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32, salt=challenge.encode('utf-8'), iterations=500000,)
    response = kdf.derive(hashed_password.encode('utf-8'))
    print("HASHED PASS")
    print(hashed_password)
    #response = AES.new(key, AES.MODE_OFB)


    # while True:
    #     get = requests.get('http://localhost:8080/server/login.php')
    #     get_json = get.json()

    xor_result = response[0] & 1
    # the chosen bit is a xor of all the response bits
    for i in range(1, len(response)):
        xor_result ^= (response[i] & 1)

    chall_resp_msg = {'key':  xor_result} 

    #     key = get_json['key']
    #     # do challenge with key
    #     # TODO
    #     chall_resp = key
    #     chall_resp_msg = json.dumps({"response": chall_resp})

    post = requests.post('http://localhost:8080/server/login.php', data = chall_resp_msg)
        
    #     # c = len(password) / len(chall ??)
    #     c+=1      #temporary
    return 'Authentication Done'


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

        async with session.post('http://localhost:8080/server/login.php', json=req_json) as resp:
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