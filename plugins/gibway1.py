from telethon.tl.functions.channels import JoinChannelRequest as join
from telethon.tl.types import MessageMediaGiveaway as G
from telethon import events
@kanha_bot.on(events.NewMessage(func=lambda e: e.media))
async def _(event):
   if isinstance(event.media, G):
      try:
         for i in event.media.channels:
            i = await kanha_bot.get_entity(i)
            await client(join(i))
      except:
         pass