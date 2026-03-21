import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

canal_origen = os.getenv("CANAL_ORIGEN")
grupo_destino = int(os.getenv("GRUPO_DESTINO"))

# 🔹 Cliente usuario (lee canal)
user = TelegramClient('user_session', api_id, api_hash)

# 🔹 Cliente bot (envía mensajes)
bot = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


@user.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()

    if chat.id != int(os.getenv("CANAL_ORIGEN")):
        return

    mensaje = event.message.text

    if not mensaje:
        return

    print("📩 Mensaje detectado:", mensaje)

    entity = await bot.get_input_entity(grupo_destino)
    await bot.send_message(entity, mensaje)
async def handler(event):
    mensaje = event.message.text

    if not mensaje:
        return

    print("📩 Mensaje detectado:", mensaje)

    entity = await bot.get_input_entity(grupo_destino)


async def main():
    await user.start()  # Aquí se loguea tu cuenta
    print("👤 USER conectado")
    print("🤖 BOT listo")
    await user.run_until_disconnected()


with bot:
    bot.loop.run_until_complete(main())
