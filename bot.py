import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

# Fix event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient('session', api_id, api_hash)

# 🔢 VARIABLES DE CONTROL
esperando_green = False
contador_green = 0


@client.on(events.NewMessage)
async def handler(event):
    global esperando_green, contador_green

    try:
        if event.chat_id != CANAL_ORIGEN:
            return

        texto = event.raw_text.upper()

        if not texto:
            return

        print("📩 Mensaje:", texto)

        # 🔴 RED DETECTADO
        if "RED" in texto:
            if esperando_green and contador_green < 3:
                await client.send_message(GRUPO_DESTINO, "❌ OBJETIVO NO CUMPLIDO")

            esperando_green = True
            contador_green = 0

            await client.send_message(GRUPO_DESTINO, "🔴 RED DETECTADO")
            return

        # 🟢 GREEN DETECTADO
        if esperando_green and "GREEN" in texto:
            contador_green += 1

            print(f"GREEN #{contador_green}")

            if contador_green == 3:
                await client.send_message(GRUPO_DESTINO, "🎯 OBJETIVO CUMPLIDO")
                esperando_green = False
                contador_green = 0

    except Exception as e:
        print("❌ Error:", e)


async def main():
    await client.start()
    print("🚀 BOT INTELIGENTE INICIADO")
    await client.run_until_disconnected()


loop.run_until_complete(main())
