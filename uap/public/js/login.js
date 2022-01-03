$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop: function() { $body.removeClass("loading"); }    
});

$(document).ready(function() {

    $("#submit-button").click(function(e) {
        data = {"user": $("input[name='user']").val(), "inputDns": $("input[name='inputDns']").val(), "inputEmail1": $("input[name='inputEmail1']").val(), "inputPassword": $("input[name='inputPassword']").val()}
        $.ajaxSetup({ 
            scriptCharset : "utf-8",
            contentType: "application/json; charset=utf-8"
        });
        $.post("/api", JSON.stringify(data))
        .done(function(response) {
            if(response.state == "success") {
                alert("Added New Login");
                window.location='/';
            } else {
                alert(response.state);
            }
        });
        e.preventDefault();
    });

    });
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