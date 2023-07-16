<style>header {
    background-color: orange;
    padding: 10px;
  }
  
  nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  
  nav ul li {
    display: inline;
    margin-right: 10px;
  }
  
  nav ul li a {
    text-decoration: none;
    color: #333;
    
  }
  body {
   background-color: white;
    
    background-size: cover;
  }  
  #text {
    background-color: white;
    font-size: 16px;
    text-align: center;
  }
  @keyframes slideIn {
    from {
      transform: translateY(100%);
    }
    to {
      transform: translateY(0);
    }
  }
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f1f1f1;
    color: #000;
    text-align: center;
    padding: 10px;
}

a {
            color: #1249; /* Farbe des Links auf Blau setzen */
        }
        body {
            color: white; /* Textfarbe im gesamten Dokument auf Rot setzen */
            background-color: #EC7419;
        }      
</style>

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

// Abfrage zum Abrufen aller Inhalte aus der Tabelle "tickets"
$sql = "SELECT * FROM tickets";
$result = $conn->query($sql);

// Überprüfen, ob Ergebnisse vorhanden sind
if ($result->num_rows > 0) {
    // Schleife über die Ergebnisdatensätze
    while ($row = $result->fetch_assoc()) {
        // Hier kannst du den Inhalt jedes Datensatzes anzeigen oder weitere Verarbeitungen durchführen
        echo "Ticket ID: " . $row["id"] . "<br>";
        echo "Grund: " . $row["name"] . "<br>";
        echo "name: " . $row["ticketname"] . "<br>";
        // ...
        echo "<a href=./tickets.php?id=".$row["id"].">Klicke hier, um zum Ticket zu gelangen</a> <br>"; 
        echo "<br>";
    }
} else {
    echo "Keine Tickets gefunden";
}

// Verbindung schließen
$conn->close();
?>
<a href=../index.php>Startseite</a> <br> 