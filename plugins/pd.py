from . import *
import asyncio
from telethon import TelegramClient, events
import re
from telethon.tl.functions.channels import GetFullChannelRequest

@kanha_cmd(pattern='pd')
async def pd(e):
    chat = -1001737654150  # Chat where Poke Dollars will be checked
    pinchat = -1001737654150  # Chat where Poke Dollars will be sent
    retries = 3  # Reduced retries for better stability
    give_retries = 3  
    delay = 5  # Reduced delay to speed up retries

    # Get pinned message ID
    a = await e.client(GetFullChannelRequest(pinchat))
    pinmsg = a.full_chat.pinned_msg_id  

    send_amount = 0  

    # **Step 1: Fetch Poke Dollars using /myinventory with retries**
    for attempt in range(retries):
        async with e.client.conversation(chat, timeout=20) as conv:  # Open a NEW conversation per attempt
            try:
                await conv.send_message('/myinventory@HeXamonbot')
                print(f"Attempt {attempt+1}: Sent /myinventory")  # DEBUG LOG

                response1 = await conv.get_response(timeout=15)  # Increased timeout
                print(f"Response received: {response1.text}")  # DEBUG LOG

               

                # **Ensure response is a reply to /myinventory**
                if response1.reply_to and response1.reply_to.reply_to_msg_id:
                    amount_match = re.search(r'Poke Dollars 💵: (\d+)', response1.text)
                    if amount_match:
                        amount = int(amount_match.group(1))
                        send_amount = max(0, amount - 300)

                        if send_amount > 0:
                            print(f"Poke Dollars: {amount}, Sending: {send_amount}")  # DEBUG LOG
                            break  # **STOP RETRYING**
                        else:
                            await e.edit('Not enough Poke Dollars to send, keeping 300.')
                            return  

            except asyncio.TimeoutError:
                print("Timeout: No response received")  # DEBUG LOG
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    await e.edit('Bot not responding after multiple attempts.')
                    return  

    # **STOP RETRYING IF RESPONSE RECEIVED**
    if send_amount == 0:
        print("No valid response, exiting")  # DEBUG LOG
        return  

    # **Step 2: Try sending /give with retries**
    for give_attempt in range(give_retries):
        async with e.client.conversation(chat, timeout=20) as conv:  # New conversation for /give
            try:
                await conv.send_message(f'/give {send_amount}', reply_to=pinmsg)
                print(f"Attempt {give_attempt+1}: Sent /give {send_amount}")  # DEBUG LOG

                response2 = await conv.get_response(timeout=10)
                print(f"Response received for /give: {response2.text}")  # DEBUG LOG

                # **Ensure response is a reply to /give**
                if response2.reply_to and response2.reply_to.reply_to_msg_id:
                    if "Poke Dollars sent" in response2.text:
                        await e.edit(f'Successfully sent {send_amount} Poke Dollars! ✅')
                        return  # **STOP RETRYING after success**
                    else:
                        print("Retrying /give...")  # DEBUG LOG
                        await asyncio.sleep(delay)
                        continue  

            except asyncio.TimeoutError:
                print("Timeout: No response for /give")  # DEBUG LOG
                if give_attempt < give_retries - 1:
                    await asyncio.sleep(delay)
                else:
                    await e.edit("Poke Dollars transfer failed: No confirmation received.")
                    return  
