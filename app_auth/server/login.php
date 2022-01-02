
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
include('connect.php');
session_start();
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: *");
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
    //echo $tempPrivateKey;
    
    // shared key by UAP and app server
    $publicKey = intval(fmod(pow($G, $tempPrivateKey), $P));
    
    // GET request
    $respJSON = file_get_contents("php://input");
    $resp = json_decode($respJSON);
    $respObj = $resp->diffieHellman;

    // app server private key
    $privateKey = intval(fmod(pow(intval($respObj), $tempPrivateKey), $P));
    
    // POST request
    $reqObj = array("diffieHellman"=>$publicKey);
    $reqJSON = json_encode($reqObj);
    echo $reqJSON;
    
    
}


function hello($email, $conn) {
    

    
}

function challenge($dbpass) {
    // while ($dbpass){
    // POST request
    $key = utf8_encode(base64_encode(openssl_random_pseudo_bytes(16)));   
    // $reqObj = array("key"=>$key, "generated_key"=>base64_encode($generated_key), "xor"=>$xor_result);
    // $reqJSON = json_encode($reqObj);
    // echo $reqJSON;

    //$hashed_pass = md5(utf8_encode($dbpass));
    $hashed_pass = md5(utf8_encode("iLoveDobby_3"));
    $algo = "sha256";
    $salt = utf8_encode($key);
    $iterations = 500000;
    $len = 32;
    $binary = True;

    // // $binarydata = "\x02\xae\x0b\xdf\xe8\x84_\x85";
    // // $array = unpack("cchars/nint", $binarydata);
    // // print_r($array);
    // // echo "<br>";

    $generated_key = hash_pbkdf2($algo, $hashed_pass, $salt, $iterations, $len, $binary);
    
    $xor_result = ord(base64_encode($generated_key)[0]) & 1;
    
    for ($i = 1; $i < strlen($generated_key) ; $i++) {
        $xor_result = (ord(base64_encode($generated_key)[$i]) & 1) ^ ($xor_result);
    }
    
    $reqObj = array("key"=>$key, "generated_key"=>base64_encode($generated_key), "xor"=>$xor_result, "response0"=> ord(base64_encode($generated_key)[0]));
    $reqJSON = json_encode($reqObj);
    echo $reqJSON;
    return $xor_result;
    
    // GET request
    // $respJSON = file_get_contents("php://input");
    // $resp = json_decode($respJSON);
    // $respObj = $resp->response;
    
    // #do things with uap response of challenge and check if its equal to a part of $dbpass
    // if (false){
    //     return false;
    // }
    // return true;
}

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
    //$result_challenge = "";

    if(isset($dataObject->diffieHellman))
    {
        startDiffieHellman();	// verificação do email é feita no react
        
    }

    if(isset($dataObject->email))
    {

    	$email = $dataObject->email;

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
            $pass = $result["password"];
            // $result_challenge = challenge($pass);

            challenge($pass);

        }else {
            // user doesn't exist
            echo json_encode(array("resp"=>'Wrong email.'));
        }

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
    

    
    return json_encode($res);
}

// connect to UAP

// connect to DB
$conn = connectDB();

login($conn);
//echo login($conn);

mysqli_close($conn);
?>