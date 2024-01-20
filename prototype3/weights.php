<?php

// Function to calculate the predicted value based on weights
function calculatePredictedValue($weightLSTM, $weightSMA, $symbol, $actualLtp) {
    // Database connection details
    $databaseLSTM = new SQLite3('C:\Users\grim\Desktop\stockpredict\prototype3\outputdatabase\predictionslstm.db');
    $databaseSMA = new SQLite3('C:\Users\grim\Desktop\stockpredict\prototype3\outputdatabase\predictionssma.db');

    // Fetch LTP values from databases
    $sqlLSTM = "SELECT ltp FROM predicted_values WHERE symbol = '$symbol'";
    $resultLSTM = $databaseLSTM->query($sqlLSTM);
    $ltpLSTM = $resultLSTM->fetchArray()['Ltp'];

    $sqlSMA = "SELECT ltp FROM predictions WHERE symbol = '$symbol'";
    $resultSMA = $databaseSMA->query($sqlSMA);
    $ltpSMA = $resultSMA->fetchArray()['ltp'];

    // Calculate the predicted value based on weights
    $predictedValue = $weightLSTM * $ltpLSTM + $weightSMA * $ltpSMA;

    // Return the difference between predicted and actual values
    return abs($predictedValue - $actualLtp);
}

// Specify the symbol and actual LTP value
$symbol = 'LICN';
$actualLtp = 1424; // Replace with your actual LTP value

// Set the range of weights you want to try
$minWeight = 0;
$maxWeight = 1;
$step = 0.01;

// Initialize variables for best weights and minimum difference
$bestWeightLSTM = $bestWeightSMA = 0;
$minDifference = PHP_INT_MAX;

// Loop through different weights
for ($weightLSTM = $minWeight; $weightLSTM <= $maxWeight; $weightLSTM += $step) {
    for ($weightSMA = $minWeight; $weightSMA <= $maxWeight; $weightSMA += $step) {
        // Calculate the difference between predicted and actual values
        $difference = calculatePredictedValue($weightLSTM, $weightSMA, $symbol, $actualLtp);

        // Update best weights if the current difference is smaller
        if ($difference < $minDifference) {
            $bestWeightLSTM = $weightLSTM;
            $bestWeightSMA = $weightSMA;
            $minDifference = $difference;
        }
    }
}

// Output the best weights
echo "Best Weights - LSTM: $bestWeightLSTM, SMA: $bestWeightSMA\n";
