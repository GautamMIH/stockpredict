<?php

// SQLite database connection details
$databaseFile1 = 'C:\Users\grim\Desktop\stockpredict\prototype3\outputdatabase\predictionslstm.db';
$databaseFile2 = 'C:\Users\grim\Desktop\stockpredict\prototype3\outputdatabase\predictionssma.db';

// Define weights for each symbol
$symbolWeights = [
    'LICN' => ['db1' => 0.99, 'db2' => 0.01],
    'NLIC' => ['db1' => 0.49, 'db2' => 0.53],
    'NLICL' => ['db1' => 0.73, 'db2' => 0.25],
    'SJLIC' => ['db1' => 0.92, 'db2' => 0.02],
    'ALICL' => ['db1' => 0.45, 'db2' => 0.55],
    'HLI' => ['db1' => 0.02, 'db2' => 0.97],
    'ILI' => ['db1' => 0.72, 'db2' => 0.25],
    'CLI' => ['db1' => 0, 'db2' => 1],
    'PMLI' => ['db1' => 0, 'db2' => 1],
    'RNLI' => ['db1' => 0, 'db2' => 1],
    'SNLI' => ['db1' => 0, 'db2' => 1],
    'SRLI' => ['db1' => 0, 'db2' => 1],
    // Add more symbols and their respective weights as needed
];

// Create database connections
$conn1 = new SQLite3($databaseFile1);
$conn2 = new SQLite3($databaseFile2);

// Check the connections
if (!$conn1 || !$conn2) {
    die("Connection failed: " . $conn1->lastErrorMsg() . " " . $conn2->lastErrorMsg());
}

// Function to determine color based on LTP values
function determineColor($weightedAverage, $csvLtp) {
    if ($weightedAverage > $csvLtp) {
        return 'Green';
    } else {
        return 'Red';
    }
}

// Fetch data from the databases (replace 'your_table' with your actual table name)
$sql1 = "SELECT symbol, Ltp FROM predicted_values";
$result1 = $conn1->query($sql1);

$sql2 = "SELECT symbol, ltp FROM predictions";
$result2 = $conn2->query($sql2);

// Array to store weighted averages for each symbol
$weightedAverages = array();

// Process data from the first database
if ($result1) {
    while ($row = $result1->fetchArray(SQLITE3_ASSOC)) {
        $symbol = $row['symbol'];
        $ltp1 = $row['Ltp'];

        // Multiply LTP by the corresponding weight
        $weightedAverages[$symbol] = $ltp1 * $symbolWeights[$symbol]['db1'];
    }
}

// Process data from the second database
if ($result2) {
    while ($row = $result2->fetchArray(SQLITE3_ASSOC)) {
        $symbol = $row['symbol'];
        $ltp2 = $row['ltp'];

        // Multiply LTP by the corresponding weight and add to the existing weighted average
        $weightedAverages[$symbol] += $ltp2 * $symbolWeights[$symbol]['db2'];
    }
}

// Loop through each symbol and compare with CSV
foreach ($weightedAverages as $symbol => $weightedAverage) {
    // Read the CSV file for the symbol (replace 'path/to/your/csv' with the actual path)
    $csvFileName = "C:/Users/grim/Desktop/stockpredict/{$symbol}.csv";
    // $csvData = file($csvFileName);
    // $lastCsvLtp = end($csvData); 
    
    $csvData = array_map('str_getcsv', file($csvFileName));
    $lastCsvLtp = end($csvData)[4];// Assuming the last line contains the latest LTP value

    // Determine the color
    $color = determineColor($weightedAverage, $lastCsvLtp);

    // Output the result
    echo "Symbol: $symbol, Weighted Average: $weightedAverage, CSV LTP: $lastCsvLtp, Color: $color<br>";
}

// Close the database connections
$conn1->close();
$conn2->close();

?>
