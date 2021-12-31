
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
    $key = 'challenge idk';
    $reqObj = array("key"=>$key);
    $reqJSON = json_encode($reqObj);
    echo $reqJSON;
    
    // GET request
    $respJSON = file_get_contents("php://input");
    $resp = json_decode($respJSON);
    $respObj = $resp->response;
    #do things with uap response of challenge and check if its equal to a part of $dbpass
    if (false){
        return false;
    }
    return true;
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
		$challenge = 'axdf';
		echo json_encode(array("key"=>$challenge));
		$pass = $result["password"];
		//TODO calcular challenge + calcular resposta
	}else {
		// user doesn't exist
		echo json_encode(array("resp"=>'Wrong email.'));
	}
	//
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