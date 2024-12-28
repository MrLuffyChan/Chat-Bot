import pyrogram
import config
import pymongo
import logging
import aiohttp


aiohttpsession = aiohttp.ClientSession() # session

FORMAT = f"[{config.name}] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)



serena = pyrogram.Client(
   name=config.name,
   api_id=api_id,
   api_hash=api_hash,
   session=session,
   plugins=dict(root='main')
)

connect_db = pymongo.MongoClient(config.db_url)
mongodb = connect_db['SERENA']
