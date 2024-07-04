from motor.motor_asyncio import AsyncIOMotorClient
import time

start = time.time()
for i in range(1000000):
    print(i)
    collection = AsyncIOMotorClient('localhost', 27017).get_database("test")["test"]
    collection.insert_one({'test': f'test{i}'})
   
#print(f'Insert 5000 documents in {time.time() - start} seconds')

#start = time.time()
#collection.find_one({'test': 'test60357'})
#print(f'Find one document in {time.time() - start} seconds')

