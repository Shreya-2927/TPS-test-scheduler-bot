# ========== IMPORTS ==========
from telegram.ext import ConversationHandler
STUDENT_USERNAME, STUDENT_PASSWORD = range(2)
from database import connect_to_db
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import mysql.connector

# ========== MYSQL CONNECTION ==========
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",  # 👈 Yaha apna MySQL password daalo
    database="school_db"
)
cursor = db.cursor()

# ========== LOGIN STATES ==========
ASK_USERNAME, ASK_PASSWORD = range(2)

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to TPS Test Scheduler Bot!\nUse /studentlogin or /teacherlogin to login.")

# ========== STUDENT LOGIN ==========
async def student_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["role"] = "student"
    await update.message.reply_text("Please enter your Student Username:")
    return ASK_USERNAME

# ========== TEACHER LOGIN ==========
async def teacher_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["role"] = "teacher"
    await update.message.reply_text("Please enter your Teacher Username:")
    return ASK_USERNAME

# ========== GET USERNAME ==========
async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("Now enter your Password:")
    return ASK_PASSWORD

# ========== GET PASSWORD ==========
async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]
    password = update.message.text
    role = context.user_data["role"]

    if role == "student":
        cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
    elif role == "teacher":
        cursor.execute("SELECT * FROM teachers WHERE username = %s AND password = %s", (username, password))

    result = cursor.fetchone()

    if result:
        await update.message.reply_text(f"✅ Login successful as {role.capitalize()}!")
        if role == "student":
            await show_student_menu(update, context)
        else:
            await show_teacher_menu(update, context)
    else:
        await update.message.reply_text("❌ Invalid credentials. Try again with /studentlogin or /teacherlogin.")
    
    return ConversationHandler.END

# ========== CANCEL ==========
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Login cancelled.")
    return ConversationHandler.END

# ========== STUDENT MENU ==========
async def show_student_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [
        [KeyboardButton("📅 View Tests"), KeyboardButton("📊 Progress")],
        [KeyboardButton("📝 Start Test"), KeyboardButton("❌ Logout")]
    ]
    await update.message.reply_text("📚 Choose an option:", reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True))

# ========== TEACHER MENU ==========
async def show_teacher_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = [
        [KeyboardButton("➕ Add Questions"), KeyboardButton("🧾 Student Reports")],
        [KeyboardButton("📈 Topic Coverage"), KeyboardButton("❌ Logout")]
    ]
    await update.message.reply_text("👨‍🏫 Choose an option:", reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True))

# ========== STUDENT BUTTON RESPONSES ==========
async def student_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "📅 View Tests":
        await update.message.reply_text("📅 Upcoming Tests:\n1. Math - Friday\n2. Science - Monday")
    elif msg == "📊 Progress":
        await update.message.reply_text("📈 Progress Report:\nScience: 80%\nMath: 75%\nEnglish: 90%")
    elif msg == "📝 Start Test":
        await update.message.reply_text("📝 Test Starting Soon... (Work in Progress)")
    elif msg == "❌ Logout":
        context.user_data.clear()
        await update.message.reply_text("🚪 You have been logged out.")

# ========== TEACHER BUTTON RESPONSES ==========
async def teacher_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "➕ Add Questions":
        await update.message.reply_text("📥 Please upload your questions. (Feature coming soon)")
    elif msg == "🧾 Student Reports":
        await update.message.reply_text("📊 Reports of all students loading...")
    elif msg == "📈 Topic Coverage":
        await update.message.reply_text("📘 Weekly topic coverage upload feature is in progress.")
    elif msg == "❌ Logout":
        context.user_data.clear()
        await update.message.reply_text("🚪 You have been logged out.")

# ========== APP SETUP ==========
app = ApplicationBuilder().token("8091779580:AAE0yg5iZ4d4lZWVdBAd_HB3p8AxyDuXKYk").build()

# Login Conversation Handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("studentlogin", student_login), CommandHandler("teacherlogin", teacher_login)],
    states={
        ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
        ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
# ========== ADD HANDLERS ==========
app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)

# Student Buttons
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(📅 View Tests|📊 Progress|📝 Start Test|❌ Logout)$"), student_menu_handler))

# Teacher Buttons
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(➕ Add Questions|🧾 Student Reports|📈 Topic Coverage|❌ Logout)$"), teacher_menu_handler))

# ========== RUN ==========
print("🤖 Bot is running...")
app.run_polling()
# Start login
async def student_login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Please enter your username:")
    return STUDENT_USERNAME

# Receive username
async def student_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("🔑 Please enter your password:")
    return STUDENT_PASSWORD

# Receive password & verify
async def student_get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["password"] = update.message.text

    from database import connect_to_db
    conn = connect_to_db()
    cursor = conn.cursor()

    username = context.user_data["username"]
    password = context.user_data["password"]

    cursor.execute("SELECT name, class, section FROM students WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()

    if result:
        name, std_class, section = result
        await update.message.reply_text(f"✅ Welcome {name}!\nClass: {std_class}-{section}")
    else:
        await update.message.reply_text("❌ Invalid username or password.")

    cursor.close()
    conn.close()
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Login cancelled.")
    return ConversationHandler.END
app.add_handler()

app.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler("student_login", student_login_start)],
        states={
            STUDENT_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_get_username)],
            STUDENT_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, student_get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
)