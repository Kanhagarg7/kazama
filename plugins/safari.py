from telethon import events, TelegramClient
from asyncio import sleep as zzz
from random import randint
from telethon import *
from . import *
chat = "@HeXamonbot"

# Edit the list
pokemon_list = ["Mewtwo", "Ho-oh", "Lugia", "Rayquaza", 
    "Deoxys", "Kyogre", "Jirachi", "Groudon", "Dialga", "Regigigas", "Giratina", 
    "Arceus", "Palkia", "Kyurem", "Zekrom", "Reshiram", "Latios", "Latias", 
    "Virizion", "Cobalion", "Terrakion", "Victini", "Genesect", "Meloetta", 
    "Keldeo", "Diancie", "Zygarde", "Xerneas", "Yveltal", "Volcanion", 
    "Necrozma", "Solgaleo", "Lunala", "Buzzwole", "Cosmoem", "Kartana", 
    "Cosmog", "Blacephalon", "Pheromosa", "Guzzlord", "Magearna", 
    "Marshadow", "Tapu", "Silvally", "Zacian", "Zamazenta",
    "Eternatus", "Spectrier", "Glastrier", "Urshifu", "✨","Entei","Suicune",
    "Raikou","Celebi", "Shaymin","Heatran","Hoopa",
    "Naganadel","Poipole","Cresselia","Nihilego","Xurkitree","Celesteela","Melmetal","Stakataka","Meltan","Kubfu",
    "Regidrago","Zarude","Enamorus","Beldum","Metang",
    "Koraidon", "Miraidon", "Ting-Lu", "Chien-Pao", 
    "Wo-Chien", "Shu-Tao", "Walking Wake","Aerodactyl", "Darumaka", "Abra", "Litwick", "Gardevoir", "Gallade", "Froakie", "Slakoth", "Tauros", "Wurmple", "Jolteon", "Espeon", "Drakloak", "Cincinno", "Miltank", "Vikavolt", "Cyndaquil", "Oranguru", "Heracross", "Mimikyu", "Drampa", "Rotom", "Lapras", "Druddigon", "Bouffalant", "Durant", "Meowstic", "Hawlucha", "Morpeko", "Sirfetch'd", "Morpeko", "Spiritomb"]
infomers = "@teamkanha"
hoenn = False
informer = "@princeji211"
@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.safari'))
async def autohexa(e):
    i = True
    await e.edit("safari is on the way")
    if i:
        try:
            async with kanha_bot.conversation(chat) as conv:
                await conv.send_message("/enter")
                resp = await conv.get_response(timeout=5)
                await zzz(4)
        except:
            await zzz(1, 3)
            await kanha_bot.send_message(chat, "/enter")
            await zzz(4)
    global hoenn
    hoenn = True
    x = await kanha_bot.send_message(chat, "/hunt")
    try:
        async with kanha_bot.conversation('@HeXamonbot') as conv:
            await conv.get_response(x.id)
    except:
        await zzz(1, 3)
        await kanha_bot.send_message(chat, "/hunt")

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def hunt(event):
    if hoenn == True:
        text = event.message.text
        hun = True
        message = await kanha_bot.get_messages(chat, ids=event.message.id)
        if ("lund" in text):
            kanha_bot.disconnect()
        elif ("TM" in text):
            print(event.message.text)
            await zzz(randint(1, 3))
            x = await kanha_bot.send_message(chat, "/hunt")
            try:
                async with kanha_bot.conversation('@HeXamonbot') as conv:
                    await conv.get_response(x.id)
            except:
                await zzz(1, 3)
                await kanha_bot.send_message(chat, "/hunt")
        elif any(item in text for item in pokemon_list):
            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        if button.text == "Engage":
                            await message.click(text="Engage")
                            await zzz(2)
                            await message.click(text="Engage")
                            return
                        elif button.text == "Battle":
                            await message.click(text="Battle")
                            await zzz(2)
                            await message.click(text="Battle")
                            return
        elif ("A wild" in text or "An expert" in text):
            if hun == False:
                pass
            else:
                await zzz(randint(2, 5))
                x = await kanha_bot.send_message(chat, "/hunt")
                try:
                    async with kanha_bot.conversation('@HeXamonbot') as conv:
                        await conv.get_response(x.id)
                except:
                    await zzz(1, 3)
                    await kanha_bot.send_message(chat, "/hunt")

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def hoenn(event):
    if hoenn == True:
        print(event.message.text)
        if event.message.text[:4] == "Wild":
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            await zzz(2,5)
            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        if button.text == "Throw ball":
                            await message.click(text="Throw ball")
                            await message.click(text="Throw ball")
        elif event.message.text.startswith("Battle begins!"):
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            await zzz(2)
            if event.message.buttons:
                for row in event.message.buttons:
                    for button in row:
                        if button.text == "Poke Balls":
                            await message.click(text="Poke Balls")
                            await message.click(text="Poke Balls")
