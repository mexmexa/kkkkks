import random
import datetime
import os
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from flask import Flask
from threading import Thread

TOKEN = "8556431265:AAFZA51BdMbGdAsqpDu7BlNNu4lzpAyy8JM"
USER_FILE = "users.json"  # Archivo donde guardamos los IDs de los usuarios

# -------------------------
# Cargar usuarios desde el archivo
# -------------------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return []

# -------------------------
# Guardar usuarios en el archivo
# -------------------------
def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_FILE, "w") as file:
            json.dump(users, file)

# -------------------------
# Preguntas motivacionales diarias (Ampliadas)
# -------------------------
PREGUNTAS = {
    "mañana": [
        "🌅 ¡Buenos días! ¿Qué puedes hacer hoy para acercarte más a tus metas?",
        "☀️ Al despertar, ¿qué es lo primero que piensas? ¡Haz de hoy un gran día!",
        "💧 ¿Ya tomaste agua al despertar? Hidratarte es clave para comenzar el día con energía.",
        "🥗 ¿Tienes algún desayuno saludable planeado hoy? ¡Lo que comes al inicio del día marca la diferencia!",
        "🧠 Hoy, ¿qué te gustaría lograr en tu día? ¡Escribe tus metas y hazlas realidad!",
        "🌞 Si pudieras definir tu objetivo principal para hoy, ¿cuál sería?",
        "🏃‍♂️ ¿Listo para moverte hoy? Recuerda que el movimiento es clave para un día productivo.",
        "🧘‍♀️ ¿Te has dado un momento para respirar profundamente hoy? El mindfulness también es importante.",
        "💪 ¿Cómo te sientes para entrenar hoy? ¡Recuerda que tu cuerpo es tu mejor aliado!"
    ],
    "tarde": [
        "🔥 ¿Ya entrenaste hoy? Si no es así, ¿qué te detiene? ¡Es tu momento!",
        "💪 ¿Te sientes con energía? Si no, tal vez un buen snack saludable te recargue.",
        "🥗 ¿Qué has comido hasta ahora? ¡Recuerda que lo que consumes afecta cómo te sientes!",
        "💬 ¿Cómo va tu jornada hasta ahora? ¿Necesitas un descanso o un pequeño impulso?",
        "⚡ ¿Te gustaría compartir algo que te haya motivado hoy? ¡Es un buen momento para reflexionar!",
        "🌱 Si estás cansado, ¿qué podrías hacer para recargar energías? ¡Escucha a tu cuerpo!",
        "🏋️‍♀️ ¿Te has dado tiempo para hacer alguna actividad física hoy? ¡Aprovecha ese impulso!",
        "📚 ¿Estás aprendiendo algo nuevo hoy? ¡El conocimiento es poder!",
        "🌟 ¿Hoy es un día para avanzar o simplemente descansar? ¡Ambos son válidos!"
    ],
    "noche": [
        "🌙 ¡Gran trabajo hoy! ¿Cómo te sientes al final del día? ¡Cada esfuerzo cuenta!",
        "💭 Hoy, ¿qué aprendiste sobre ti mismo/a? ¡El aprendizaje continuo es parte del crecimiento!",
        "🧘‍♀️ ¿Qué hiciste hoy para relajarte? El descanso también es esencial para tu progreso.",
        "🍽️ ¿Comiste algo nutritivo para la cena? ¡Recuerda que lo que consumes ayuda a tu recuperación!",
        "📈 ¿Cuál fue tu mayor logro hoy? ¡Celebra tus victorias, por pequeñas que sean!",
        "🌙 Al final del día, ¿qué te gustaría mejorar mañana? ¡Cada día es una nueva oportunidad!",
        "✨ ¿Hiciste algo hoy por tu bienestar mental? ¡No olvides que tu mente también necesita cuidado!",
        "🎯 ¿Tus metas están claras para mañana? ¡Prepara tu mente y cuerpo para un nuevo día!",
        "🌱 Reflexiona: ¿cómo puedes ser aún más eficiente mañana? ¡Haz que cada día cuente!"
    ]
}

