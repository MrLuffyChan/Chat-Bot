from sakura import Client
from serena.database import *
from pyrogram import filters, types, enums, errors

import config
import random
import re
import requests
import os

import pyrogram
import pymongo
import logging
import aiohttp


aiohttpsession = aiohttp.ClientSession() # session

FORMAT = f"[{config.name}] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)



serena = pyrogram.Client(
   name=config.name,
   api_id=config.api_id,
   api_hash=config.api_hash,
   session_string=config.session
)

connect_db = pymongo.MongoClient(config.db_url)
db = connect_db['SERENA']


developers = 1666544436


SERENA_MSG = [
     
     "Hi there i can't reply that question try asking again.",
     "Hello something went wrong idk.",
     "Hey idk why do you ask such thing",
     "Hmm... well idk.",
     "Please idk maybe ask other",
     
]


content= requests.get('https://litter.catbox.moe/g8nkqq').content
serena_photo = 'serena.jpeg'
with open(serena_photo, 'wb') as f:
     f.write(content)


Serena= Client(
    username = config.username,
    password = config.password,
    mongo = config.db_url
)
     

async def serena_react(message):
     try:
       await message.react(
            random.choice(
                 ['🥰', '❤️', '😁', '🗿']
            )
       )
     except:
          pass
         

async def ask_serena(chat_id, user_id, name, prompt):
     try:
        response = Serena.sendMessage(
             user_id, config.char_id, prompt
        )
        reply = response['reply']
        reply = re.sub(r'\bUser\b(?!s)', name, reply, flags=re.IGNORECASE)
     except Exception:
           print(
                   'chat_id: ',chat_id,
                   '\nUser: ', name, 
                   '\nError: ', str(Exception), 
                   '\nPrompt: ', prompt
               )
           reply = random.choice(SERENA_MSG)
           
     return reply


def admin_only(func):
     async def wrapped(client, message):
         user_id = message.from_user.id
         chat_id = message.chat.id
         if message.chat.type in (enums.ChatType.PRIVATE, enums.ChatType.BOT):
               return await func(client, message)
         else:
            try:
              user = await client.get_chat_member(chat_id, user_id)
            except errors.ChatAdminRequired:
                 return await message.reply_text(
                      "**Hello, Make me Admin to activate & deactivate assistant**"
                 )
            if user.privileges or user_id == config.serena_id or user_id in developers:
                 return await func(client, message)
     return wrapped
              

@serena.on_message((filters.text | filters.sticker | filters.animation ), group=2)
async def serena_reply(client, message):

    
    reply = message.reply_to_message
    chat_id = message.chat.id
    user = message.sender_chat if message.sender_chat else message.from_user
    name = message.sender_chat.title if message.sender_chat else message.from_user.first_name
    chatname = message.chat.title if message.chat.title else message.chat.first_name
     
    if (
    (
        (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.serena_id))
        or message.sender_chat
    )
    and message.text
    and bool(re.search('serena|cutie|@serena_ai', string=message.text, flags=re.IGNORECASE))
    ):
        
        is_serena = get_chat_mode(chat_id, chatname)
        if not is_serena:
             return
             
        await serena.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
        
        await serena_react(message)
         
        reply = await ask_serena(
               chat_id, user.id, name, message.text
        )
            
        return await message.reply_text(
              text=reply, quote=True)        
  
    elif (
    (
       (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.serena_id)) 
    or message.sender_chat
    )
  and reply 
  and reply.from_user 
  and reply.from_user.id == config.serena_id
  and message.chat.type != enums.ChatType.PRIVATE
    ):  
        
        is_serena = get_chat_mode(chat_id, chatname)
        if not is_serena:
             return
        
        if message.sticker or message.animation:
             if message.sticker:
                  if not message.sticker.file_id in get_all_stickers():
                     add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 #get_chat_stickers(chat_id) alos exsit
                 stickers = get_all_stickers()
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        
        await serena.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
         
        await serena_react(message)
         
        reply = await ask_serena(
               chat_id, user.id, name, message.text
        )
        
        return await message.reply(
             text=reply, quote=True)
        
    elif (
    (
       (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.serena_id)) 
    or message.sender_chat
    )
  and message.chat.type == enums.ChatType.PRIVATE
    ):  
        is_serena = get_chat_mode(chat_id, chatname)
        if not is_serena:
             return
             
        if message.sticker or message.animation:
             if message.sticker:
                  add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 stickers = get_all_stickers()
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        

        await serena.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)

        await serena_react(message)
         
        reply = await ask_serena(
              chat_id, user.id, name, message.text
        )
        
        return await message.reply(
             text=reply, quote=True)
        
         
@serena.on_message(filters.command('serena', prefixes=['.', '?']))
@admin_only
async def serena_mode(client, message):
  
      chat_id = message.chat.id
      
      modes = {
          'on': True,
          'off': False
      }
      if len(message.text.split()) == 2 and message.text.split()[1] in list(modes.keys()):
           key = message.text.split()[1]
           mode = modes[key]
           chatname = message.chat.title if message.chat.title else message.chat.first_name + ' Chat'
           
           set_chat_mode(
                chat_id=chat_id, 
                chatname=chatname, 
                mode=mode)
           
           mode = get_chat_mode(chat_id, chatname)
           serena = 'off'
           for k, v in modes.items():
             if v == mode:
                serena = k
                
                   
           return await message.reply(
              f'**Serena Assistant {serena.upper()} in {chatname}.**')
      else:
         return await message.reply(
            'Maybe something you did wrong, Example: `.serena on|off`')
 

@serena.on_message((filters.me|filters.user(developers)) & filters.command('chats', prefixes=['.', '?']))
async def get_serena_chats(client, message):
       chats = get_chats()
       text = '❤️ Serena Chats: {}\n'
       for i, chat in enumerate(chats[1]):
           name, chat_id, serena = chat['name'], chat['chat_id'], chat['chat']
           text += f'{i+1}, {name} - (`{chat_id}`): {serena}\n'
            
       serena_docs = 'SerenaChats.txt'
       text = text.format(len(chats))
       with open(serena_docs, 'w') as file:
           file.write(text)
           
       await message.reply_document(
            document=serena_docs, thumb=serena_photo, quote=True)
       os.remove(path)


from web import keep_alive, web_server
from aiohttp import web

BIND_ADDRESS = "0.0.0.0"
PORT = "8080"

async def start_services():        
        server = web.AppRunner(web_server())
        await server.setup()
        await web.TCPSite(server, BIND_ADDRESS, PORT).start()
        log.info("Web Server Initialized Successfully")
        log.info("=========== Service Startup Complete ===========")
  
        asyncio.create_task(keep_alive())
        log.info("Keep Alive Service Started")
        log.info("=========== Initializing Web Server ===========")
        

if __name__ == "__main__":
     loop = asyncio.get_event_loop()
     loop.run_until_complete(start_services())
     serena.run()
     log.info('Bot Started!')