@kanha_bot.on(events.MessageEdited(chats=chat))
async def cacther(event):
    global hoenn
    if hoenn == True:
        message = await kanha_bot.get_messages(chat, ids=event.message.id)
        await message.click(text="Poke Balls")
        await message.click(text="Poke Balls")
        if event.message.text[:11] == "Your Safari":
            await zzz(2,5)
            await message.click(text="Throw ball")
            await message.click(text="Throw ball")

        elif event.message.text[:4] == "Wild":
            # Fixed indentation here
            await zzz(2)
            if event.message.buttons:
                button_clicked = False 
                for row in event.message.buttons:
                    for button in row:
                        if button.text in ["Level", "Quick", "Fast", "Ultra", "Repeat"]:
                            await message.click(text=button.text)
                            button_clicked = True  # Mark that a button was clicked

        # If no specific buttons were clicked, send a message
                if not button_clicked:
                    await kanha_bot.send_message(informer, "hut bc pokeball hi koni \n \n buy krle bakchod")
                    hoenn = False

        if any(keyword in event.message.text for keyword in ['fled', 'caught']):
            # Fixed indentation here
            await zzz(2)  
            await event.click(text="Release")  
            
            await zzz(randint(4, 5))
            x = await kanha_bot.send_message(chat, "/hunt")
            try:
                async with kanha_bot.conversation('@HeXamonbot') as conv:
                    await conv.get_response(x.id)
            except:
                await zzz(1, 3)
                await kanha_bot.send_message(chat, "/hunt")
        
        if "Choose your next pokemon." in event.message.text and event.message.buttons:
            await zzz(4,5)
        
        # Define button coordinates
            buttons = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
            for x, y in buttons:
            # Get the button text
                button_text = event.buttons[x][y].text if event.buttons[x][y].text else ""
            # Check if the button has non-empty text
                if button_text.strip():  # This will check for non-empty strings
                    await event.click(x, y)  # Click the button
                    print(f"Clicked button at ({x}, {y}): {button_text}")  # Print the butt # Click the first non-empty button and exit
                else:
                    print(f"Button at ({x}, {y}) is empty or contains only spaces.")
                
@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.stop'))
async def stop(event):
    await event.edit("Stopping.....")
    global hoenn
    hoenn = False

@kanha_bot.on(events.NewMessage(chats=chat, func=lambda e: 
    ("You have run out of Safari Balls and are now exiting the Hoenn Safari Zone" in e.text or 
     "The Safari Game has finished and you were kicked out" in e.text)))
async def stoppp(event):
    global hoenn
    hoenn = False

@kanha_bot.on(events.MessageEdited(chats=chat, func=lambda e: 
    ("You have run out of Safari Balls and are now exiting the Hoenn Safari Zone" in e.text or 
     "The Safari Game has finished and you were kicked out" in e.text)))
async def stoppp(event):
    global hoenn
    hoenn = False
    
@kanha_bot.on(events.NewMessage(chats=chat))
async def infom(event):
    if hoenn == True:
        text = event.message.text
        if "✨"  in text :
            await kanha_bot.forward_messages(infomers, event.message)
            await zzz(4)
            await kanha_bot.forward_messages(informer, event.message)
        if "want to release" in text:
            await kanha_bot.forward_messages(informer, event.message)
