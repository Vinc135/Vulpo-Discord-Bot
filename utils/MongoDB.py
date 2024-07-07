from motor.motor_asyncio import AsyncIOMotorClient

def getMongoDataBase():
    return getMongoClient()["Vulpo"]

def getMongoClient():
    return AsyncIOMotorClient('localhost', 27017)