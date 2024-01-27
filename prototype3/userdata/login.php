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

// Function to authenticate the user and create a session
function authenticateUser($email, $password) {
    $db = openDatabase();

    // Hash the provided password for comparison
    $hashedPassword = md5($password);

    // Check if the user exists with the given credentials
    $query = "SELECT UserID FROM users WHERE email = :email AND password = :password";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $stmt->bindValue(':password', $hashedPassword, SQLITE3_TEXT);

    $result = $stmt->execute();
    $user = $result->fetchArray(SQLITE3_ASSOC);

    if ($user) {
        // Generate a session ID and update it in the database
        $sessionID = md5(uniqid(rand(), true));

        $updateQuery = "UPDATE users SET sessionID = :sessionID WHERE UserID = :userID";
        $updateStmt = $db->prepare($updateQuery);
        $updateStmt->bindValue(':sessionID', $sessionID, SQLITE3_TEXT);
        $updateStmt->bindValue(':userID', $user['UserID'], SQLITE3_INTEGER);

        $updateStmt->execute();

        closeDatabase($db);

        return $sessionID;
    } else {
        closeDatabase($db);
        return false; // Invalid credentials
    }
}


// Handle the login request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Assuming you have form fields named 'email' and 'password'
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Check if email and password are provided
    if (!empty($email) && !empty($password)) {
        // Authenticate the user
        $sessionID = authenticateUser($email, $password);

        if ($sessionID) {
            // Set the session ID as a cookie and respond with success
            setcookie('sessionID', $sessionID, time() + 3600, "/"); // Adjust the expiration time as needed
            echo json_encode(['success' => true, 'message' => 'Login successful', 'session_id'=> $sessionID]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid email or password']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'Email and password are required']);
    }
} else {
    // Handle non-POST requests (e.g., direct access to the script)
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
