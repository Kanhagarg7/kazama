from telethon.tl.functions.channels import JoinChannelRequest
from telethon import events
from . import kanha_bot  # Assuming kanha_bot is defined in your module

@kanha_bot.on(events.NewMessage(func=lambda e: e.media is not None and hasattr(e.media, 'channels')))
async def join_channels(event):
    channels = event.media.channels
    try:
        for channel in channels:
            channel_entity = await kanha_bot.get_entity(channel)  # Use kanha_bot to get the entity
            await kanha_bot(JoinChannelRequest(channel_entity))
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
