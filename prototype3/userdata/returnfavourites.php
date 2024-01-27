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

// Function to get favorite symbols for a user
function getFavorites($userID) {
    $db = openDatabase();

    $query = "SELECT favourite FROM user_favourites WHERE UserID = :userID";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':userID', $userID, SQLITE3_INTEGER);

    $result = $stmt->execute();

    $favorites = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $favorites[] = $row['favourite'];
    }

    closeDatabase($db);

    return $favorites;
}

// Function to get UserID from sessionID
function getUserIDFromSessionID($sessionID) {
    $db = openDatabase();

    $query = "SELECT UserID FROM users WHERE sessionID = :sessionID";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':sessionID', $sessionID, SQLITE3_TEXT);

    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    closeDatabase($db);

    return $user ? $user['UserID'] : null;
}

// Handle the return favorites request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Assuming you have a form field named 'sessionID'
    $sessionID = $_POST['sessionID'];

    // Check if sessionID is provided
    if (!empty($sessionID)) {
        // Get UserID from sessionID
        $userID = getUserIDFromSessionID($sessionID);

        if ($userID !== null) {
            // Get favorite symbols for the user
            $favorites = getFavorites($userID);

            echo json_encode(['success' => true, 'favorites' => $favorites]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid sessionID']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'SessionID is required']);
    }
} else {
    // Handle non-POST requests (e.g., direct access to the script)
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
