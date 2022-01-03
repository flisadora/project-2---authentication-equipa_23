$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop: function() { $body.removeClass("loading"); }    
});

(function(credentials){
$.fn.get_logins = function(credentials) {
    res_login = "";
    res_info = "";
    for(i = 0; i < credentials.length; i++) {
        if (i == 0) {
            res_login += "<a class=\"list-group-item list-group-item-action active\" id=\"list-" + i + "-list\" data-toggle=\"list\" href=\"#list-" + i + "\" role=\"tab\" aria-controls=\"" + i + "\">";
            res_info += "<div class=\"tab-pane fade show active\" id=\"list-" + i +"\" role=\"tabpanel\" aria-labelledby=\"list-" + i +"-list\">";
        } else {
            res_login += "<a class=\"list-group-item list-group-item-action\" id=\"list-" + i + "-list\" data-toggle=\"list\" href=\"#list-" + i + "\" role=\"tab\" aria-controls=\"" + i + "\">";
            res_info += "<div class=\"tab-pane fade show\" id=\"list-" + i +"\" role=\"tabpanel\" aria-labelledby=\"list-" + i +"-list\">";
        }
        res_login += "<div class=\"d-flex w-100 justify-content-between\">" + 
                            credentials[i].dns + " \
                        </div> \
                        <small>" + credentials[i].email + "</small> \
                        </a>";
        res_info += "<form class=\"myform\" method=\"post\" action=\"submit_credentials\"> \
                <div class=\"list-group mb-3\"> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Name</small> \
                    </div> " + 
                    credentials[i].dns + " \
                    <input id = \"dns\" type=\"hidden\" name=\"dns\" value=" + credentials[i]["dns"] +" readonly> \
                </div> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Email</small> \
                    </div> " + 
                    credentials[i].email + " \
                    <input id = \"email\" type=\"hidden\" name=\"email\" value=" + credentials[i]["email"] + " readonly> \
                </div> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Password</small> \
                    </div> \
                    <input type=\"password\" class=\"form-control\" name=\"password\" id=\"exampleInputPassword1\" value=\"" + credentials[i].password + "\" readonly> \
                </div> \
            </div> \
            <button type=\"submit\" class=\"btn btn-primary\" onclick=\"showProtocol()\">Login</button> \
            </form> \
        </div>";
    }
    return [res_login, res_info];
}; 
})();

$(document).ready(function() {
    $.ajaxSetup({ 
        scriptCharset : "utf-8",
        contentType: "application/json; charset=utf-8"
    });
    $.get("/api")
    .done(function(response) {
        r = $.fn.get_logins(response);
        $("#list-tab").html(r[0]);
        $("#nav-tabContent").html(r[1]);
    });
    $("#myform").on("submit", function(){
        $("#pageloader").fadeIn();
      });//submit
});

function showProtocol(){
    alert("Wait a few moments until we check if your credentials are valid.\nWe are running an E-CHAP security protocol");
}