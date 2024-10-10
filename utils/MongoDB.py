from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# Benutzername und Passwort für die Authentifizierung

def getMongoDataBase():
    return getMongoClient()["VulpoDB"]

def getMongoClient():
    # Füge Authentifizierung zum Connection String hinzu
    connection_string = f'mongodb://{os.getenv("username")}:{os.getenv("password")}@localhost:27017/?authSource={os.getenv("auth_source")}'
    return AsyncIOMotorClient(connection_string)