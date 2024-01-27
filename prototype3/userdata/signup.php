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

// Function to create the users table if it doesn't exist
function createUsersTable() {
    $db = openDatabase();

    $query = "CREATE TABLE IF NOT EXISTS users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        sessionID TEXT
    )";

    $db->exec($query);

    closeDatabase($db);
}

// Function to create a new user
function createUser($email, $password) {
    $db = openDatabase();

    // Hash the password using MD5 (not recommended for production)
    $hashedPassword = md5($password);

    // Insert user into the database
    $query = "INSERT INTO users (email, password) VALUES (:email, :password)";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $stmt->bindValue(':password', $hashedPassword, SQLITE3_TEXT);

    $result = $stmt->execute();

    closeDatabase($db);

    return $result;
}

// Check if the users table exists, create it if not
createUsersTable();

// Handle the signup request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Assuming you have form fields named 'email' and 'password'
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Check if email and password are provided
    if (!empty($email) && !empty($password)) {
        // Create a new user
        $result = createUser($email, $password);

        if ($result) {
            echo json_encode(['success' => true, 'message' => 'User registered successfully']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Error registering user']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'Email and password are required']);
    }
} else {
    // Handle non-POST requests (e.g., direct access to the script)
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}
?>
