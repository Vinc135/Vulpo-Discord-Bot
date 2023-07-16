<?php
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "ticketss";

// Verbindung zur Datenbank herstellen
$conn = new mysqli($servername, $username, $password, $dbname);

// Überprüfen, ob die Verbindung erfolgreich hergestellt wurde
if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
}
// SQL-Befehl zum Löschen der Tabelle
$sql = "DROP TABLE IF EXISTS $id"; // "tablename" durch den Namen der zu löschenden Tabelle ersetzen

// Tabelle löschen
if ($conn->query($sql) === TRUE) {
    echo "Die Tabelle wurde erfolgreich gelöscht.";
} else {
    echo "Fehler beim Löschen der Tabelle: " . $conn->error;
}

$sqll = "DELETE FROM tickets WHERE id = ?";

// Prepared Statement erstellen
$stmt = $conn->prepare($sqll);

// Parameter binden
$stmt->bind_param("i", $id); // "i" steht für den Datentyp Integer

// Prepared Statement ausführen
if ($stmt->execute()) {
    echo "Der Eintrag wurde erfolgreich gelöscht.";
} else {
    echo "Fehler beim Löschen des Eintrags: " . $conn->error;
}

// Prepared Statement schließen
$stmt->close();
// Verbindung schließen
$conn->close();
header("Location: ./index.php");
exit;
?>






