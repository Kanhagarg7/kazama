from telethon import events , TelegramClient
from asyncio import sleep as zzz
from random import randint
from re import match

chat = "@HeXamonbot"
from . import *

#edit the list
list = ["Zacian", "Zamazenta", "Eternatus", "Spectrier", "Glastrier", "Urshifu", "✨"]


@kanha_bot.on(events.NewMessage(outgoing=True,pattern='.sgalar'))
async def autohexa(e):
    i = True
    await e.edit("galar safari is on the way")
    if i == True:
      async with kanha_bot.conversation(chat) as conv :
        await conv.send_message("/enter")
        resp = await conv.get_response(timeout=5)
        await zzz(4)
    global galar
    galar = True
    x = await kanha_bot.send_message(chat , "/hunt")
    try:  
     async with kanha_bot.conversation('@Hexamonbot') as conv:
       await conv.get_response(x.id)
    except:
       await zzz(1,3)
       await kanha_bot.send_message(chat , "/hunt")

@kanha_bot.on(events.NewMessage(chats=chat,incoming=True))
async def hunt(event):
    if galar == True:
     text = event.message.text
     hun = True
     message = await kanha_bot.get_messages(chat, ids=event.message.id)
     if ("lund" in text):
        kanha_bot.disconnect()
     elif("TM" in text):
        print(event.message.text)
        await zzz(randint(1,3))
        x = await kanha_bot.send_message(chat , "/hunt")
        try:  
         async with kanha_bot.conversation('@Hexamonbot') as conv:
           await conv.get_response(x.id)
        except:
           await zzz(1,3)
           await kanha_bot.send_message(chat , "/hunt")
     elif any(item in text for item in list):
        await message.click(text="Engage")
        await message.click(text="Engage")
        await message.click(text="Engage")
     elif("A wild" in text or "An expert" in text):
      if hun == False:
       pass
      else:
       await zzz(randint(2,5))
       x = await kanha_bot.send_message(chat , "/hunt")
       try:  
        async with kanha_bot.conversation('@Hexamonbot') as conv:
          await conv.get_response(x.id)
       except:
          await zzz(1,3)
          await kanha_bot.send_message(chat , "/hunt")
      

@kanha_bot.on(events.NewMessage(chats=chat,incoming=True))
async def galar(event):
   print(event.message.text)
   if event.message.text[:4] == "Wild":
        message = await kanha_bot.get_messages(chat, ids=event.message.id)
        await zzz(2)
        await message.click(text = "Throw ball")
        await message.click(text = "Throw ball")
        await message.click(text = "Throw ball")      


@kanha_bot.on(events.MessageEdited(chats=chat))
async def cacther(event):
   message = await kanha_bot.get_messages(chat, ids=event.message.id)
   await message.click(text = "Poke Balls")
   await message.click(text = "Poke Balls")
   await message.click(text = "Poke Balls") 
   if event.message.text[:11] == "Your Safari":
      await zzz(2)
      await message.click(text = "Throw ball")
      await message.click(text = "Throw ball")
      await message.click(text = "Throw ball")
   if any(keyword in event.message.text for keyword in ['fled', 'fainted', 'caught']):
      await zzz(randint(2,5))
      x = await kanha_bot.send_message(chat , "/hunt")
      try:  
       async with kanha_bot.conversation('@Hexamonbot') as conv:
         await conv.get_response(x.id)
      except:
         await zzz(1,3)
         await kanha_bot.send_message(chat , "/hunt")



@kanha_bot.on(events.NewMessage(outgoing=True,pattern='.stops'))
async def stop(event):
    global galar
    galar = False

@kanha_bot.on(events.NewMessage(from_users=chat,func=lambda e: "You have run out of Safari Balls and are now exiting the Galar Safari Zone" in e.text or "The Safari Game has finished and you were kicked out" in e.text))
async def stoppp(event):
   global galar
   galar = False

@kanha_bot.on(events.MessageEdited(from_users=chat,func=lambda e: "You have run out of Safari Balls and are now exiting the Galar Safari Zone" in e.text or "The Safari Game has finished and you were kicked out" in e.text))
async def stoppp(event):
   global galar
   galar = False