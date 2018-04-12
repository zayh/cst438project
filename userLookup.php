<?php
    if (isset($_POST['username']))
	{
            $servername = "18.222.66.236";
            $username = "webapp";
            $password = "centralSolutions123";
            $dbname = "musicproject";
        
           $dbConn new mysqli($servername, $username, $password, $dbname);
        
           if ($dbConn->connect_error) {
               die("Connection failed: " . $conn->connect_error
           }
	   
                $sql = "SELECT username
        		FROM account
        		WHERE username = :username";
        
		$stmt = $dbConn -> prepare($sql);
		$stmt -> execute(array(":username" => $_POST['username']));
		$record = $stmt->fetch();

		$output = array();

		if (empty($record))
			{
    			//echo "{\"exists\":\"true\"}";
    			$output["exists"] = "false";
			}
		else
    		{
        		//echo "Username already taken";
        		$output["exists"] = "true";
    		}
    
    	echo json_encode($output);
     }
?>
