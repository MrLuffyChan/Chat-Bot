import os
import config
import pymongo
import logging
import aiohttp

from pyrogram import Client


aiohttpsession = aiohttp.ClientSession() # session

FORMAT = f"[{config.name}] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)


api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
session_string = os.getenv("string")


serena = Client(name="serena",
          api_id=api_id,
          api_hash=api_hash,
          string=session_string,
          plugins=dict(root='main'), )


connect_db = pymongo.MongoClient(config.db_url)
mongodb = connect_db['SERENA']
