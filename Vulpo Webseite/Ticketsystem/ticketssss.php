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

// SQL-Abfrage zum Abrufen der Einträge mit der E-Mail-Adresse "test"
$email = "testt";
$sql = "SELECT * FROM temm WHERE email = '$email'";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Ausgabe der Einträge
    while ($row = $result->fetch_assoc()) {
        echo "Name: " . $row["name"] . "<br>";
        echo "E-Mail: " . $row["email"] . "<br>";
        echo "<br>";
    }
} else {
    echo "Keine Einträge gefunden.";
}

$conn->close(); */



// Verbindung zur Datenbank herstellen
if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
}
$neuerInhalt = $id;
echo '<div id="e">' . $neuerInhalt . '</div>';

$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "ticketss";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Verbindung zur Datenbank fehlgeschlagen: " . $conn->connect_error);
}

// SQL-Abfrage zum Abrufen der Einträge mit der E-Mail-Adresse "test"
$email = "testt";
$sql = "SELECT * FROM $id /* WHERE ticketname = '$email' */";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Ausgabe der Einträge
    while ($row = $result->fetch_assoc()) {
        echo "------------------------------------------------------------- <br>";
        echo "Name: " . $row["Name"] . "<br>";
        echo "Nachricht: " . $row["message"] . "<br>";
        
    }
} else {
    echo "Keine Einträge gefunden, Starte die unterhaltung";
} /*
session_start();

include("../login/connection.php");
include("../login/functions.php");
$user_data = check_login($con);
*/
if (isset($_GET['id'])) {
    $id2 = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
} /*
$sql = "SELECT ticketname FROM $id WHERE ticketname = '".$user_data['user_name']."'";

// SQL-Abfrage ausführen
$result = $conn->query($sql);

// Überprüfen, ob die Abfrage ein Ergebnis zurückgegeben hat
if ($result->num_rows > 0) {
    
} else {
    
    header("Location: ./index.php");
} */
$conn->close();

echo '<form action="submit2.php?id='.$id.'" method="post">
<label for="text">Text:</label>
<input type="text" id="text" name="text" placeholder="Gebe was ein" required>
<input type="submit" value="Eingabe">';



echo '<a href="close.php?id=' . $id2 . '"><u>Klicke hier, um zu schließen</u></a>';



?>
<!DOCTYPE html>
<html lang="en">
<head>
  <script type="text/javascript" charset="UTF-8" async="" src="https://consent.cookiebot.com/Scripts/widgetIcon.min.js"></script><script type="text/javascript" charset="UTF-8" async="" src="https://consentcdn.cookiebot.com/consentconfig/4201f56a-66a9-4e81-b252-16665dafb20b/state.js"></script><script id="Cookiebot" src="https://consent.cookiebot.com/uc.js" data-cbid="4201f56a-66a9-4e81-b252-16665dafb20b" data-blockingmode="auto" type="text/javascript"></script><style type="text/css" id="CookieConsentStateDisplayStyles">.cookieconsent-optin,.cookieconsent-optin-preferences,.cookieconsent-optin-statistics,.cookieconsent-optin-marketing{display:block;display:initial;}.cookieconsent-optout-preferences,.cookieconsent-optout-statistics,.cookieconsent-optout-marketing,.cookieconsent-optout{display:none;}</style>

  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>Vulpo - Beste Lösung für deinen Discord Server</title>
  <meta content="Vulpo ist ein vielseitiger Deutscher Discord Bot, der deinen Server sehr gut verwalten kann." name="description">
  <meta content="discord, bot, discord bot, bester discord bot, deutscher discord bot, economy, levelsystem, gewinnspiele, stats, vulpo premium, premium, günstig, free, gratis" name="keywords">

  <!-- Favicons -->
  <link href="https://vulpo-bot.de/static/assets/img/favicon.webp" rel="icon">
  <link href="https://vulpo-bot.de/static/assets/img/apple-touch-icon.webp" rel="apple-touch-icon">

  <!-- Vendor CSS Files -->
  <link href="https://vulpo-bot.de/static/assets/vendor/aos/aos.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/bootstrap-icons/bootstrap-icons.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/remixicon/remixicon.css" rel="stylesheet">
  <link href="https://vulpo-bot.de/static/assets/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">
  
  <!-- Template Main CSS File -->
  <link href="https://vulpo-bot.de/static/assets/css/style.css" rel="stylesheet">
  <title>test</title>

  <!-- =======================================================
  * Template Name: Arsha
  * Updated: Mar 10 2023 with Bootstrap v5.2.3
  * Template URL: https://bootstrapmade.com/arsha-free-bootstrap-html-template-corporate/
  * Author: BootstrapMade.com
  * License: https://bootstrapmade.com/license/
  ======================================================== -->


  <!-- =======================================================
  * Template Name: Arsha
  * Updated: Mar 10 2023 with Bootstrap v5.2.3
  * Template URL: https://bootstrapmade.com/arsha-free-bootstrap-html-template-corporate/
  * Author: BootstrapMade.com
  * License: https://bootstrapmade.com/license/
  ======================================================== -->
