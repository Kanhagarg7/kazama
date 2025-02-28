# made by @moiuname < dot arc >

import asyncio
from random import choice, randrange
from re import search
import os
import time
import sys
from telethon import events
from telethon.events import NewMessage, MessageEdited
from telethon.errors import DataInvalidError, MessageNotModifiedError
from telethon.tl.custom import Message

from . import *


HEXA_ID = 572621020


async def get_response(
    chat,
    user_id,
    message,
    func=None,
    **kwargs,
):
    timeout = kwargs.pop("timeout", 60)
    reply_to = kwargs.pop("reply_to", None)
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        response = conv.wait_event(
            NewMessage(
                incoming=True,
                from_users=user_id,
                func=func,
                **kwargs,
            )
        )
        await conv.send_message(message, reply_to=reply_to)
        response = await response
        return response


async def re_fetch(m):
    return await m.client.get_messages(m.chat_id, ids=m.id)

async def watch_edits(chat, msg_id, timeout=16):
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        func = lambda e: e.id == msg_id and search(
            rf"(?i)Current turn: (.+){kanha_bot.uid}", e.message.text
        ) or "Daily limit" in e.text
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


async def main(e, other_usr):
    try:
        usr_response = await get_response(
            chat=e.chat_id,
            user_id=other_usr,
            message="/fakeChallenge",
            pattern=r"^\#ReadyforBattle$",
        )
    except asyncio.TimeoutError:
        raise TypeError("No response from 2nd ID")

    try:
        await asyncio.sleep(1)
        hexa_response = await get_response(
            chat=e.chat_id,
            user_id=HEXA_ID,
            message="/challenge",
            timeout=20,
            reply_to=usr_response.id,
        )
    except asyncio.TimeoutError:
        raise TypeError("No response from Hexa Bot!")

    try:
        await e.edit(
            f"**Challenge Sent.** \n\nWaiting to get accept!"
        )
        await asyncio.sleep(1)
    except MessageNotModifiedError:
        pass

    while True:
        response = await watch_edits(e.chat_id, hexa_response.id)
        if isinstance(response, Message):
            if "Daily limit" in response.text:
            	return "stop"
            resp = await do_click(response, 0, 0)
            if resp == True:
                return
from telethon import events
import asyncio
import asyncio
import time
from telethon import events
@kanha_cmd(pattern="hexa( (.*)|$)")
async def autohexa(e):
    chat = e.chat_id
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
                    await kanha_bot.send_message("teamkanha", "battle ruk gya")
                    return  # **Exit function if no response**
    # **Step 1: Fetch /myteam Response with Retries**
    

    if response is None or not response.buttons:
        await e.respond("⚠️ Couldn't get a valid response from `/myteam`. Stopping execution.")
        await kanha_bot.send_message("teamkanha", "battle ruk gya")
        return  # Stop execution if no valid response

    # **Step 2: Click 'Team 1' Button (Up to 5 Times)**
    team1_loaded = False

    try:
        for i in range(click_attempts):
            # Extract button list
            buttons = response.buttons
            team1_button = None

            # Find the "Team 1" button
            for row in buttons:
                for button in row:
                    if button.text == "Team 1":
                        team1_button = button
                        break
                if team1_button:
                    break

            if team1_button is None:
                print("Team 1 button not found.")  # DEBUG LOG
                await e.respond("⚠️ Couldn't find 'Team 1' button. Stopping execution.")
                await kanha_bot.send_message("teamkanha", "battle ruk gya")
                return  # **Stop execution if button is not found**

            # Click the "Team 1" button
            click_result = await team1_button.click()

            # **Check if it's an alert (BotCallbackAnswer)**
            if hasattr(click_result, "message"):
                alert_text = click_result.message  # Alert message
                print(f"Alert received: {alert_text}")  # DEBUG LOG

                # **STOP clicking if alert says "Loaded Team 1"**
                if "Loaded team 1" in alert_text:
                    print("✅ Loaded Team 1 - Stopping clicks.")  # DEBUG LOG
                    await e.respond("✅ Successfully loaded Team 1!")
                    team1_loaded = True
                    break  # **Stop clicking immediately**

            print(f"Clicked 'Team 1' button ({i+1}/{click_attempts})")  # DEBUG LOG
            await asyncio.sleep(click_delay)

    except Exception as err:
        print(f"❌ Failed to click Team 1: {err}")  # DEBUG LOG
        await e.respond("⚠️ Couldn't select Team 1. Stopping execution.")
        await kanha_bot.send_message("teamkanha", "battle ruk gya")
        return  # **Stop execution if clicking fails**

    # **If Team 1 Not Loaded, Stop Execution**
    if not team1_loaded:
        await e.respond("⚠️ Could not confirm Team 1 was loaded. Stopping execution.")
        await kanha_bot.send_message("teamkanha", "battle ruk gya")
        return  

    # **Step 3: Wait up to 30 seconds for "Successfully loaded Team 2!"**
    print("⏳ Waiting up to 30 seconds for 'Successfully loaded Team 2!'...")  # DEBUG LOG
    start_time = time.time()

    async with kanha_bot.conversation(chat, timeout=30) as conv:
        while time.time() - start_time < 30:  # Keep checking for 30 seconds
            try:
                response = await conv.wait_event(events.NewMessage(incoming=True, chats=chat), timeout=25)  # Non-blocking check
                print(f"Checking Team 2 load status: {response.text}")  # DEBUG LOG

                if "✅ Successfully loaded Team 2!" in response.text:
                    print("✅ Team 2 loaded - Proceeding with battle.")  # DEBUG LOG
                    await e.respond("✅ Successfully loaded Team 2! Starting battle...")
                    break  # **Exit loop and continue execution immediately**
            
            except asyncio.TimeoutError:
                pass  # If no response, just keep looping

            await asyncio.sleep(2)  # Wait 2 seconds before checking again

        else:  # If 30 seconds pass without finding the message
            print("⚠️ Team 2 not loaded - Stopping execution.")  # DEBUG LOG
            await e.respond("⚠️ Team 2 was not loaded within 30 seconds. Stopping execution.")
            await kanha_bot.send_message("teamkanha", "battle ruk gya")
            return  # **Stop execution**


    # **Proceed with battle**
    args = e.pattern_match.group(2)
    if not args:
        return await e.eor("`Whom should I fight with..?`", time=8)

    try:
        count, other_usr = args.split(" ", maxsplit=1)
    except Exception:
        return await e.eor("Use .hexa 5 123456789")

    try:
        count = int(count)
        if count < 0:
            raise ValueError
        count += 1
    except ValueError:
        return await e.eor("`Invalid Count..`", time=5)

    try:
        other_usr = int(other_usr)
        if other_usr < 0:
            raise ValueError
    except ValueError:
        return await e.eor("`Invalid user..`", time=5)

    domt = await e.eor(f"**Auto Battle Running for {count} times!..**")
    success = 0
    for _ in range(1, count):
        try:
            a = await main(domt, other_usr)
            if a == "stop":
                break
        except asyncio.TimeoutError:
            await domt.reply(f"Got Timeout Error.. Stopping run #{_}")
            continue
        except Exception as exc:
            LOGS.exception(exc)
            await domt.reply(f"**Got {exc.__class__} in run #{_}** \n\n`{exc}`")
            continue
        else:
            success += 1
            await domt.edit(f"__Finished run #{_}__")
        finally:
            await asyncio.sleep(6)

    await domt.edit(f"**Finished AutoHexa!\n\nFailed #{count - success} times!**")
        
