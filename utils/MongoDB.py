from motor.motor_asyncio import AsyncIOMotorClient

def getMongoDataBase():
    return getMongoClient()["VulpoDB"]

def getMongoClient():
    return AsyncIOMotorClient('mongodb://Vulpo:wTi6sj6GW9kaabcqDBSCe28z7xnUEB@5.180.255.5:27017')