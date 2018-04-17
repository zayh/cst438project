<?php
  // function to add slashes to variable, ensure no SQL injections
  function AddSlash($var)
  { 
      $var=addslashes($var);
  } 

   // Calling above function for all post variables
   AddSlash($_POST);      
  
  // variables from signup form
   $firstName = $_POST['fname'];
   $lastName = $_POST['lname'];
   $userName = $_POST['username'];
   $passwd = $_POST['pass'];
  
  // Connecting to database 
    require 'db_connection.php'

  // Search to see if user already exists
  $query = "SELECT * FROM `account` WHERE `username` = '$userName'";
  $sqlsearch = mysql_query($query);
  $result = mysql_numrows($sqlsearch);

  // if user found
  if ($result > 0) {
      echo 'User already exists. Please go back and try again.';
      die(mysql_error());
    
  } else {

    mysql_query("INSERT INTO `account` (username, firstname, lastname, password) 
                               VALUES ('$userName', '$firstName', '$lastName', '$passwd') ") 
    or die(mysql_error());  

}
?>
