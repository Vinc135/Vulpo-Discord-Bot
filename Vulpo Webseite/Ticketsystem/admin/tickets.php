<!DOCTYPE html>
<html lang="en">
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
        <li>AdminPage ✅</li>
        <i class="bi bi-list mobile-nav-toggle"></i>
      </nav><!-- .navbar -->
     
    </div>
     
  </header>
  <section id="hero" class="d-flex align-items-center">

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
<?php echo '<form action="send.php?id='.$id.'" method="post">
<label for="text">Text:</label>
<input type="text" id="text" name="text" placeholder="Gebe was ein" required>
<input type="submit" value="Eingabe">'; ?>
</section>
</body>
</html>