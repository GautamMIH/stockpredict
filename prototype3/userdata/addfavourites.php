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

// Function to create the user_favourites table if it doesn't exist
function createUserFavouritesTable() {
    $db = openDatabase();

    $query = "CREATE TABLE IF NOT EXISTS user_favourites (
        UserID INTEGER,
        favourite TEXT,
        FOREIGN KEY (UserID) REFERENCES users(UserID)
    )";

    $db->exec($query);

    closeDatabase($db);
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

// Function to add a favorite for a user
function addFavorite($userID, $symbol) {
    $db = openDatabase();

    $query = "INSERT INTO user_favourites (UserID, favourite) VALUES (:userID, :symbol)";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':userID', $userID, SQLITE3_INTEGER);
    $stmt->bindValue(':symbol', $symbol, SQLITE3_TEXT);

    $result = $stmt->execute();

    closeDatabase($db);

    return $result;
}

// Check if the user_favourites table exists, create it if not
createUserFavouritesTable();

// Handle the add favorites request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Assuming you have form fields named 'sessionID' and 'symbol'
    $sessionID = $_POST['sessionID'];
    $symbol = $_POST['symbol'];

    // Check if sessionID and symbol are provided
    if (!empty($sessionID) && !empty($symbol)) {
        // Get UserID from sessionID
        $userID = getUserIDFromSessionID($sessionID);

        if ($userID !== null) {
            // Add favorite for the user
            $result = addFavorite($userID, $symbol);

            if ($result) {
                echo json_encode(['success' => true, 'message' => 'Favorite added successfully']);
            } else {
                echo json_encode(['success' => false, 'message' => 'Error adding favorite']);
            }
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid sessionID']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'SessionID and symbol are required']);
    }
} else {
    // Handle non-POST requests (e.g., direct access to the script)
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
