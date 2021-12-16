<?php

function connectDB() {
    $user = 'root';
    $password = '';
    $db = 'HPWiki';
    $host = 'localhost';
    $port = '3036';
    
    $conn = mysqli_connect($host,$user,$password,$db, $port);

    // Check connection
    if (!$conn) {
        return "Connection to the database failed";
    }
    // Successfull connection
    return $conn;
}

// https://www.w3schools.com/php/php_form_validation.asp
function verifyInput($input) {
    $input = trim($input);
    $input = stripslashes($input);
    return  htmlspecialchars($input);
}

function successfullConn($conn) {
    if(is_string($conn)) {
        return false;
    }
    return true;
}

?>
