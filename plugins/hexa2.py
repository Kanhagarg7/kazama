
import asyncio
from random import choice, randrange
from re import search
from telethon import TelegramClient, events
from telethon.events import NewMessage, MessageEdited
from telethon.errors import DataInvalidError, MessageNotModifiedError
from telethon.tl.custom import Message

from . import *
HEXA_ID = 572621020


async def re_fetch(m):
    return await m.client.get_messages(m.chat_id, ids=m.id)


async def watch_edits(chat, msg_id, timeout=20):
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        func = lambda e: e.id == msg_id and search(rf"(?i)Current turn: (.+){kanha_bot.uid}", e.message.text)
        response = conv.wait_event(
            MessageEdited(
                incoming=True,
                from_users=HEXA_ID,
                func=func,
            )
        )
        response = await response
        await asyncio.sleep(3)
        response = await re_fetch(response)
        return response


# try clicking button 3 times in background. (2s delay)
async def do_click(msg, *buttons):
    async def _click():
        try:
            await msg.click(*buttons)
        except DataInvalidError:
            pass

    async def _loop():
        nonlocal msg
        for _ in range(3):
            await asyncio.sleep(2)
            r_msg = await re_fetch(msg)
            if r_msg and r_msg.buttons and r_msg.text == msg.text:
                await _click()
                msg = r_msg
            else:
                return

    await _click()
    asyncio.create_task(_loop())


# clicks ready button
async def get_ready(chat):
    async with kanha_bot.conversation(chat, timeout=16) as conv:
        response = conv.wait_event(
            NewMessage(incoming=True, from_users=HEXA_ID, func=lambda e: e.mentioned)
        )
        response = await response
        if response.buttons and response.buttons[0][0].text.startswith("Ready"):
            await asyncio.sleep(3)
            await do_click(response, 0, 0)
            await asyncio.sleep(3)
            return response.id


# clicks button b/w (2-6)
async def click_rnd_button(msg):
    for count1, sub_buttons in enumerate(msg.buttons):
        for count2, button in enumerate(sub_buttons):
            text = str(button.text).strip()
            if text and text.isdigit():
                return await do_click(msg, count1, count2)


# click (attack) if dodged or missed otherwise pokemon -> 2 to 6
async def auto_battle(chat, msg_id):
    response = await watch_edits(chat, msg_id, timeout=15)
    await asyncio.sleep(2)
    if not response.buttons:
        return True
    elif "team" in response.buttons[0][0].text.lower():
        return await click_rnd_button(response)
    else:
        if 'missed' in response.raw_text:
            await do_click(response, 0, 0)
            return 
        if 'dodged' in response.raw_text:
            await do_click(response, 0, 0)
            return
@kanha_bot.on(
    NewMessage(
        incoming=True,
        pattern="^/fakeChallenge$",
        from_users=udB.get_key("SUDOS"),
    )
)
async def autohemxa(e):
    await asyncio.sleep(1)
    msg = await e.reply("#ReadyforBattle")
    try:
        hexa_msg_id = await get_ready(e.chat_id)
        await msg.delete()
        while True:
            response = await auto_battle(e.chat_id, hexa_msg_id)
            # await asyncio.sleep(0.3)
            if response == True:
                return
    except asyncio.TimeoutError:
        return await msg.respond("Timeout Error.. Skipping!")
    except Exception as exc:
        LOGS.exception(exc)
        await msg.respond(f"**2nd ID Error** \n\nGot {exc.__class__} \n`{exc}`")

from telethon import events
import asyncio

@kanha_bot.on(events.NewMessage(incoming=True))
async def x(event):
    chat = "HeXamonbot"

    if "✅ Successfully loaded Team 1!" in event.raw_text:
        retries = 3  # Max retries for /myteam
        delay = 5  # Delay between retries
        click_attempts = 5  # Click button up to 5 times
        click_delay = 4  # Delay between clicks

        response = None
        # Notify user

        # **Step 1: Fetch /myteam Response**
        for attempt in range(retries):
            async with kanha_bot.conversation(chat, timeout=20) as conv:
                try:
                    await conv.send_message("/myteam")
                    print(f"Attempt {attempt+1}: Sent /myteam")  # DEBUG LOG

                    response = await conv.get_response(timeout=10)
                    print(f"Response received: {response.text}")  # DEBUG LOG

                    if response.buttons:
                        break  # **Valid response received, stop retrying**
                    else:
                        print("No buttons found, retrying...")  # DEBUG LOG
                        await asyncio.sleep(delay)

                except asyncio.TimeoutError:
                    print("Timeout: No response received")  # DEBUG LOG
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
                    else:
                        await event.respond("⚠️ Bot did not respond after multiple attempts. Try again later.")
                        return  # **Exit function if no response**

        if response is None:
            return  # Stop if no response

        # **Step 2: Click 'Team 2' Button up to 5 Times**
        final_response = None
      # Notify user

        try:
            for i in range(click_attempts):
                # Extract button list
                buttons = response.buttons
                team2_button = None

                # Find the "Team 2" button
                for row in buttons:
                    for button in row:
                        if button.text == "Team 2":
                            team2_button = button
                            break
                    if team2_button:
                        break

                if team2_button is None:
                    print("Team 2 button not found.")  # DEBUG LOG
                    await event.respond("⚠️ Couldn't find 'Team 2' button. Try manually.")
                    return

                # Click the "Team 2" button
                click_result = await team2_button.click()

                # **Check if it's an alert (BotCallbackAnswer)**
                if hasattr(click_result, "message"):
                    alert_text = click_result.message  # Alert message
                    print(f"Alert received: {alert_text}")  # DEBUG LOG
                  # Send alert to user

                    # **Stop clicking if alert says "Loaded Team 2"**
                    if "Loaded team 2" in alert_text:
                        print("✅ Loaded Team 2 - Stopping clicks.")  # DEBUG LOG
                        await event.respond("✅ Successfully loaded Team 2!")
                        break  # **Stop clicking**

                print(f"Clicked 'Team 2' button ({i+1}/{click_attempts})")  # DEBUG LOG
                await asyncio.sleep(click_delay)

            # **Wait for the final response from the bot**
            final_response = await kanha_bot.get_messages(chat, limit=1)

        except Exception as e:
            print(f"❌ Failed to click Team 2: {e}")  # DEBUG LOG
            await event.respond("⚠️ Couldn't select Team 2. Try manually.")
            return

        # **Step 3: Send Final Response to the Original Chat**
        if final_response:
            await event.respond(final_response[0].text)
            print("✅ Sent final response to original chat")  # DEBUG LOG
