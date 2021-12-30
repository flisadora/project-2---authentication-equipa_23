import cherrypy
from cherrypy.lib import auth_digest
import json
import requests
import asyncio
import aiohttp
#import requests_async as requests
from random import randint
from jinja2 import Environment, FileSystemLoader
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
        asyncio.run(startDiffieHellman())
        #hello
        # self.hello(email)
        # #challenge
        # self.challenge(password)
        
        

        #send response to challege
        tmpl = env.get_template('authentication.html')
        return tmpl.render()

    


    @cherrypy.expose
    def hello(self, email):
        hellomsg = json.dumps({"email": email})

        post = requests.post('http://localhost:8080/server/login.php', data = hellomsg)
        print("POST", post)

        return hellomsg
    
    @cherrypy.expose
    def challenge(self, password):
        c = 0
        password=''
        while c<len(password):
            get = requests.get('http://localhost:8080/server/login.php')
            get_json = get.json()

            # {'key': … } 
            key = get_json['key']
            # do challenge with key
            # TODO
            chall_resp = key
            chall_resp_msg = json.dumps({"response": chall_resp})

            post = requests.post('http://localhost:8080/server/login.php', data = chall_resp_msg)
            
            # c = len(password) / len(chall ??)
            c+=1      #temporary
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
        #post_request = await requests.post(url = 'http://localhost:8080/server/login.php', data = req_json)
            post_request = await resp.text()
            print(post_request)
    #json1 = post_request
    #print(post_request.url)
    #print(post_request)

    # GET request
    # get_request = requests.get('http://localhost:8080/server/login.php')
    # print("GET", get_request)
    # print(get_request.text)
    # #avg = get_request.json

    # resp_json = json.loads(get_request)
    # resp_json = resp_json['form']
    # print(resp_json)

    # uap private key
    # private_key = int(pow(int(resp_json['diffieHellman']), temp_private_key, P))
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