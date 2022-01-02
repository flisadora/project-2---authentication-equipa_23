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
        res_info += "<div class=\"list-group mb-3\"> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Name</small> \
                    </div> " + 
                    credentials[i].dns + " \
                </div> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Email</small> \
                    </div> " + 
                    credentials[i].email + " \
                </div> \
                <div class=\"list-group-item\"> \
                    <div class=\"d-flex w-100 justify-content-between\"> \
                        <small>Password</small> \
                    </div> \
                    <input type=\"password\" class=\"form-control\" id=\"exampleInputPassword1\" value=\"" + credentials[i].password + "\" readonly> \
                </div> \
            </div> \
            <button type=\"button\" class=\"btn btn-primary\">Login</button> \
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
});