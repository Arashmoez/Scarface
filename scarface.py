import logging
from pathlib import Path
from decouple import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

Token = config('Token')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Change to DEBUG for more verbosity
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ['Alejandro Sosa', 'Antonio Montana'],
        ['Manolo Ribera', 'Frank Lopez'],
        ['Omar Suarez', 'Angel Fernandez'],
        ['Ernie Garcia']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    chat_id = update.message.chat_id
    await update.message.reply_text("What is your favorite character?", reply_markup=reply_markup)

async def cancel(update:Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text("Canceled.", reply_markup=reply_markup)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    context.user_data['favorite_character'] = user_choice
    keyboard = [
        [InlineKeyboardButton("Description", callback_data=f"{user_choice}-1")],
        [InlineKeyboardButton("Photos", callback_data=f"{user_choice}-2")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text ("Please choose:", reply_markup=reply_markup)
    

async def handle_descripton_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    name_without_id = data[:-2]
    if data[-1] == '1':
        match name_without_id:
            case "Alejandro Sosa":
                await query.edit_message_text("The mastermind of drug empire.")
            case "Antonio Montana":
                await query.edit_message_text("Political refugee.")
            case "Frank Lopez":
                await query.edit_message_text("Do you know what a khazzer is, Frank?")
            case "Omar Suarez":
                await query.edit_message_text("Informer for the police.")
            case "Manolo Ribera":
                await query.edit_message_text("A horse that sticks his tongue out like a lizard. Seduced by vagina.")
            case "Angel Fernandez":
                await query.edit_message_text("Massacred with a chainsaw by Colombians.")
            case "Ernie Garcia":
                await query.edit_message_text("The worst bodygaurd ever, got recruited after the Frank incident.")
    else:
        match name_without_id:
            case "Alejandro Sosa":
                file_path = Path('./') / 'static' / 'photos' / 'Alejandro_Sosa.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Alejandro Sosa")
                    )
            case "Antonio Montana":
                file_path = Path('./') / 'static' / 'photos' / 'Antonio_Montana.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Antonio Montana")
                    )
            case "Omar Suarez":
                file_path = Path('./') / 'static' / 'photos' / 'Omar_Suarez.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Omar Suarez")
                    )
            case "Angel Fernandez":
                file_path = Path('./') / 'static' / 'photos' / 'Angel_Fernandez.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Angel Fernandez")
                    )
            case "Ernie_Garcia":
                file_path = Path('./') / 'static' / 'photos' / 'Ernie_Garcia.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Ernie")
                    )
            case "Manolo Ribera":
                file_path = Path('./') / 'static' / 'photos' / 'Manolo_Ribera.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Manny")
                    )
            case "Frank Lopez":
                file_path = Path('./') / 'static' / 'photos' / 'Frank_Lopez.jpg'
                with open(file_path, "rb") as photo:
                    await query.edit_message_media(
                        media=InputMediaPhoto(media=photo, caption="Frank Lopez")
                    )
    
    

async def handle_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

def main():
    application = Application.builder().token(Token).build()
    start_handler = CommandHandler("start", start)
    response_handler = MessageHandler(filters.TEXT & ~ filters.COMMAND, handle_response)
    description_photos_handler = CallbackQueryHandler(handle_descripton_photos)
    cancel_handler = CommandHandler("cancel", cancel)

    application.add_handler(start_handler)
    application.add_handler(response_handler)
    application.add_handler(description_photos_handler)
    application.add_handler(cancel_handler)
    application.run_polling()

if __name__=='__main__':
    main()