</head>
    

<body>







<header id="header" class="fixed-top">
    <div class="container d-flex align-items-center">
      <h1 class="logo me-auto"><a href="static/assets/img/favicon.webp">Vulpo</a></h1>
      <a class="logo me-auto"><img src="static/assets/img/favicon.webp" alt="" class="img-fluid"></a>

      <nav id="navbar" class="navbar">
        <ul>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#hero">Hauptseite</a></li>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#about">Über Vulpo</a></li>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#services">Funktionen</a></li>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#portfolio">Galerie</a></li>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#team">Team</a></li>
          <li><a class="nav-link scrollto active" href="https://vulpo-bot.de/ticket">Ticketsystem</a></li>
          
          <li class="dropdown"><a href="#"><span>Premium</span> <i class="bi bi-chevron-down"></i></a>
            <ul>
              <li><a href="https://vulpo-bot.de/premium">Mehr Informationen</a></li>
              <li><a href="https://vulpo-bot.de/login">Mit Discord einloggen &amp; kaufen</a></li>
            </ul>
          </li>
          <li><a class="nav-link scrollto" href="https://vulpo-bot.de/#contact">Kontakt</a></li>
          <li><a class="getstarted scrollto" href="https://vulpo-bot.de/invite">Einladen</a></li>
        </ul>
        <i class="bi bi-list mobile-nav-toggle"></i>
      </nav><!-- .navbar -->

    </div>
  </header>
  <br>
  <br>




























    <script>
    // Den Inhalt des HTML-Elements auslesen
    var divInhalt = document.getElementById("e").innerHTML;

    // Den Inhalt an PHP übergeben
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "submit2.php", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("inhalt=" + encodeURIComponent(divInhalt));
    </script>    
</body>
</html>
<?php
// Verbindung zur Datenbank herstellen
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "ticketss";

$conn = new mysqli($servername, $username, $password, $dbname);

// Überprüfen, ob die Verbindung erfolgreich hergestellt wurde
if ($conn->connect_error) {
    die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}
if (isset($_GET['id'])) {
    $id2 = $_GET['id'];
    
} else {
    echo "Es wurde keine 'id' übergeben.";
}

// Daten über $_POST empfangen
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = $_POST['username'];
  $profilbild = $_POST['profilbild'];

}

// SQL-Abfrage erstellen
$sql = "SELECT ticketname FROM `tickets` WHERE ticketname = '".$user_data['user_name']."' AND id = '$id2'";



// SQL-Abfrage ausführen
$result = $conn->query($sql);

// Überprüfen, ob die Abfrage ein Ergebnis zurückgegeben hat
if ($result->num_rows > 0) {
    
} else {
    header("Location: ./index.php");
}

// Verbindung zur Datenbank schließen
$conn->close();
?>