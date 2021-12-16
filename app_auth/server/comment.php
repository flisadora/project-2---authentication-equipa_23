<?php 
include('connect.php');
session_start();
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");

function newComment($conn) {
    $res = array();

    // not successfull connection
    if(!successfullConn($conn)) {
        // {success: false; error: ...}
        $res["success"] = false;
        $res["error"] = $conn;
        return json_encode($res);
    }

    // successfull connection
    // get charcater information 
    $JSONData = file_get_contents("php://input");
    $dataObject = json_decode($JSONData); 
    
    $username = "";
    $character = "";
    $text = "";

    if(isset($dataObject->user)) {
        $username = $dataObject->user;
    }
    if(isset($dataObject->character)) {
        $character = $dataObject->character;
    }
    if(isset($dataObject->text)) {
        $text = verifyInput($dataObject->text);
    }
    
    $date = date('Y-m-d H:i:s');

    // insert new comment
    $sql = "INSERT INTO comments VALUES(?,?,?,?)";
    $stmt = mysqli_prepare($conn, $sql);

    mysqli_stmt_bind_param($stmt,'ssss',$username,$date,$text,$character);

    if(mysqli_stmt_execute($stmt)){
        // {success:true, comment:..., date:...} no react atualizar com o texto q já têm
        $res["success"] = true;
        $res["comment"] = $text;
        $res["date"] = $date;
    } else {
        // {success:false, error:...}
        $res["success"] = false;
        $res["error"] = mysqli_stmt_error($stmt);
    }
    return json_encode($res);
}

// connect to DB
$conn = connectDB();

echo newComment($conn);

mysqli_close($conn); 
?>