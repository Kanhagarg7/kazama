from . import *
import asyncio
from telethon import TelegramClient, events
import re
from telethon.tl.functions.channels import GetFullChannelRequest

@kanha_cmd(pattern='pd')
async def pd(e):
    chat = -1001737654150  # Target chat where Poke Dollars will be sent
    pinchat = -1001737654150  # Pinned chat for reference
    a = await e.client(GetFullChannelRequest(pinchat))
    pinmsg = a.full_chat.pinned_msg_id  # Get pinned message ID
    
    async with e.client.conversation(chat) as conv:
        await conv.send_message('/myinventory')
        try:
            a = await conv.get_response(timeout=8)
            if 'Poke Dollars' in a.text:
                # Extract Poke Dollars amount
                amount = re.search(r'💵: (\d+)', a.text)
                if amount:
                    amount = int(amount.group(1))
                    
                    # Keep 300 Poke Dollars in inventory, send the rest
                    if amount > 300:
                        send_amount = amount - 300
                    else:
                        send_amount = 0
                    
                    if send_amount > 0:
                        await asyncio.sleep(3)
                        await e.client.send_message(pinchat, f'/give {send_amount}', reply_to=pinmsg)
                    else:
                        await e.edit('Not enough Poke Dollars to send, keeping 300.')
        except asyncio.TimeoutError:
            await e.edit('Bot not responding')
