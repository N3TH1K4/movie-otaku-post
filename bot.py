from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
import asyncio
from pyrogram.errors import FloodWait
import config as c
from pyromod import listen
import queriestest as q
import requests
import os

app = Client("an", bot_token=c.BOT_TOKEN, api_id=c.API_ID, api_hash=c.API_HASH)

def shorten(description, info='anilist.co'):
    description = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        description += f'_{description}_[Read More]({info})'
    else:
        description += f"_{description}_"
    return description

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]

url = 'https://graphql.anilist.co'

@app.on_message(filters.command("new"))
async def post_thing(client, message: Message):
    user_id = message.chat.id
    search_msg = await app.ask(user_id, 'Send The Name OF The anime')
    search = search_msg.text
    if len(search)<1:
        await app.send_message(user_id,"Oi Send a name and send /new again")
        return
    variables = {'search': search}
    json = requests.post(url,json={
        'query': q.anime_query,
        'variables': variables}).json()
    search = search.replace('','_')
    json = json['data']['Media']
    titleen = json['title']['english']
    titleja = json['title']['romaji']
    score = json['averageScore']
    surl = json['siteUrl']
    tyype=json['format']
    idm = json.get("id")
    dura = json['duration']
    duration = f"{dura}  Minutes Per Ep."
    cover = json['coverImage']['extraLarge']
    genres = ""
    for x in json['genres']:
            genres += f"{x}, "
    genres = genres[:-2]
    genres = genres.replace("Action", "👊Action").replace("Adventure", "🏕Adventure").replace("Comedy", "😂Comedy").replace("Drama", "💃Drama").replace("Ecchi", "😘Ecchi").replace("Fantasy", "🧚🏻‍♂️Fantasy").replace("Hentai", "🔞Hentai").replace("Horror", "👻Horror").replace("Mahou Shoujo", "🧙Mahou Shoujo").replace("Mecha", "🚀Mecha").replace("Music", "🎸Music").replace("Mystery", "🔎Mystery").replace("Psychological", "😵‍💫Psychological").replace("Romance", "❤️Romance").replace("Sci-Fi", "🤖Sci-Fi").replace("Slice of Life", "🍃Slice of Life").replace("Sports", "⚽️Sports").replace("Supernatural", "⚡️Supernatural").replace("Thriller", "😳Thriller")                                                                       
    title_img = f"https://img.anili.st/media/{idm}"
    chaid = -1001600210763
    invitel = await app.export_chat_invite_link(chaid)
    main_reply =f"""
**{titleen}** | `{titleja}` [{tyype}]

**Score:** ⭐️ {score} [Anilist]({surl})
**Duration:** {duration}
**Genres:** {genres}

© Managed By Otaku™ Network**
"""    
    
     movie_reply =f"""
**{titleen}** | `{titleja}` [{tyype}]

**Score:** ⭐️ {score} [Anilist]({surl})
**Duration:** {duration}
**Genres:** {genres}

© Managed By Otaku™ Network
"""    
    link = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="> Link <",
                        url=f"{invitel}",
                    )
                    ]])
    down = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="Download",
                        url=f"{invitel}",
                    )
                    ]])
    await app.send_message(user_id,"Preview")
    await app.send_photo(user_id,photo=cover,caption="cover img")
    await app.send_photo(user_id,photo=title_img,caption=main_reply,reply_markup=down)
    ma_msg = await app.ask(user_id, 'Should I send This To The movie Channel?\nThen send **OK**\nIf you want to cancel send **NO**')
    mai = ma_msg.text
    gmain = -1001595817253
    main_id = -1001600210763
    if "ok" in mai or "OK" in mai or "Ok" in mai:
        if user_id == 1813305809 or user_id == 1930645496 or user_id==5235061478:
            await app.send_photo(main_id,photo=title_img,caption=main_reply)
            #await app.send_sticker(main_id,"CAACAgUAAxkBAAIEHGLJScxBvcNzlS5AkEoRpqRpxu5hAAJGAAOpmuYWsYkry0a6FRAeBA")
            link = await app.ask(user_id, 'Send The Link For The Post in main!')
            invitel = link.text
            down = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="Download",
                        url=f"{invitel}",
                    )
                    ]])
            await app.send_photo(gmain,photo=title_img,caption=main_reply,reply_markup=down)
            await app.send_sticker(gmain,"CAACAgUAAxkBAAIEe2LPzdkbPBM5gZLxLfOZyPKe-rAzAAKZAAOpmuYWfOMe2DS8IdceBA")
            await app.send_message(user_id,"**Sucessfully Sent The Post to the main!**")
        else:
            await app.send_message(user_id,"**You Are Not From @Otaku_network So you cant do this**")
            return
    elif "No" in mai or "NO" in mai or "no" in mai:
        await app.send_message(user_id,"Cancellin' The Process!")
        return
    else:
        await app.send_message(user_id,"Give a valid answer!")

        
@app.on_message(filters.command("start"))
async def strt(client, message: Message):
    user_id = message.chat.id
    msgid= message.id
    print(msgid)
    link = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="> Ongoing Anime Net <",
                        url="https://t.me/OngoingAnimeNet",
                    )
                    ],
                [
                    InlineKeyboardButton(
                        text="> Main Anime Index <",
                        url="https://t.me/Otaku_Network",
                    )
                    ],
                ])
    img = "https://wallpaperaccess.com/full/5393948.jpg"
    txt = "Hello! **My name is Shinoa Hiiragi** Am a girl who can send posts like posts in **@Anime_MoviesNet**\n**Note**: This Only Works For The Admins Of Otaku Network"
    await app.send_photo(user_id,photo=img,caption=txt,reply_markup=link)

    
app.run()
print("Bot Started Successfully\n")
