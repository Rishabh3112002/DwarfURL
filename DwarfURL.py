from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime, timedelta
import requests

api_id = ""
api_hash = ""
token = ""

client = TelegramClient(StringSession(), api_id, api_hash)
client.start(bot_token=token)

@client.on(events.NewMessage)
async def messageHandler(event):
    now = str(datetime.now() + timedelta(hours=5,minutes=30))[0:19]
    print(now, event.message.peer_id.user_id, event.message.text)

    try:
        if event.message.text[0] == '/':
            return 
        
        if 'https://' not in event.message.text and 'http://' not in event.message.text:
            event.message.text = f'https://{event.message.text}'
          
        response = requests.post("https://rishh.onrender.com/api/url/shorten", json={'longURL': event.message.text})

        shorternUrl = response.json()['shortURL']

        user = await event.get_sender()
        await client.send_message(user, shorternUrl)
    
    except Exception as e:
        print(e)

@client.on(events.NewMessage(pattern='/start'))
async def handelNewUsers(event):
    user = await event.get_sender()
    welcomeText = "🚀 Welcome to DwarfURL! Your friendly neighborhood URL shrinking expert! ✂️\n\nTired of those long, clunky URLs cluttering up your messages? Well, fret no more! DwarfURL is here to save the day and simplify your digital life. 🎉\n\nWhether you're sharing articles, memes, or even secret messages, DwarfURL has got you covered. No more struggling with endless strings of characters. Say goodbye to link overload and hello to simplicity! 😎\n\nSo, what are you waiting for? Let's get shortening! Just send us a URL, and DwarfURL will shrink it down in a blink. Get ready to unleash the power of concise communication like never before! 💪"
    await client.send_message(user, welcomeText)
        

client.run_until_disconnected()

