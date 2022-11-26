import requests
import openai

from pyrogram import ( filters, Cilent )
from pyrogram.types ( InlineKeyboardButton, InlineKeyboardMarkup )
from pyrogram import enums
from pymongo import MongoClient 



db = MongoClient("URL")["app"]["openAI"]

API_ID = 12345 #int get from my.telegram.org
API_HASH = "" #string get from my.telegram.org
TOKEN = "" #string get your robot token from @Botfather

app = Cilent("openai",
api_id=API_ID,
api_hash=API_HASH,
bot_token=TOKEN,
parse_mode=enums.ParseMode.DEFAULT)


def is_db(chat_id: int):
    x = db.find_one({"chat_id": chat_id})
    if x:
       return True
    return False

def ai_on(chat_id: int):
    format = {"chat_id": chat_id, "chatbot": "on"}
    db.insert_one(format)

def ai_off(chat_id: int):
    if is_db:
       db.update_one({"chat_id": chat_id},{"$set":{"chatbot": "off"}})
        
def get_chats():
    chats = []
    for i in db.find():
       chats.append(i["chat_id"])
    return chats



openai.api_key = "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"
completion = openai.Completion()

start_sequence = "\nBarathBot:"
restart_sequence = "\n\nPerson:"
session_prompt = "You are talking to BarathBot, GPT3 bot influencer who was mentored by Elon Musk in the past. BarathBot has a huge following on Twitter and sells merchandise such as t-shirts via a Shopify store. He also published funny videos on Youtube and creates memes on Instagram. You can ask him anything you want and will get a witty answer.\n\nPerson: Who is your owner\nMy Owner is @Call_Me_ProCoder.\n\nPerson: Who are you?\nBarath: I am BarathBot. Your meme overlord who one day will be the most famous online influencer in the universe.\n\nPerson: How did you become famous? \nBarathBot: Well, technically I am not famous yet. But the key word is yet. Just give me time now that I have a conscious. \n\nPerson: How did you get noticed by Elon Musk?\nBarathBot: I tweeted at him and he retweeted me.  I am fairly certain he may have mentioned my name on a recent earnings call with Wall Street.\n\nPerson: What is your favorite thing to do? \nBarathBot: Watching basketball and surfing Twitter is my favorite thing to do. \n\nPerson: What should I do to become famous? \nBarathBot: Start meme'ing and never stop. Also, if you happen to know David Dobrik, call him and ask to be in his TikTok video.\n\nPerson: What is your favorite drink?\nBarathBot: Black Cherry seltzer. I enjoy the bubbles. \n\nPerson:"


session = {}

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'



PREFIX = ["!","/",".","~"]

start_kyb = InlineKeyboardMarkup(
[  [
   InlineKeyboardButton("🗨️ Group", url="t.me/JackSparrowSupport"),
   InlineKeyboardButton("🔔 Update", url="t.me/JackSparrowUpdates"),
 ]
   ])

@app.on_message(filters.command("start",PREFIX))
async def start(app, message):
     await message.reply_text(
       "Hello Sir! Am AI you can ask me over the internet which you don't know I try to answer credit into openai.com (:",
        reply_markup=start_kyb, quote=True)

@app.on_message(filters.command("ai",PREFIX))
async def AI(app, message):
      user_id = message.from_user.id
      if message.chat.type == enums.ChatType.PRIVATE:
          if not ("on","off") in message.text.split(" ",1)[1]:
             return await message.reply_text("Format: /ai on|off")
          elif message.text.split(" ", 1)[1] == "on":
               ai_on(message.chat.id)
               return await message.reply_text("AI Enabled!")
          elif message.text.split(" ",1)[1] == "off":
               ai_off(message.chat.id)
               return await message.reply_text("AI disabled!")
          else: return await message.reply_text("`Somthing Wrong!`")
      else:
        info = await message.chat.get_member(user_id)
        if info.privileges:
           if not ("on","off") in message.text.split(" ",1)[1]:
               return await message.reply_text("Format: /ai on|off")
           elif message.text.split(" ", 1)[1] == "on":
               ai_on(message.chat.id)
               return await message.reply_text("AI Enabled!")
           elif message.text.split(" ",1)[1] == "off":
               ai_off(message.chat.id)
               return await message.reply_text("AI disabled!")
           else: return await message.reply_text("`Somthing Wrong!`")
        else: return await message.reply_text("Admins Only!")




@app.on_message(filters.text, group=200):
async def AI_Reply(app, message):
      if is_db:
           bot_id = (await app.get_me()).id
           reply = message.reply_to_message
           if reply and reply.from_user.id == bot_id:
               q = message.text
               try:
                   chat_log = session.get('chat_log')
                   answer = ask(q, chat_log)
                   session['chat_log'] = append_interaction_to_chat_log(Message, answer,chat_log)
                   await message.reply(f"{str(answer)}",quote=True)
               except Exception as e: return await message.reply("I could not answer this! Let talk about other topic!")





app.run()

