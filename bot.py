import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

CANAL_ORIGEN = int(os.getenv("CANAL_ORIGEN"))
GRUPO_DESTINO = int(os.getenv("GRUPO_DESTINO"))

TU_ID = 5019372975

client = TelegramClient('session', api_id, api_hash)

# 🔢 VARIABLES
esperando = False
contador_green = 0

# 📊 ESTADÍSTICAS GENERALES
total_ciclos = 0

# 📊 ESCENARIOS
escenarios = {
    1: {"objetivo": 2, "activo": False, "cumplido": False, "inicios": 0, "exitos": 0, "fallos": 0},
    2: {"objetivo": 3, "activo": False, "cumplido": False, "inicios": 0, "exitos": 0, "fallos": 0},
    3: {"objetivo": 4, "activo": False, "cumplido": False, "inicios": 0, "exitos": 0, "fallos": 0},
    4: {"objetivo": 5, "activo": False, "cumplido": False, "inicios": 0, "exitos": 0, "fallos": 0},
}


# 📊 COMANDO STATS
@client.on(events.NewMessage)
async def comandos(event):
    if event.chat_id != GRUPO_DESTINO:
        return

    if event.sender_id != TU_ID:
        return

    texto = event.raw_text.strip().lower()

    if texto != "/eric_9281_stats":
        return

    mensaje = "📊 ESTADÍSTICAS\n\n"

    for i in escenarios:
        esc = escenarios[i]
        efectividad = (esc["exitos"] / esc["inicios"] * 100) if esc["inicios"] > 0 else 0

        mensaje += f"""
🎯 ESCENARIO {i}
▶️ Inicios: {esc["inicios"]}
✅ Éxitos: {esc["exitos"]}
❌ Fallos: {esc["fallos"]}
📈 Efectividad: {efectividad:.2f}%

"""

    await event.reply(mensaje)


# 🧠 LÓGICA PRINCIPAL
@client.on(events.NewMessage)
async def handler(event):
    global esperando, contador_green, total_ciclos

    try:
        if event.chat_id != CANAL_ORIGEN:
            return

        texto = event.raw_text.upper()
        texto = texto.replace("🍀", "").replace("!", "").strip()

        print("📩 Mensaje:", texto)

        if not texto:
            return

        # 🔴 RED
        if "RED" in texto:

            if esperando:
                for i in escenarios:
                    esc = escenarios[i]
                    if esc["activo"] and not esc["cumplido"]:
                        esc["fallos"] += 1
                        await client.send_message(GRUPO_DESTINO, f"❌ ESCENARIO {i} NO CUMPLIDO")

            esperando = True
            contador_green = 0
            total_ciclos += 1

            # activar escenarios
            for i in escenarios:
                escenarios[i]["activo"] = True
                escenarios[i]["cumplido"] = False
                escenarios[i]["inicios"] += 1

            await client.send_message(GRUPO_DESTINO, "🔴 RED DETECTADO")
            return

        # 🟢 GREEN
        if esperando and "GREEN" in texto:
            contador_green += 1
            print(f"GREEN #{contador_green}")

            for i in escenarios:
                esc = escenarios[i]

                if esc["activo"] and not esc["cumplido"]:
                    if contador_green == esc["objetivo"]:
                        esc["cumplido"] = True
                        esc["exitos"] += 1
                        await client.send_message(GRUPO_DESTINO, f"🎯 ESCENARIO {i} CUMPLIDO")

    except Exception as e:
        print("❌ Error:", e)


print("🚀 BOT MULTI ESCENARIOS INICIADO")

client.start()
client.run_until_disconnected()
