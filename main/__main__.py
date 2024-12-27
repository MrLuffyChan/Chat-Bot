from web import keep_alive, web_server
from aiohttp import web

from serena import serena

import pyrogram
import asyncio

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

async def keep_online():
     await serena.invoke(pyrogram.raw.functions.account.UpdateStatus(offline=False))

async def client():
      await serena.start()
      await keep_online()
      await pyrogram.idle()
        

if __name__ == "__main__":
     loop = asyncio.get_event_loop()
     loop.run_until_complete(start_services())
     log.info('Bot Started!')
