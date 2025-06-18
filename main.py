import logging
import os
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

today_tab = datetime.today().strftime("%d-%m-%Y")
worksheet = client.open_by_url(SHEET_URL).worksheet(today_tab)

def get_lines():
    data = worksheet.col_values(1)
    return [row.replace("Line- ", "") for row in data if row.startswith("Line-")]

def extract_line_data(line_name):
    data = worksheet.get_all_values()
    result = []
    capture = False
    for row in data:
        if row[0].strip() == f"Line- {line_name}":
            capture = True
            continue
        if capture:
            if row[0].strip().startswith("Line-") or row[0].strip() == '':
                break
            result.append(row)
    return result

def format_line_data(line_name):
    rows = extract_line_data(line_name)
    if not rows:
        return f"No data found for Line {line_name}"
    message = f"📅 Date: {today_tab}\n🛠️ Line: {line_name}\n\n"
    for row in rows:
        op, first, second, third, total = row[:5]
        message += f"✳️ {op.strip()}: 1st={first} | 2nd={second} | 3rd={third} | Total={total}\n"
    return message

def start(update: Update, context: CallbackContext):
    lines = get_lines()
    keyboard = [[InlineKeyboardButton(line, callback_data=line)] for line in lines]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select Production Line:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    line = query.data
    text = format_line_data(line)
    query.edit_message_text(text=text)

def error(update: Update, context: CallbackContext):
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
