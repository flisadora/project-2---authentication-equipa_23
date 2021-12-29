import cherrypy
import json

class UAP(object):
    @cherrypy.expose
    def index(self):
        f = open('passwords.json')
        passwords = json.load(f)

        choosen_credentials = 0
        r = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

            <title>This is the title of the webpage!</title>
        </head>
        <script>
            var active_tab="0";
            function saveCredentials(){
                var dns = document.getElementById("dns"+active_tab).innerHTML;
                var username = document.getElementById("username"+active_tab).innerHTML;
                var email = document.getElementById("email"+active_tab).innerHTML;
                var pw = document.getElementById("password"+active_tab).value;

                credentials(email, pw);

                var json = {"email": email, "password": pw};
                console.log(json)
                console.log(JSON.stringify(json))
                var obj =JSON.stringify(json);
            }
            function activeTab(i){
                active_tab=i;
                console.log(active_tab);
            }
        </script>
        <body>

            

            <div class="container mt-3">
                <p>This is an example paragraph. Anything in the <strong>body</strong> tag will appear on the page, just like this <strong>p</strong> tag and its contents.</p>

                <div class="row">
                    <div class="col-4">
                        <div class="list-group" id="list-tab" role="tablist">
        """
        c = ""
        for i, credentials in enumerate(passwords):
            if i == 0:
                r += """
                                <a class="list-group-item list-group-item-action active" id="list-""" + str(i) + """-list" data-toggle="list" href="#list-""" + str(i) + """"" role="tab" aria-controls="home" onclick="activeTab("""+str(i)+""")">
                                    <div class="d-flex w-100 justify-content-between">
                                        """ + credentials["dns"] + """
                                    </div>
                                    <small>""" + credentials["username"] + """</small>
                                </a>
                """
                c += """
                            <div class="tab-pane fade show active" id="list-""" + str(i) + """"" role="tabpanel" aria-labelledby="list-""" + str(i) + """"-list >
                                <div class="list-group mb-3">
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Name</small>
                                        </div>
                                        <div id="dns0">""" + credentials["dns"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Username</small>
                                        </div>
                                        <div id="username0">""" + credentials["username"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Email</small>
                                        </div>
                                        <div id="email0">""" + credentials["email"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Password</small>
                                        </div>
                                        <input type="password" class="form-control" id="password0" value=\"""" + credentials["password"] + """" readonly>
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary" onclick="saveCredentials()">Login</button>
                            </div>

                """
            else:
                r += """
                                <a class="list-group-item list-group-item-action" id="list-""" + str(i) + """-list" data-toggle="list" href="#list-""" + str(i) + """"" role="tab" aria-controls="home" onclick="activeTab("""+str(i)+""")">
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
                                        <div id="dns"""+str(i)+"""">""" + credentials["dns"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Username</small>
                                        </div>
                                        <div id="username"""+str(i)+"""">""" + credentials["username"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Email</small>
                                        </div>
                                        <div id="email"""+str(i)+"""">""" + credentials["email"] + """</div>
                                    </div>
                                    <div class="list-group-item">
                                        <div class="d-flex w-100 justify-content-between">
                                            <small>Password</small>
                                        </div>
                                        <input type="password" class="form-control" id="password""" + str(i) + """" value=\"""" + credentials["password"] + """" readonly>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-primary" onclick="saveCredentials()">Login</button>
                            </div>

                """
            
            #                 <a class="list-group-item list-group-item-action" id="list-profile-list" data-toggle="list" href="#list-profile" role="tab" aria-controls="profile">Profile</a>
            #                 <a class="list-group-item list-group-item-action" id="list-messages-list" data-toggle="list" href="#list-messages" role="tab" aria-controls="messages">Messages</a>
            #                 <a class="list-group-item list-group-item-action" id="list-settings-list" data-toggle="list" href="#list-settings" role="tab" aria-controls="settings">Settings</a>
        r += """
                        </div>
                 </div>
                 <div class="col-8">
                        <div class="tab-content" id="nav-tabContent">
        """

        r += c
            #             </div>
            #         </div>
            #         <div class="col-8">
            #             <div class="tab-content" id="nav-tabContent">
            #                 <div class="tab-pane fade show active" id="list-home" role="tabpanel" aria-labelledby="list-home-list">Email: isabella@hotmail.com</div>
            #                 <div class="tab-pane fade" id="list-profile" role="tabpanel" aria-labelledby="list-profile-list">Email: isabel@hotmail.com</div>
            #                 <div class="tab-pane fade" id="list-messages" role="tabpanel" aria-labelledby="list-messages-list">Email: isab@hotmail.com</div>
            #                 <div class="tab-pane fade" id="list-settings" role="tabpanel" aria-labelledby="list-settings-list">Email: is@hotmail.com</div>
            #             </div>
            #         </div>
            # """
        r += """
                        </div>
                    </div>
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

        # send to server

# TODO: ask password
# TODO: encrypt data with password and salt
# TODO: button to add login (como se fossemos fazer login no site original)

        return r

        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8443})
    cherrypy.quickstart(UAP())