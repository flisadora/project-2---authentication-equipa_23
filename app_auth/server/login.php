
<?php
//session_start();
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
include('connect.php');
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: *");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");

    // bella.4: iLoveDobby_3
    // johny_03: AvadaKedravaBellatrix
    // lilimarta74: AvadaKedravaBellatrix88

    /*
        post message types:
        1. hello
        2. challenge
        3. challenge + response
        4. end of auth
        5. msg error
        6. username + role
        7. response username + role
    */

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

function challenge($dbpass) {
    $key = utf8_encode(base64_encode(openssl_random_pseudo_bytes(16)));   
   
    $xor_result = calc_response($key, $dbpass);

    return array($xor_result[0], $key, $xor_result[1]);
}

function calc_response($key, $password) {
    $hashed_pass = $password;
    $algo = "sha256";
    $salt = utf8_encode($key);
    $iterations = 500000;
    $len = 32;
    $binary = True;

    $generated_key = hash_pbkdf2($algo, $hashed_pass, $salt, $iterations, $len, $binary);
    
    $xor_result = ord(base64_encode($generated_key)[0]) & 1;
    
    for ($i = 1; $i < strlen($generated_key) ; $i++) {
        $xor_result = (ord(base64_encode($generated_key)[$i]) & 1) ^ ($xor_result);
    }

    return array($xor_result, ord(base64_encode($generated_key)[0]));
}

function login($conn) {
    $res = array();
    // not successfull connection
    if(!successfullConn($conn)) {
        // {loggedin: false; erro: ...}
        $res['loggedin'] = false;
        $res['error'] = $conn;
        return json_encode($res);
    }
    // successfull connection
    
    // get login information
    $JSONData = file_get_contents("php://input");
    $dataObject = json_decode($JSONData);

    $email = "";
    $n = 4;

    if(isset($dataObject->type))
    {
        switch ($dataObject->type) {
            case 1:
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
                    if(isset($result['nickname'])) {
                        // check if password is correct
                        session_start();
                        $_SESSION['pass'] = $result['password'];
                        $_SESSION['n'] = 0;
                        $_SESSION['valid_user_auth'] = True;
                        $array = challenge($_SESSION['pass']);
                        $_SESSION['result_challenge'] = $array[0];
                        $key = $array[1];
                        
                        $reqObj = array("type"=>2,"key"=>$key, "session_id"=>session_id(), "inteiro"=>$array[2]);
                        $reqJSON = json_encode($reqObj);
                        echo $reqJSON;
                    }else {
                        // user doesn't exist
                        echo json_encode(array("type"=>5,"key"=>'wrong email'));
                    }
            
                }
                break;
            case 3:
                if(isset($dataObject->key ) && isset($dataObject->response))
                {
                    $key = $dataObject->key;
                    $response = $dataObject->response;
                    $url_components = parse_url($_SERVER['REQUEST_URI']);
                    parse_str($url_components['query'], $params);
                    session_id($params['PHPSESSID']);
                    session_start();

                    if($_SESSION['n'] < $n){
                        $_SESSION['n']+=1;
                        $reqObj = "";
                        if(($_SESSION['result_challenge'] == $response) && $_SESSION['valid_user_auth']) {
                            if($_SESSION['n'] == ($n)){

                                $array_calcresponse = calc_response($key, $_SESSION['pass']);


                                $reqObj = array("type"=>4,"response"=>$array_calcresponse[0], "auth"=>$_SESSION['valid_user_auth'], "inteiro"=>$array_calcresponse[1], "session"=> $_SESSION['n']);
                            }
                            else {
                                $array = challenge($_SESSION['pass']);
                                $_SESSION['result_challenge'] = $array[0];
                                $challenge = $array[1];

                                $array_calcresponse = calc_response($key, $_SESSION['pass']);

                                $reqObj = array("type"=>3, "key"=>$challenge, "response"=>$array_calcresponse[0], "inteiro"=>$array_calcresponse[1], "session"=> $_SESSION['n']);
                            }   
                        }
                        else {
                            if($_SESSION['n'] == ($n)){
                                $reqObj = array("type"=>4, "response"=>calc_response($key, $_SESSION['pass'])[0], "auth"=>$_SESSION['valid_user_auth']);
                            }
                            else {
                                $_SESSION['valid_user_auth'] = FALSE;
                                $rand_num = utf8_encode(base64_encode(openssl_random_pseudo_bytes(32)));
                                $_SESSION['result_challenge'] = ord(base64_encode($rand_num)[0]) & 1;
                                $reqObj = array("type"=>3, "key"=>$rand_num, "response"=>calc_response($key, $_SESSION['pass'])[0], "session"=> $_SESSION['n']);
                            }
                        }
                        $reqJSON = json_encode($reqObj);
                        echo $reqJSON;
                    }
                }
                break;
            case 6:
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
                    if(isset($result['nickname'])) {
                        $url_components = parse_url($_SERVER['REQUEST_URI']);
                        parse_str($url_components['query'], $params);
                        session_id($params['PHPSESSID']);
                        session_start();
                        
                        $reqObj = array("type"=>7,"username"=>$result['nickname'], "role"=>$result['role']);
                        $reqJSON = json_encode($reqObj);
                        echo $reqJSON;
                    }else {
                        // user doesn't exist
                        echo json_encode(array("type"=>5,"key"=>"username or role not found"));
                    }
            
                }
                break;
        }
        
    }

    
    // GET request
    // $respJSON = file_get_contents("php://input");
    // $resp = json_decode($respJSON);
    // $email = $resp->email;
    
    return json_encode($res);
}

// connect to UAP

// connect to DB
$conn = connectDB();

login($conn);
//echo login($conn);

mysqli_close($conn);
exit();
?>