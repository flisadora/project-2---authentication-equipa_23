<?php 
include('connect.php');
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");


function deleteComment($conn) {
    $res = array();

    // not successfull connection
    if(!successfullConn($conn)) {
        // {loggedin: false; erro: ...}
        $res["loggedin"] = false;
        $res["error"] = $conn;
        return json_encode($res);
    }

    // successfull connection
    
    // get charcater information 
    $JSONData = file_get_contents("php://input");
    $dataObject = json_decode($JSONData);  
    
    $username = "";
    $date = "";

    if(isset($dataObject->username)) {
        $username = $dataObject->username;
    }

    if(isset($dataObject->date)) {
        $date = $dataObject->date;
        $date = strtotime($date);
        $date = date('Y-m-d H:i:s',$date);
    }

    // delete comment from database
    $sql = "DELETE FROM comments WHERE nickname=? AND comm_date=?";
    $stmt = mysqli_prepare($conn, $sql);

    mysqli_stmt_bind_param($stmt,'ss',$username,$date);
    
    mysqli_stmt_execute($stmt);

    if(mysqli_stmt_execute($stmt)) {
        // {deleted: true}
        $res["deleted"] = true;
    } else {
        // {deleted: false}
        $res["deleted"] = false;
    }
    
    return json_encode($res);
}
// connect to DB
$conn = connectDB();

echo deleteComment($conn);

mysqli_close($conn); 
?>