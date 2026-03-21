import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

# Fix event loop (Railway / Python moderno)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient('session', api_id, api_hash)


@client.on(events.NewMessage)
async def handler(event):
    try:
        if event.chat_id != CANAL_ORIGEN:
            return

        mensaje = event.raw_text

        if not mensaje:
            return

        print("📩 Mensaje detectado:", mensaje)

        await client.send_message(GRUPO_DESTINO, mensaje)

    except Exception as e:
        print("❌ Error:", e)


async def main():
    await client.start()  # ya usa session, NO pide código
    print("🚀 BOT INICIADO (SESSION OK)")
    await client.run_until_disconnected()


loop.run_until_complete(main())
