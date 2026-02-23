import os
import sys
import time
import asyncio
from random import randrange
from re import search
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.custom import Message
from telethon import TelegramClient
from telethon import events
from . import *
import os
import sys
import asyncio

@kanha_cmd(pattern="r$", fullsudo=True)
async def restart(event):
    await event.edit("🔄 Restarting...")

    await asyncio.sleep(1)

    # Clean restart using module mode
    os.execv(
        sys.executable,
        [sys.executable, "-m", "pykanha"]
    )
