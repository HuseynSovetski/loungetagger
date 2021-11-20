import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("7685796"))
api_hash = os.environ.get("95a3612e4e76fda494ea2728a66a375f")
bot_token = os.environ.get("2135440852:AAFQjPkH0YferlTPgJSvjBP211kYqOK9AcM")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**DBMtagbot**, Salam,Men qrup ve kanallarda bütün üzvleri tağ ede bilecek botam.★\nDaha çox melumat üçün **/help**'i basın.",
                    buttons=(
                      [Button.url('🔗 Meni qrupa elave et', 'https://t.me/loungetaggerbot?startgroup=a'),
                      Button.url('📍 DBMresmi', 'https://t.me/DBMresmi'),
                      Button.url('⚜️ Sahibim', 'https://t.me/DBMBOSSdu')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**DBMtagbot bot'un Kömek menyusuna xoş geldiniz**\n\nKomanda: /tag \n  Bu komandanı, başqalarını tağ etmek istediyiniz metinle birlikde istifade ede bilersiniz. \n`Misal: /all Sabahınız xeyir!`  \nBu komandanı yanıt olaraq istifade ede bilersiniz

  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Meni qrupa elave et', 'https://t.me/loungetaggerbot?startgroup=a'),
                       Button.url('📣 DBMresmi', 'https://t.me/DBMresmi'),
                      Button.url('🚀 Sahibim', 'https://t.me/DBMBOSSdu')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/tag ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu komanda qruplarda ve kanallarda istifade edile biler.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Yalnız adminler hamını tağ ede biler!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Evvelki mesajlar üçün üzvlerden behs elemerem! (qrupa elave etmeden evvel gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Mene tag sebibini yaz!__")
  else:
    return await event.respond("__Bir mesaja yanıt verin veya başqalarından behs elememem üçün mene metn ver!__")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ müveffeqiyyetle dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tağ müveffeqiyyetle dayandırıldı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot çalıyor merak etme 🚀 @loungesupport bilgi alabilirsin <<")
client.run_until_disconnected()
