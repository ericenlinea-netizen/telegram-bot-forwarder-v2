import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

client = TelegramClient('session', api_id, api_hash)

# 🔢 VARIABLES
esperando_green = False
contador_green = 0

# 📊 ESTADÍSTICAS
total_ciclos = 0
cumplidos = 0
no_cumplidos = 0


# 📊 COMANDO /stats
@client.on(events.NewMessage(pattern='/stats'))
async def stats(event):
    global total_ciclos, cumplidos, no_cumplidos

    efectividad = (cumplidos / total_ciclos * 100) if total_ciclos > 0 else 0

    mensaje = f"""
📊 ESTADÍSTICAS

🔁 Ciclos totales: {total_ciclos}
✅ Cumplidos: {cumplidos}
❌ No cumplidos: {no_cumplidos}

📈 Efectividad: {efectividad:.2f}%
"""
    await event.reply(mensaje)


# 🧠 LÓGICA PRINCIPAL
@client.on(events.NewMessage)
async def handler(event):
    global esperando_green, contador_green
    global total_ciclos, cumplidos, no_cumplidos

    try:
        if event.chat_id != CANAL_ORIGEN:
            return

        texto = event.raw_text.upper()

        if not texto:
            return

        print("📩 Mensaje:", texto)

        # 🔴 RED
        if "RED" in texto:
            if esperando_green:
                if contador_green < 3:
                    no_cumplidos += 1
                    await client.send_message(GRUPO_DESTINO, "❌ OBJETIVO NO CUMPLIDO")

            esperando_green = True
            contador_green = 0
            total_ciclos += 1

            await client.send_message(GRUPO_DESTINO, "🔴 RED DETECTADO")
            return

        # 🟢 GREEN
        if esperando_green and "GREEN" in texto:
            contador_green += 1
            print(f"GREEN #{contador_green}")

            if contador_green == 3:
                cumplidos += 1
                await client.send_message(GRUPO_DESTINO, "🎯 OBJETIVO CUMPLIDO")
                esperando_green = False
                contador_green = 0

    except Exception as e:
        print("❌ Error:", e)


print("🚀 BOT CON ESTADÍSTICAS INICIADO")

client.start()
client.run_until_disconnected()