# -------------------------
# Frases motivacionales
# -------------------------
MOTIVACION = [
    "✨ ¡Lo estás haciendo increíble! Cada día es una nueva oportunidad para crecer.",
    "🔥 No te detengas ahora, ¡estás más cerca de lo que crees!",
    "💪 *La disciplina hoy* es la *victoria mañana*",
    "🌱 Cada paso cuenta, no importa cuán pequeño sea, estás avanzando.",
    "💥 Tienes todo lo necesario para lograr tus metas, ¡no te rindas!",
    "🌟 Hoy es un buen día para seguir trabajando en ti mismo/a. ¡Sigue así!",
    "🚀 El esfuerzo de hoy te llevará a la mejor versión de ti mañana. ¡Sigue adelante!",
    "🌈 Cada esfuerzo suma, y tú estás en el camino correcto. ¡Sigue avanzando!",
    "🏅 El éxito no es un destino, es un camino. ¡Sigue caminando con fuerza!"
]

# -------------------------
# Respuestas del bot
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    save_user(user_id)  # Guardar el ID del usuario al iniciar el bot

    bienvenida = (
        "🎉 *¡Bienvenido a CoreX!*\n\n"
        "¡Estás a punto de comenzar una aventura increíble hacia tu mejor versión! 🚀💪\n\n"
        "Soy tu compañero de entrenamiento y motivación, aquí para apoyarte en cada paso de tu jornada.\n"
        "¡Lo que más quiero es que te sientas fuerte, motivado y listo para romperla cada día! 🔥✨\n\n"
        "Recuerda: ¡Nunca estás solo/a en esto! Cada día te enviaré preguntas, consejos y mucho ánimo para que "
        "sigamos avanzando juntos en tu camino hacia el éxito. 💥"
    )

    await update.message.reply_text(bienvenida)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    # Responder a situaciones negativas
    if "cansado" in texto or "no puedo" in texto or "agotado" in texto:
        mensaje_emocional = (
            "💛 *Te escucho.* A veces no es fácil, pero recuerda esto:\n\n"
            "✨ *En CoreX creemos en ti incluso en los días difíciles.* ¡Eres más fuerte de lo que crees!\n\n"
            "¿Qué te está costando más hoy? Cuéntame, estoy aquí para apoyarte."
        )
    # Responder a situaciones positivas
    elif "bien" in texto or "motivado" in texto or "entrené" in texto:
        mensaje_emocional = (
            "🔥 ¡Eso me encanta escuchar! Así se construye una mentalidad CoreX. ¡Sigue así!\n\n"
            "*Felicitaciones* por dar el 100% hoy, ¡lo estás logrando!"
        )
    # Responder a cualquier otra situación
    else:
        mensaje_emocional = "💬 Entiendo, gracias por compartirlo. Estoy contigo en este camino hacia tu mejor versión."

    # Enviar mensaje motivacional
    await update.message.reply_text(mensaje_emocional)

    # Enviar un consejo motivacional
    await update.message.reply_text(random.choice(MOTIVACION))

# -------------------------
# Tareas automáticas diarias (horarios fijos)
# -------------------------
async def mensajes_diarios(context: ContextTypes.DEFAULT_TYPE):
    users = load_users()  # Cargar los usuarios desde el archivo

    # Definir horarios fijos para enviar preguntas
    hora_preguntas = {
        "mañana": datetime.time(hour=8, minute=0),
        "tarde": datetime.time(hour=14, minute=0),
        "noche": datetime.time(hour=20, minute=0)
    }

    for user in users:
        hora_actual = datetime.datetime.now().time()

        if hora_actual < hora_preguntas["mañana"]:
            mensaje = random.choice(PREGUNTAS["mañana"])
        elif hora_actual < hora_preguntas["tarde"]:
            mensaje = random.choice(PREGUNTAS["tarde"])
        else:
            mensaje = random.choice(PREGUNTAS["noche"])

        # Enviar mensaje con la pregunta motivacional
        await context.bot.send_message(chat_id=user, text=mensaje)

        # Enviar mensaje de motivación
        await context.bot.send_message(chat_id=user, text=random.choice(MOTIVACION))

# -------------------------
# Inicializar Flask
# -------------------------
app = Flask(__name__)

@app.route('/')
def webhook():
    return 'Bot de CoreX en funcionamiento!'

# -------------------------
# Main para ejecutar Flask y Telegram
# -------------------------
def start_flask():
    app.run(host="0.0.0.0", port=5000)

def main():
    # Iniciar la aplicación de Telegram
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    telegram_app.job_queue.run_daily(mensajes_diarios, time=datetime.time(hour=8, minute=0))

    # Iniciar Flask en un hilo separado
    thread = Thread(target=start_flask)
    thread.start()

    print("🔥 CoreX Assistant está activo... y escuchando en Flask")
    telegram_app.run_polling()

if __name__ == "__main__":
    main()
