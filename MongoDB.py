from motor.motor_asyncio import AsyncIOMotorClient

def getMongoDataBase():
    return getMongoClient()["DiscordBot"]

def getMongoClient():
    return AsyncIOMotorClient('localhost', 27017)