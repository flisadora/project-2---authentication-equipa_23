import cherrypy
from cherrypy.lib import auth_digest
import json
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

        #hello
        hellomsg = {"email": email}
        hellomsg = json.dumps(hellomsg)

        #send response to challege
        
        return hellomsg
        

        # send to server

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