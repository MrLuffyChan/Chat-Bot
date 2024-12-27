from aiohttp import web
from main import serena

import pyrogram, asyncio, aiohttp, logging, traceback

WEB_URL = "https://chat-bot-2z78.onrender.com"
WEB_SLLEP = 3*60

log = logging.getLogger(__name__)


routes = web.RouteTableDef()

@routes.get('/', allow_head=True)
async def hello(request):
    return web.Response(text="Hello, world!")


def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app




async def keep_alive():
    if WEB_URL:
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=10)
                        log.info(
                            "Pinged {} with response: {}".format(
                                WEB_URL, resp.status
                            )
                        )
                )
            except asyncio.TimeoutError:
                log.warning("Couldn't connect to the site URL..!")
            except Exception:
                traceback.print_exc()
                    

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
     loop = asyncio.new_event_loop()
     loop.run_until_complete(start_services())
     serena.run()
     log.info('Bot Started!')
