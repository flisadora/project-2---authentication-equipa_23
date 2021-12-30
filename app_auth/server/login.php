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

function startDiffieHellman() {
    // prime number
    $P = 23;
    // base 
    $G = 5;
        
    $tempPrivateKey = random_int(2, $P-1);
    echo $tempPrivateKey;
    
    // shared key by UAP and app server
    $publicKey = intval(fmod(pow($G, $tempPrivateKey), $P));
    
    // POST request
    $reqObj = array("diffieHellman"=>$publicKey);
    $reqJSON = json_encode($reqObj);
    echo $reqJSON;
    
    // GET request
    $respJSON = file_get_contents("php://input");
    $resp = json_decode($respJSON);
    $respObj = $resp->form;

    // app server private key
    $privateKey = intval(fmod(pow(intval($respObj->diffieHellman), $tempPrivateKey), $P));
}

function challenge($dbpass) {
    // while ($dbpass){
    // POST request
    $key = 'challenge idk'
    $reqObj = array("key"=>$key);
    $reqJSON = json_encode($reqObj);
    echo $reqJSON;
    
    // GET request
    $respJSON = file_get_contents("php://input");
    $resp = json_decode($respJSON);
    $respObj = $resp->response;
    #do things with uap response of challenge and check if its equal to a part of $dbpass
    if (false)
        return false;
    }
    return true;
}

function login() {
    $res = array();
    
    // not successfull connection
    // if(!successfullConn($conn)) {
    //     // {loggedin: false; erro: ...}
    //     $res["loggedin"] = false;
    //     $res["error"] = $conn;
    //     return json_encode($res);
    // }
    // successfull connection
    startDiffieHellman();
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
    
    // GET request
    // $respJSON = file_get_contents("php://input");
    // $resp = json_decode($respJSON);
    // $email = $resp->email;


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
        $res = challenge($result["password"])
        // if($pass == $result["password"]){
        //     // {loggedin:true, username:...}
        //     $res["loggedin"] = true;
        //     $res["username"] = $result["nickname"];
        //     $res["role"] = $result["role"];
        //     $_SESSION["user"] = $result["nickname"];
        //     $_SESSION["role"] = $result["role"];
        // } else {
        //     // {loggedin: false; erro: ...}
        //     $res["loggedin"] = false;
        //     $res["error"] = "Wrong password.";
        // }
    // user doesn't exist
    } else {
        // {loggedin: false; erro: ...}
        $res["loggedin"] = false;
        $res["error"] = "Wrong email.";
    }
    
    return json_encode($res);
}

// connect to UAP

// connect to DB
// $conn = connectDB();

echo login();

// mysqli_close($conn);
?>