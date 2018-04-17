<?php        
        $servername = "18.222.66.236";
        $username = "webapp";
        $password = "centralSolutions123";
        $dbname = "musicproject";
        
        $dbConn new mysqli($servername, $username, $password, $dbname);
        
        if ($dbConn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
?>
