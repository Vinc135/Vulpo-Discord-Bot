<?php
// Verbindung zur Datenbank herstellen
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "ticketss";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}
echo "werden gelöscht";
// SQL-Abfrage zum Löschen aller Einträge außer der Tabelle "tickets"
$sql = "DELETE FROM tickets WHERE id != (SELECT id FROM tickets LIMIT 1)";

if ($conn->query($sql) === TRUE) {
    echo "Alle Einträge wurden erfolgreich gelöscht.";
} else {
    echo "Fehler beim Löschen der Einträge: " . $conn->error;
}

$conn->close();
?>
