from telethon.tl.functions.channels import JoinChannelRequest
from telethon import *
@kanha_bot.on(events.NewMessage(func=lambda e: e.media.channels))
async def _(event):
   a = event.media.channels
   try:
      for i in a:
         i = await client.get_entity(i)
         await client(JoinChannelRequest(i))
   except:
      pass