<?php

// Read JSON data from file
$jsonData = file_get_contents('buyingbroker.json');

// Set headers to indicate JSON content
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Output JSON data
echo $jsonData;
?>
