<?php 

// Daten über $_POST empfangen
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = $_POST['username'];
  $profilbild = $_POST['profilbild'];

}


     echo $user_data['user_name']."<br>" ;

     if ($user_data['user_name'] !== 'admin') {
        header('Location: ../index.php');
        exit();
    }

?>
<?php
$host = 'localhost';
$user = 'root';
$password = '1234';
$dbname = 'ticketss';

// Verbindung zur Datenbank herstellen
$conn = new mysqli($host, $user, $password, $dbname);

// Überprüfen, ob die Verbindung erfolgreich hergestellt wurde
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
}
// Abfrage zum Abrufen aller Einträge aus der Tabelle "tickets"
$sql = "SELECT * FROM $id";
$result = $conn->query($sql);

// Überprüfen, ob Ergebnisse vorhanden sind
if ($result->num_rows > 0) {
    // Schleife über die Ergebnisdatensätze
    while ($row = $result->fetch_assoc()) {
        // Hier kannst du den Inhalt jedes Datensatzes anzeigen oder weitere Verarbeitungen durchführen
        echo "Name: " . $row["Name"] . "<br>";
        echo "Nachricht: " . $row["message"] . "<br>";
        
        // ...
        echo "<br>";
    }
} else {
    echo "Keine Einträge gefunden";
}

// Verbindung schließen
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<?php echo '<form action="send.php?id='.$id.'" method="post">
<label for="text">Text:</label>
<input type="text" id="text" name="text" placeholder="Gebe was ein" required>
<input type="submit" value="Eingabe">'; ?>
</body>
</html>