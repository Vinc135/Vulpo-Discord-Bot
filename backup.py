import json
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# MongoDB-Verbindungs-URI mit der richtigen Datenbank
mongo_uri = os.getenv("mongodb_uri")

# Lade die JSON-Datei
with open('database.json') as json_file:
    database_dict = json.load(json_file)

# Für jede Tabelle im Dictionary
for table_name, table_data in database_dict.items():
    # Konvertiere die Tabellendaten in JSON-Format
    json_data = json.dumps(table_data)
    json_file_name = f'{table_name}.json'
    
    # Speichere die JSON-Daten in eine Datei
    with open(json_file_name, 'w') as file:
        file.write(json_data)
    
    # Importiere die Daten in MongoDB
    result = subprocess.run(
        ['mongoimport', '--uri', mongo_uri, '--jsonArray', '--collection', table_name, '--file', json_file_name],
        capture_output=True,
        text=True
    )
    
    # Ausgabe von Fehlern während des MongoDB-Imports
    if result.returncode != 0:
        print(f"Error importing {table_name}: {result.stderr}")
    else:
        print(f"Successfully imported {table_name}")
    
    # Lösche die temporäre JSON-Datei
    os.remove(json_file_name)

print("Import abgeschlossen.")
