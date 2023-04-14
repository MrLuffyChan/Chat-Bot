@bot.on_message(filters.command("ban"))
async def ban(_, message):
     if not bot_stats.privileges:
         return await message.reply("**Lol! Make Me Admin When!**")
     elif not user_stats.privileges:
         return await message.reply("**You Needs Admin Rights to Control Me (~_^)!**")
     elif not bot_stats.privileges.can_restrict_members:
         return await message.reply("**I'm missing the admin rights `can_restrict_members**")
     elif not user_stats.privileges.can_restrict_members:
         return await message.reply("**You're missing the admin rights `can_restrict_members**")
         reply = message.reply_to_message
             bot.ban_chat_member(message.chat.id , reply.from_user.id)
             bot.send_message(message.chat.id ,f"Banned! {reply.from_user.mention}")
