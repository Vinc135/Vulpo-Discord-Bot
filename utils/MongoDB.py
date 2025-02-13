from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# Benutzername und Passwort für die Authentifizierung

def getMongoDataBase():
    return getMongoClient()["VulpoDB"]

def getMongoClient():
    # Füge Authentifizierung zum Connection String hinzu
    connection_string = os.getenv("mongo_uri")
    return AsyncIOMotorClient(connection_string)