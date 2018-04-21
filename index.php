<?php
	$band_string;
	$json_string = file_get_contents('http://18.219.102.221/api/band');
	$data = json_decode($json_string, true);
	
	// Iterate through the JSON response and look for the array that contains the bands
	foreach($data as $category) {
		if (is_array($category)){
			foreach($category as $band_list){
				if (strlen($band_string) == 0) {
					$band_string = $band_string . $band_list[band_name];
				}
				else {
					$band_string = $band_string . ', ' . $band_list[band_name];
				}
				
			}
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

  <title>new_file</title>
  <meta name="description" content="">
  <meta name="author" content="Lyndsay Hackett">

  <meta name="viewport" content="width=device-width; initial-scale=1.0">

  <!-- Replace favicon.ico & apple-touch-icon.png in the root of your domain and delete these references -->
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
</head>

<body>
  <div>

	<?php echo "The following bands are in the database: " . $band_string ?>
    <br/>
	<br/>    
    
    <!-- Input for form -->
    <form action="" method="get">
      Enter a band name to be added to the database (9 characters max): <input type="text" class="userEntered"/>
	  <input type="submit" />
	</form>
	
    <p class="inputStatus"></p>
	
	<script src="EventObserver.js"></script>
	
	<p>(Note: Submitting does not actually write to db.)</p>

  </div>
</body>
</html>