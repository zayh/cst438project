<?php

	session_start();

	if (isset($_POST['username'])){
	//put db connection here
	require '';
	
	$sql = "SELECT *
			FROM account
			WHERE username = :username
			AND password = :password";

	$stmt = $dbConn -> prepare($sql);
	$stmt -> execute(array(":username" => $_POST['username'], ":password" => hash("sha1", $_POST['password'])));

	$record = $stmt -> fetch();

	if (empty($record)){
		echo "Wrong username/password!";
	} else {
		$_SESSION['username'] = $record['username'];
		$_SESSION['name'] = $record['firstname'] . " " . $record['lastname'];
		header("Location: index.php");
	}
}

?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">

		<!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame
		Remove this if you use the .htaccess -->
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

		<title>Log In</title>
		<meta name="viewport" content="width=device-width; initial-scale=1.0">

		<!-- Replace favicon.ico & apple-touch-icon.png in the root of your domain and delete these references -->
		<link rel="shortcut icon" href="/favicon.ico">
		<link rel="apple-touch-icon" href="/apple-touch-icon.png">
		
		<style>
			#wrapper{
				margin:auto;
				border: thin black solid;
				text-align: center;
				width: 300px;
				height: 300px;
				overflow: auto;
			}
			body{
				background-color: #D8D0CF;
			}
		</style>

	</head>

	<body>
		<div id="wrapper">
			<h2>Music Website</h2>
			<h2>Log In</h2>
			<form method="post">
				Username: <input type="text" name="username" /><br />
				<p></p>
				Password: <input type="password" name="password" /><br />
				<p></p>
				<input type="submit" value="Login" />
				<p></p>
			</form>
			<form method="post" action="/signup.html">
				Don't have an account?&nbsp;&nbsp;<input type="submit" value="Sign Up" />
			</form>
		</div>
	</body>
</html>
