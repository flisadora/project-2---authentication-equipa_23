import cherrypy
from cherrypy.lib import auth_digest
import json

USERS = {'jon': 'secret'}

class UAP(object):
    @cherrypy.expose
    def index(self):
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
        # f = open('passwords.json')
        # passwords = json.load(f)
        r = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
            
            <title>This is the title of the webpage!</title>
        </head>
        <body>

            <div class="container mt-5">

                <div class="row">
                    <div class="col-4">
                        <div class="list-group" id="list-tab" role="tablist">
        """
        c = ""
        for i, credentials in enumerate(passwords):
            if i == 0:
                r += """
                                <a class="list-group-item list-group-item-action active" id="list-""" + str(i) + """-list" data-toggle="list" href="#list-""" + str(i) + """"" role="tab" aria-controls="home">
                                    <div class="d-flex w-100 justify-content-between">
                                        """ + credentials["dns"] + """
                                    </div>
                                    <small>""" + credentials["username"] + """</small>
                                </a>
                """
                c += """
                            <div class="tab-pane fade show active" id="list-""" + str(i) + """"" role="tabpanel" aria-labelledby="list-""" + str(i) + """"-list>
                                <div class="list-group mb-3">
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Name</small>
                                        </div>
                                        """ + credentials["dns"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Username</small>
                                        </div>
                                        """ + credentials["username"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Email</small>
                                        </div>
                                        """ + credentials["email"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Password</small>
                                        </div>
                                        <input type="password" class="form-control" id="exampleInputPassword1" value=\"""" + credentials["password"] + """" readonly>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-primary">Login</button>
                            </div>

                """
            else:
                r += """
                                <a class="list-group-item list-group-item-action" id="list-""" + str(i) + """-list" data-toggle="list" href="#list-""" + str(i) + """"" role="tab" aria-controls="home">
                                    <div class="d-flex w-100 justify-content-between">
                                        """ + credentials["dns"] + """
                                    </div>
                                    <small>""" + credentials["username"] + """</small>
                                </a>
                """
                c += """
                            <div class="tab-pane fade show" id="list-""" + str(i) + """"" role="tabpanel" aria-labelledby="list-""" + str(i) + """"-list>
                                <div class="list-group mb-3">
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Name</small>
                                        </div>
                                        """ + credentials["dns"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Username</small>
                                        </div>
                                        """ + credentials["username"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Email</small>
                                        </div>
                                        """ + credentials["email"] + """
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Password</small>
                                        </div>
                                        <input type="password" class="form-control" id="exampleInputPassword1" value=\"""" + credentials["password"] + """" readonly>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-primary">Login</button>
                            </div>

                """
        r += """
                        </div>
                 </div>
                 <div class="col-8">
                        <div class="tab-content" id="nav-tabContent">
        """
        r += c
        r += """
                        </div>
                    </div>
                </div>
                <div class="container d-flex flex-row-reverse p-2 mb-3 position-fixed" style="bottom: 0;">
                    <a class="btn btn-primary" href="/new_login"><i class="fas fa-plus"></i> New Login</a>
                </div>

            </div>

            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        return r

    @cherrypy.expose
    def new_login(self):
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css" integrity="sha384-AYmEC3Yw5cVb3ZcuHtOA93w35dYTsvhLPVnYs9eStHfGJvOvKxVfELGroGkvsg+p" crossorigin="anonymous"/>
            
            <title>This is the title of the webpage!</title>
        </head>
        <body>

            <div class="container mt-5">
                <form class="needs-validation" method="post" action="add_login" novalidate>
                    <div class="form-group row">
                        <label for="inputDns" class="col-sm-2 col-form-label">DNS</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" id="inputDns" name="inputDns" aria-describedby="dnsHelp" placeholder="Enter DNS" required>
                            <small id="dnsHelp" class="form-text text-muted">DNS of the website.</small>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="inputEmail1" class="col-sm-2 col-form-label">Email address</label>
                        <div class="col-sm-10">
                            <input type="email" class="form-control" id="inputEmail1" name="inputEmail1" aria-describedby="emailHelp" placeholder="Enter email" required>
                            <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="inputUsername" class="col-sm-2 col-form-label">Username</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" id="inputUsername" name="inputUsername" aria-describedby="dnsHelp" placeholder="Enter username" required>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
                        <div class="col-sm-10">
                            <input type="password" class="form-control" id="inputPassword" name="inputPassword" placeholder="Password" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                    <button href="/" class="btn btn-primary">Cancel</button>
                </form>
            </div>

            <script type="text/javascript">
            // Example starter JavaScript for disabling form submissions if there are invalid fields
            (function () {
            'use strict'

            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            var forms = document.querySelectorAll('.needs-validation')

            // Loop over them and prevent submission
            Array.prototype.slice.call(forms)
                .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    }

                    form.classList.add('was-validated')
                }, false)
                })
            })()
            </script>

            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
        </html>
        """

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
        raise cherrypy.HTTPRedirect("http://localhost:8443")
        

# TODO: ask password
# TODO: encrypt data with password and salt



if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8443})
    
    conf = {
    '/': {
        'tools.auth_digest.on': True,
        'tools.auth_digest.realm': 'localhost',
        'tools.auth_digest.get_ha1': auth_digest.get_ha1_dict_plain(USERS),
        'tools.auth_digest.key': 'a565c27146791cfb',
        'tools.auth_basic.accept_charset': 'UTF-8',
        }
    }

    cherrypy.quickstart(UAP(), "/", conf)