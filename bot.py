import os
from dotenv import load_dotenv

from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

load_dotenv()

TELEGRAM_TOKEN = "8774978613:AAFQTLvS0CfRZyhvWh11RhcSfRieYXgu3yY"
ADMIN_ID = 6721514548

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Support form steps
NAME, REQUEST = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🏢 About Apex Horizon", "🛠 Services"],
        ["💼 Business Solutions", "📞 Contact Support"],
        ["❓ FAQ", "🤖 Ask AI"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Welcome to Apex Horizon LLC 🤖\n\n"
        "Your professional business services assistant.\n\n"
        "How can we assist you today?",
        reply_markup=reply_markup
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏢 About Apex Horizon LLC\n\n"
        "Apex Horizon LLC is a professional business services company "
        "dedicated to delivering reliable operational support and "
        "strategic solutions for individuals, entrepreneurs, and "
        "organizations.\n\n"
        "We specialize in business solutions, customer support services, "
        "financial and brokerage assistance, investment operations, "
        "and administrative coordination.\n\n"
        "Our mission is to help clients streamline processes, improve "
        "efficiency, and achieve sustainable growth through dependable "
        "service and professional expertise."
    )


async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛠 Apex Horizon LLC Services\n\n"
        "• Professional business solutions and consulting\n"
        "• Customer support and client assistance\n"
        "• Financial and brokerage support services\n"
        "• Investment operational coordination\n"
        "• Administrative and business process support\n"
        "• General business inquiries and assistance\n\n"
        "Why Choose Us?\n\n"
        "✅ Professional service\n"
        "✅ Reliable support\n"
        "✅ Client-focused approach\n"
        "✅ Accuracy and efficiency"
    )


async def business(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💼 Business Solutions\n\n"
        "Apex Horizon LLC helps individuals and organizations "
        "with operational support, business coordination, "
        "and professional assistance."
    )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❓ Frequently Asked Questions\n\n"
        "Q: What does Apex Horizon LLC do?\n"
        "A: We provide professional business support services.\n\n"
        "Q: How can I contact support?\n"
        "A: Use the Contact Support option."
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📞 Apex Horizon LLC Support\n\n"
        "Please provide your name."
    )

    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Thank you.\n\n"
        "Please describe your request or the service you need help with."
    )

    return REQUEST


async def get_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = context.user_data["name"]
    request = update.message.text

    message = (
        "🔔 New Apex Horizon LLC Inquiry\n\n"
        f"Name: {name}\n"
        f"Request: {request}\n"
        f"Telegram User ID: {update.effective_user.id}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message
    )

    await update.message.reply_text(
        "Thank you for contacting Apex Horizon LLC.\n\n"
        "Your request has been received. Our team will review it and respond."
    )

    return ConversationHandler.END


async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    company_context = """
You are the official AI assistant for Apex Horizon LLC.

Company Information:
Apex Horizon LLC is a professional business services company providing
business solutions, customer support services, financial and brokerage
support assistance, investment operational coordination, and administrative
business support.

Your role:
- Be professional, helpful, and respectful.
- Answer questions about Apex Horizon LLC services.
- Help potential clients understand available services.
- Assist users with general business inquiries.
- Encourage users to contact support for specific requests.

Company Support:
Email: support@apexhorizonllc.com

Support Hours:
Monday-Friday, 9:00 AM - 6:00 PM UTC.

Do not claim to provide services that are not listed.
Do not make promises about financial returns or guaranteed results.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=company_context + "\n\nUser Question:\n" + user_message
    )

    await update.message.reply_text(
        response.output_text
    )


app = Application.builder().token(TELEGRAM_TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.Regex("🏢 About Apex Horizon"), about)
)

app.add_handler(
    MessageHandler(filters.Regex("🛠 Services"), services)
)

app.add_handler(
    MessageHandler(filters.Regex("💼 Business Solutions"), business)
)

app.add_handler(
    MessageHandler(filters.Regex("❓ FAQ"), faq)
)


support_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("📞 Contact Support"), contact)
    ],
    states={
        NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
        ],
        REQUEST: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_request)
        ],
    },
    fallbacks=[]
)

app.add_handler(support_handler)


app.add_handler(
    MessageHandler(filters.Regex("🤖 Ask AI"), ai_reply)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_reply
    )
)


print("Apex Horizon LLC AI Bot is running...")

app.run_polling()
