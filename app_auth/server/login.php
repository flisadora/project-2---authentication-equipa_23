<?php
include('connect.php');
session_start();
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");

    // bella.4: iLoveDobby_3
    // johny_03: AvadaKedravaBellatrix
    // lilimarta74: AvadaKedravaBellatrix88

function login($conn) {
    $res = array();
    
    // not successfull connection
    if(!successfullConn($conn)) {
        // {loggedin: false; erro: ...}
        $res["loggedin"] = false;
        $res["error"] = $conn;
        return json_encode($res);
    }
    // successfull connection
    
    // get login information
    $JSONData = file_get_contents("php://input");
    $dataObject = json_decode($JSONData);

    $email = "";
    $pass = "";

    if(isset($dataObject->email))
    {
        $email = verifyInput($dataObject->email);	// verificação do email é feita no react

    }

    if(isset($dataObject->password))
    {
        $pass = md5($dataObject->password);
    }
    
    
    if(empty($pass)) {
        // {loggedin: false; erro: ...}
        $res["loggedin"] = false;
        $res["error"] = "You must enter a password.";
        return json_encode($res);
    }
    
    // get data from database
    $sql = "SELECT * FROM users WHERE email=?";
    $stmt = mysqli_prepare($conn, $sql);

    mysqli_stmt_bind_param($stmt,'s',$email);

    mysqli_stmt_execute($stmt);

    $result = mysqli_stmt_get_result($stmt);
    $result = mysqli_fetch_assoc($result);

    // user exists
    if(isset($result["nickname"])) {
        // check if password is correct
        if($pass == $result["password"]){
            // {loggedin:true, username:...}
            $res["loggedin"] = true;
            $res["username"] = $result["nickname"];
            $res["role"] = $result["role"];
            $_SESSION["user"] = $result["nickname"];
            $_SESSION["role"] = $result["role"];
        } else {
            // {loggedin: false; erro: ...}
            $res["loggedin"] = false;
            $res["error"] = "Wrong password.";
        }
    // user doesn't exist
    } else {
        // {loggedin: false; erro: ...}
        $res["loggedin"] = false;
        $res["error"] = "Wrong email.";
    }
    
    return json_encode($res);
}

// connect to DB
$conn = connectDB();

echo login($conn);

mysqli_close($conn);
?>