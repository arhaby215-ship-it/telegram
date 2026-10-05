import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# التوكن الخاص ببوتك
BOT_TOKEN = "8817945545:AAFEmKVIXX18Eu12YjL7myry9xBxAvI57AE"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def delete_message_after_delay(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    chat_id = job_data["chat_id"]
    message_id = job_data["message_id"]

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        logging.info(f"تم حذف الرسالة {message_id} بنجاح.")
    except Exception as e:
        logging.warning(f"تعذر حذف الرسالة {message_id}: {e}")

async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return

    chat_id = update.effective_chat.id
    message_id = update.effective_message.message_id

    # جدولة حذف الرسالة بعد 40 ثانية بالضبط
    context.job_queue.run_once(
        delete_message_after_delay,
        when=40,
        data={"chat_id": chat_id, "message_id": message_id}
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_new_message))
    logging.info("البوت يعمل واستمع للرسائل...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
