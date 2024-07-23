from motor.motor_asyncio import AsyncIOMotorClient

def getMongoDataBase():
    return getMongoClient()["VulpoDB"]

def getMongoClient():
    return AsyncIOMotorClient('localhost', 27017)