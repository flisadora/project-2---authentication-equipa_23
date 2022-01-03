
<?php
//session_start();
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: *");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");


# $_REQUEST
# url
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    echo json_encode(array("url"=>"https://localhost/server/authentication.php"));
}

//echo login($conn);

// exit();
?>