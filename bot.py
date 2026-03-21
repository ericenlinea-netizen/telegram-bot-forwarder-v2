import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

canal_origen = int(os.getenv("CANAL_ORIGEN"))
grupo_destino = int(os.getenv("GRUPO_DESTINO"))

bot = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(chats=canal_origen))
async def handler(event):
    mensaje = event.message.text

    if not mensaje:
        return

    print("📩 Mensaje recibido:", mensaje)

    await bot.send_message(grupo_destino, mensaje)

print("🚀 BOT INICIADO CORRECTAMENTE")

bot.run_until_disconnected()
