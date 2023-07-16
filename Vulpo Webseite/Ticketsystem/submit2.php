
<?php /*
 // Verbindung zur Datenbank herstellen
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "test";


$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}

// Formulardaten verarbeiten und in die Datenbank einfügen
$name = $_POST['reson'];
// $email = $_POST['email'];
$ticketname = "testt";

$sql = "INSERT INTO temm (name, email) VALUES ('$name', '$ticketname')";

if ($conn->query($sql) === TRUE) {
    echo "Formulardaten wurden erfolgreich in die Datenbank eingefügt.";
} else {
    echo "Fehler beim Einfügen der Formulardaten: " . $conn->error;
}

$conn->close(); */
/*
// Verbindung zur Datenbank herstellen
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "tickets";


$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}

// Formulardaten verarbeiten und in die Datenbank einfügen
$msg = $_POST['text'];
// $email = $_POST['email'];
$name = "testt";
function generateRandomID($length) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomID = '';
    for ($i = 0; $i < $length; $i++) {
        $randomID .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomID;
}

$minLength = 10;
$maxLength = 30;
$randomIDLength = rand($minLength, $maxLength);

$randomID = generateRandomID($randomIDLength);
if (isset($_POST['inhalt'])) {
    $inhalt = $_POST['inhalt'];
}

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
}

$sql = "INSERT INTO $id (Name, message, id) VALUES ('$name', '$msg', '$randomID')";

if ($conn->query($sql) === TRUE) {
    echo "Formulardaten wurden erfolgreich in die Datenbank eingefügt.";
} else {
    echo "Fehler beim Einfügen der Formulardaten: " . $conn->error;
}



/*$sql = "CREATE TABLE $randomID (
    Name VARCHAR(255),
    message VARCHAR(255),
    id VARCHAR(255)

)"; */ /*

if ($conn->query($sql) === TRUE) {
    echo "Die Tabelle tickettt wurde erfolgreich erstellt.";
} else {
    echo "Fehler beim Erstellen der Tabelle: " . $conn->error;
}

$conn->close();
header("Location: ./");
exit; */

$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "ticketss";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}

$msg = $_POST['text'];


// Daten über $_POST empfangen
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = $_POST['username'];
  $profilbild = $_POST['profilbild'];

}

$servername = "localhost";
    $username = "root";
    $password = "1234";
    $dbname = "login";
    
    
    $connn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
    }
	$user_data = check_login($connn);

$name = $user_data['user_name'];

function generateRandomID($length) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomID = '';
    for ($i = 0; $i < $length; $i++) {
        $randomID .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomID;
}

$minLength = 10;
$maxLength = 30;
$randomIDLength = rand($minLength, $maxLength);

$randomID = generateRandomID($randomIDLength);

if (isset($_GET['id'])) {
    $id = $_GET['id'];
} else {
    echo "Es wurde keine 'id' übergeben.";
}

$sql = "INSERT INTO $id (Name, message, id) VALUES ('$name', '$msg', '$randomID')";

if ($conn->query($sql) === TRUE) {
    echo "Formulardaten wurden erfolgreich in die Datenbank eingefügt.";
} else {
    echo "Fehler beim Einfügen der Formulardaten: " . $conn->error;
}

$conn->close();
header("Location: ./tickets.php?id=".$id);

exit;
?>


