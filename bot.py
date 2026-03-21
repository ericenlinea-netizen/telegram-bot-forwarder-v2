import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):

    # Filtrar solo canal origen
    if event.chat_id != CANAL_ORIGEN:
        return

    mensaje = event.raw_text

    if not mensaje:
        return

    print("📩 Mensaje detectado:", mensaje)

    await client.send_message(GRUPO_DESTINO, mensaje)


client.start(phone)

print("🚀 BOT INICIADO (MODO USER)")

client.run_until_disconnected()
