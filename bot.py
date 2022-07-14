from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client, filters
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
    channel_id_msg = await app.ask(user_id, 'Please Add Me To The Channel And Send The `Channel ID`')
    channel_id = int(channel_id_msg.text)
    #print(channel_id)
    chaid = channel_id
    search_msg = await app.ask(user_id, 'Send The Name OF The anime')
    search = search_msg.text
    variables = {'search': search}
    json = requests.post(url,json={
        'query': q.anime_query,
        'variables': variables}).json()
    search = search.replace('','_')
    json = json['data']['Media']
    titleen = json['title']['english']
    titleja = json['title']['romaji']
    score = json['source']
    surl = json['siteUrl']
    tyype=json['format']
    idm = json.get("id")
    duration = f"{json.get('duration', 'N/A')} Minutes Per Ep."
    genres = ""
    for x in json['genres']:
            genres += f"{x}, "
    genres = genres[:-2]
    is_hd_msg = await app.ask(user_id, 'Is it **720p** or **1080p**?')
    hd = is_hd_msg.text
    invitel = await app.export_chat_invite_link(chaid)
    title_img = f"https://img.anili.st/media/{idm}"
    final_reply =f"""
**{titleen}** | `{titleja}` [{tyype}]

**Score:** ⭐️ {score} [Anilist]({surl})
**Duration:** {duration}
**Genres:** {genres}

♻️ {hd} SUB

Main Index: ||@Ongoinganimenet||
Powered By: **@Otaku_Network**
"""
    link = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        text="> Link <",
                        url=f"{invitel}",
                    )
                    ]])
    #print(invitel)
    await app.send_photo(chaid,photo=title_img,caption=final_reply,reply_markup=link)
app.run()
print("Bot Started Successfully\n")
