from telegram import (Update, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters,
                          ConversationHandler, ContextTypes)

TOKEN = "7977611224:AAG5nuBzOIISnbIkGZI9zsFrpe3bEMHRuM0"

# States
LANGUAGE, MENU, LASER1, LASER2, LASER3, MATERIAL1, MATERIAL2, MATERIAL3, MATERIAL4, SQFT1, SQFT2, SQFT_RATE_QUERY, SQFT_RATE_INPUT = range(13)

user_data = {}

def start_keyboard():
    return ReplyKeyboardMarkup([['Start']], one_time_keyboard=True, resize_keyboard=True)

def language_keyboard():
    return ReplyKeyboardMarkup([['English', 'मराठी']], one_time_keyboard=True, resize_keyboard=True)

def main_menu_keyboard(lang):
    if lang == "English":
        return ReplyKeyboardMarkup([['Laser Cutting Cost', 'Material Cost'], ['Sqft Cost']], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([['लेझर कटिंग खर्च', 'मटेरियल खर्च'], ['स्क्वेअर फूट खर्च']], resize_keyboard=True)

def yes_no_keyboard(lang):
    return ReplyKeyboardMarkup([["Yes" if lang == "English" else "हो", "Stop"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Please click Start to begin.", reply_markup=start_keyboard())
    return LANGUAGE

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot stopped. Type /start to begin again.", reply_markup=start_keyboard())
    return LANGUAGE

async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "start":
        await update.message.reply_text("Choose your language / आपली भाषा निवडा", reply_markup=language_keyboard())
        return LANGUAGE
    elif text == "stop":
        return await stop(update, context)
    elif text in ["english", "मराठी"]:
        context.user_data['lang'] = "English" if text == "english" else "मराठी"
        await update.message.reply_text(
            "Select an option:" if context.user_data['lang'] == "English" else "एक पर्याय निवडा:",
            reply_markup=main_menu_keyboard(context.user_data['lang'])
        )
        return MENU
    else:
        await update.message.reply_text("Please click 'Start' to begin.", reply_markup=start_keyboard())
        return LANGUAGE

async def handle_main_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lang = context.user_data.get('lang', 'English')

    if text.lower() == "stop":
        return await stop(update, context)

    if text in ["Laser Cutting Cost", "लेझर कटिंग खर्च"]:
        await update.message.reply_text("Give Laser Cutting Cut length in mm" if lang == "English" else "कट लांबी (mm मध्ये) द्या")
        return LASER1
    elif text in ["Material Cost", "मटेरियल खर्च"]:
        await update.message.reply_text("Give Length of the sheet in mm" if lang == "English" else "शीटची लांबी (mm मध्ये) द्या")
        return MATERIAL1
    elif text in ["Sqft Cost", "स्क्वेअर फूट खर्च"]:
        await update.message.reply_text("Give Length in inch" if lang == "English" else "लांबी (इंच मध्ये) द्या")
        return SQFT1
    else:
        await update.message.reply_text("Invalid input. Please choose from the menu." if lang == "English" else "अवैध इनपुट. कृपया मेनूमधून निवडा.")
        return MENU

# ---- Laser Cutting Cost Flow ----
async def laser1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['cut_length'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Thickness in mm" if lang == "English" else "जाडी (mm मध्ये) द्या")
        return LASER2
    except ValueError:
        await update.message.reply_text("Please enter a valid number." if lang == "English" else "कृपया योग्य संख्या टाका")
        return LASER1

async def laser2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['thickness'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Rate" if lang == "English" else "दर द्या")
        return LASER3
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Enter a number." if lang == "English" else "अवैध इनपुट. संख्या द्या")
        return LASER2

async def laser3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        rate = float(update.message.text)
        length = context.user_data['cut_length']
        thickness = context.user_data['thickness']
        total = (length * thickness / 1000) * rate
        lang = context.user_data['lang']
        await update.message.reply_text(
            f"Laser Cutting Total Cost = ₹{total:.2f}" if lang == "English" else f"लेझर कटिंग एकूण खर्च = ₹{total:.2f}",
            reply_markup=main_menu_keyboard(lang)
        )
        return MENU
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Enter a number." if lang == "English" else "अवैध इनपुट. संख्या द्या")
        return LASER3

# ---- Material Cost Flow ----
async def material1(update, context):
    try:
        context.user_data['mat_length'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Width of the sheet in mm" if lang == "English" else "शीटची रुंदी (mm मध्ये) द्या")
        return MATERIAL2
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return MATERIAL1

async def material2(update, context):
    try:
        context.user_data['mat_width'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Thickness in mm" if lang == "English" else "जाडी (mm मध्ये) द्या")
        return MATERIAL3
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return MATERIAL2

async def material3(update, context):
    try:
        context.user_data['mat_thickness'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Rate" if lang == "English" else "दर द्या")
        return MATERIAL4
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return MATERIAL3

async def material4(update, context):
    try:
        rate = float(update.message.text)
        l = context.user_data['mat_length']
        w = context.user_data['mat_width']
        t = context.user_data['mat_thickness']
        total = (l * w * t * 0.000008) * rate
        lang = context.user_data['lang']
        await update.message.reply_text(
            f"Material Total Cost = ₹{total:.2f}" if lang == "English" else f"मटेरियल एकूण खर्च = ₹{total:.2f}",
            reply_markup=main_menu_keyboard(lang)
        )
        return MENU
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return MATERIAL4

# ---- Sqft Cost Flow ----
async def sqft1(update, context):
    try:
        context.user_data['sqft_length'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Width in inch" if lang == "English" else "रुंदी (इंच मध्ये) द्या")
        return SQFT2
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return SQFT1

async def sqft2(update, context):
    try:
        context.user_data['sqft_width'] = float(update.message.text)
        lang = context.user_data['lang']
        await update.message.reply_text("Give Rate" if lang == "English" else "दर द्या")
        return SQFT_RATE_INPUT
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return SQFT2

async def sqft_rate_input(update, context):
    try:
        rate = float(update.message.text)
        l = context.user_data['sqft_length']
        w = context.user_data['sqft_width']
        total = (l * w / 144) * rate
        lang = context.user_data['lang']
        await update.message.reply_text(
            f"Sqft Total Cost = ₹{total:.2f}" if lang == "English" else f"स्क्वेअर फूट एकूण खर्च = ₹{total:.2f}",
            reply_markup=main_menu_keyboard(lang)
        )
        return MENU
    except ValueError:
        lang = context.user_data['lang']
        await update.message.reply_text("Invalid input. Please enter a number." if lang == "English" else "अवैध इनपुट. कृपया संख्या द्या")
        return SQFT_RATE_INPUT

if __name__ == '__main__':
    from telegram.ext import Application

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("stop", stop), MessageHandler(filters.TEXT & ~filters.COMMAND, choose_language)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_language)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_option)],
            LASER1: [MessageHandler(filters.TEXT & ~filters.COMMAND, laser1)],
            LASER2: [MessageHandler(filters.TEXT & ~filters.COMMAND, laser2)],
            LASER3: [MessageHandler(filters.TEXT & ~filters.COMMAND, laser3)],
            MATERIAL1: [MessageHandler(filters.TEXT & ~filters.COMMAND, material1)],
            MATERIAL2: [MessageHandler(filters.TEXT & ~filters.COMMAND, material2)],
            MATERIAL3: [MessageHandler(filters.TEXT & ~filters.COMMAND, material3)],
            MATERIAL4: [MessageHandler(filters.TEXT & ~filters.COMMAND, material4)],
            SQFT1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sqft1)],
            SQFT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sqft2)],
            SQFT_RATE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, sqft_rate_input)],
        },
        fallbacks=[CommandHandler("stop", stop), MessageHandler(filters.ALL, stop)]
    )

    app.add_handler(conv_handler)
    app.run_polling()
