import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

# Crear loop manual (compatibilidad)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Cliente USER (lee canal)
user = TelegramClient('user_session', api_id, api_hash)

# Cliente BOT (envía mensajes)
bot = TelegramClient('bot_session', api_id, api_hash)


@user.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()

        # Filtrar solo el canal origen
        if chat.id != CANAL_ORIGEN:
            return

        mensaje = event.message.text

        if not mensaje:
            return

        print("📩 Mensaje detectado:", mensaje)

        # Obtener grupo destino correctamente
        entity = await bot.get_input_entity(GRUPO_DESTINO)

        await bot.send_message(entity, mensaje)

    except Exception as e:
        print("❌ Error:", e)


async def main():
    # Iniciar USER
    await user.start()
    print("👤 USER conectado")

    # Iniciar BOT solo si no está conectado (evita flood)
    if not bot.is_connected():
        await bot.start(bot_token=bot_token)

    print("🤖 BOT listo")

    await user.run_until_disconnected()


loop.run_until_complete(main())
