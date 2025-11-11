import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from transport_api import get_bus_times  # Importa la función

# Carga variables del .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Función que responde al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 ¡Hola! Soy tu bot de transporte de Madrid.")

# Función para consultar tiempos de una parada
async def parada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Por favor indica el ID de la parada. Ejemplo: /parada 1234")
        return

    stop_id = context.args[0]
    buses = get_bus_times(stop_id)
    
    if not buses:
        await update.message.reply_text("❌ No se han encontrado buses para esa parada.")
        return

    message = "🚌 Tiempos de llegada:\n"
    for bus in buses:
        message += f"Linea {bus['line']} → {bus['destination']} : {bus['time']} min\n"

    await update.message.reply_text(message)

# Crear el bot y agregar handlers **antes** de run_polling
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("parada", parada))

if __name__ == "__main__":
    print("Bot iniciado...")
    app.run_polling()
