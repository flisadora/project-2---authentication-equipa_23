<?php 
include('connect.php');
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header("Content-Type: text/html; charset=utf-8");


function infoCharacter($conn) {
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

    $character = "";

    if(isset($dataObject->name)) {
        $character = $dataObject->name;
    }

    // get data from database
    $sql = "SELECT * FROM characters WHERE name=?";
    $stmt = mysqli_prepare($conn, $sql);

    mysqli_stmt_bind_param($stmt,'s',$character);

    mysqli_stmt_execute($stmt);

    $result = mysqli_stmt_get_result($stmt);
    $result = mysqli_fetch_assoc($result);
    //mysqli_stmt_num_rows

    // character exists
    if(isset($result["name"])) {
        // {name:..., photo:..., born: ..., blood_status:..., marital_status:..., nationality:..., species:...,
        // gender:..., height:..., weight:..., boggart:..., wand:..., patronus:..., occupation:..., house:..., 
        // biography:..., comments: [{nickname:...,date:...,text:...},...]}
        $res["name"] = $result["name"];
        $res["photo"] = $result["photo"];
        $res["born"] = $result["born"];
        $res["blood_status"] = $result["blood_status"];
        $res["marital_status"] = $result["marital_status"];
        $res["nationality"] = $result["nationality"];
        $res["species"] = $result["species"];
        $res["gender"] = $result["gender"];
        $res["height"] = $result["height"];
        $res["weight"] = $result["weight"];
        $res["boggart"] = $result["boggart"];
        $res["wand"] = $result["wand"];
        $res["patronus"] = $result["patronus"];
        $res["occupation"] = $result["occupation"];
        $res["house"] = $result["house"];
        $res["biography"] = $result["biography"];
        $res["comments"] = array();

        // get comments
        $sql = "SELECT * FROM comments WHERE charactere=? ORDER BY comm_date DESC";
        $stmt = mysqli_prepare($conn, $sql);

        mysqli_stmt_bind_param($stmt,'s',$character);

        mysqli_stmt_execute($stmt);

        $result = mysqli_stmt_get_result($stmt);

        while($row = mysqli_fetch_assoc($result)){
            $comment = array("nickname"=>$row["nickname"], "date"=>$row["comm_date"], "text"=>$row["text"]);
            array_push($res["comments"], $comment); 
        }

    // character doesn't exist
    } else {
        // {loggedin: false; erro: ...}
        $res["error"] = "Character doesn't exist.";
    }
    
    return json_encode($res);
}
// connect to DB
$conn = connectDB();

echo infoCharacter($conn);

mysqli_close($conn); 
?>