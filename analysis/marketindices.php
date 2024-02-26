<?php
$json_file_path = 'jsondata/marketindices.json';


if (file_exists($json_file_path)) {
    // Read the contents of the JSON file
    $njson_data = file_get_contents($json_file_path);
    $json_data = strip_tags($njson_data);

    // Check if data was successfully read
    if ($json_data !== false) {
        // Output the JSON data to the frontend
        header('Content-Type: application/json');
        echo $json_data;
    } else {
        // If reading failed, display an error message
        echo 'Error reading JSON file';
    }
} else {
    // If the file does not exist, display an error message
    echo 'JSON file not found';
}

?>