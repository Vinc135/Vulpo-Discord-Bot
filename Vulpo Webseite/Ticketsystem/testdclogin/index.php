<?php
$data = file_get_contents("test.py");
echo $data;  // Hallo von Python!
?>
<?php
// Daten über $_POST empfangen
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = $_POST['username'];
  $profilbild = $_POST['profilbild'];

  // Hier können Sie die erhaltenen Daten verarbeiten
  // ...

  // Beispiel-Ausgabe
  echo "Benutzername: " . $username . "<br>";
  echo "profilbild: " . $profilbild . "<br>";
}
?>