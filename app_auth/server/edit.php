<?php 
include('connect.php');
session_start();
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");

function edit($conn) {
    $res = array();

    // not successfull connection
    if(!successfullConn($conn)) {
        // {success: false; error: ...}
        $res["success"] = false;
        $res["error"] = $conn;
        return json_encode($res);
    }

    // successfull connection
    if(isset($_SESSION["user"])) {
        // get charcater information 
        $JSONData = file_get_contents("php://input");
        $dataObject = json_decode($JSONData);   

        // {character: name, campo: newText} assim não é preciso ser só a biografia
        $character = $dataObject->character;
        $text = htmlspecialchars($dataObject->text);

        // update info
        $sql = "UPDATE characters SET biography=? WHERE name=?";
        $stmt = mysqli_prepare($conn, $sql);

        mysqli_stmt_bind_param($stmt,'ss',$text,$character);

        if(mysqli_stmt_execute($stmt)){
            // {success:true} no react atualizar com o texto q já têm
            $res["success"] = true;
        } else {
            // {success:false, error:}
            $res["success"] = false;
            $res["error"] = mysqli_stmt_error($stmt);
        }
    } else {
        // {success: false; error: ...}
        $res["success"] = false;
        $res["error"] = "User doesn't have permissions to edit.";
    }

    return json_encode($res);
}

// connect to DB
$conn = connectDB();

echo edit($conn);

mysqli_close($conn); 
?>