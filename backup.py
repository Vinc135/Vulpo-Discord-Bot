import json
import os

with open('database.json') as json_file:
    database_dict = json.load(json_file)

for table_name, table_data in database_dict.items():
    json_data = json.dumps(table_data)
    json_file_name = f'{table_name}.json'
    
    with open(json_file_name, 'w') as file:
        file.write(json_data)
    
    os.system(f'mongoimport --jsonArray --db VulpoDB --collection {table_name} --file {json_file_name}')
    os.remove(json_file_name)

print("Import abgeschlossen.")