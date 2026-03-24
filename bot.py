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

    # 📊 STATS
    if texto == "/eric_9281_stats":
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

    # 🤖 RECOMENDACIÓN
    if texto == "/recomendacion":

        ranking = []

        for i in escenarios:
            esc = escenarios[i]
            efectividad = (esc["exitos"] / esc["inicios"] * 100) if esc["inicios"] > 0 else 0
            ranking.append((i, efectividad))

        # ordenar de mayor a menor
        ranking.sort(key=lambda x: x[1], reverse=True)

        mensaje = "🤖 RECOMENDACIÓN AUTOMÁTICA\n\n"

        for idx, (esc, ef) in enumerate(ranking):
            medalla = ["🥇", "🥈", "🥉", "🏅"]
            mensaje += f"{medalla[idx]} Escenario {esc} → {ef:.2f}%\n"

        mejor = ranking[0][0]

        mensaje += f"\n👉 Mejor opción: ESCENARIO {mejor}"

        if mejor == 1:
            mensaje += " (más seguro)"
        elif mejor == 2:
            mensaje += " (balance riesgo/beneficio)"
        else:
            mensaje += " (más agresivo)"

        await event.reply(mensaje)


# 🧠 LÓGICA PRINCIPAL
@client.on(events.NewMessage)
async def handler(event):
    global esperando, contador_green

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


print("🚀 BOT CON IA DE RECOMENDACIÓN INICIADO")

client.start()
client.run_until_disconnected()
