<?php

// Enable error reporting for debugging purposes (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', '1');

// Function to open the SQLite database connection
function openDatabase() {
    $db = new SQLite3('database.sqlite');
    return $db;
}

// Function to close the SQLite database connection
function closeDatabase($db) {
    $db->close();
}

// Function to remove sessionID from the users table
function removeSessionID($sessionID) {
    $db = openDatabase();

    $query = "UPDATE users SET sessionID = NULL WHERE sessionID = :sessionID";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':sessionID', $sessionID, SQLITE3_TEXT);

    $result = $stmt->execute();

    closeDatabase($db);

    return $result;
}

// Handle the logout request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Assuming you have a form field named 'sessionID'
    $sessionID = $_POST['sessionID'];

    // Check if sessionID is provided
    if (!empty($sessionID)) {
        // Remove sessionID from the users table
        $result = removeSessionID($sessionID);

        if ($result) {
            // Destroy the session
            session_start();
            session_destroy();

            echo json_encode(['success' => true, 'message' => 'Logout successful']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Error removing sessionID']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'SessionID is required']);
    }
} else {
    // Handle non-POST requests (e.g., direct access to the script)
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
