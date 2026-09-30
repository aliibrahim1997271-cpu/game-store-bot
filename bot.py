import telebot
from telebot import types
import os

TOKEN = "8702641409:AAEdCvIf_WKajYS52jn_H2DjmCrh1sNysck"
ADMIN_ID = 8581698359

bot = telebot.TeleBot(TOKEN)

# قواعد بيانات مؤقتة
user_wallets = {}  
games_prices = {
    "موبايل ليجند (100 جوهرة)": 750,
    "ببجي موبايل (60 شدة)": 1000,
    "فري فاير (110 جوهرة)": 800
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎮 شحن الألعاب", "💰 رصيد محفظتي")
    if message.from_user.id == ADMIN_ID:
        markup.add("⚙️ لوحة التحكم (الأدمن)")
    bot.send_message(message.chat.id, "أهلاً بك في متجر شحن الألعاب الرسمي 🚀\nاختر ما يناسبك من القائمة أدناه:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 رصيد محفظتي")
def check_wallet(message):
    uid = message.from_user.id
    balance = user_wallets.get(uid, 0)
    bot.send_message(message.chat.id, f"💳 رصيد محفظتك الحالي: {balance} د.ع")

@bot.message_handler(func=lambda message: message.text == "🎮 شحن الألعاب")
def show_games(message):
    markup = types.InlineKeyboardMarkup()
    for game, price in games_prices.items():
        markup.add(types.InlineKeyboardButton(f"{game} - {price} د.ع", callback_data=f"buy_{game}"))
    bot.send_message(message.chat.id, "اختر اللعبة والباقة التي تريد شحنها:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def process_buy(call):
    game_name = call.data.replace('buy_', '')
    price = games_prices[game_name]
    uid = call.from_user.id
    balance = user_wallets.get(uid, 0)
    
    markup = types.InlineKeyboardMarkup()
    if balance >= price:
        markup.add(types.InlineKeyboardButton("💳 الدفع من المحفظة", callback_data=f"pay_wallet_{game_name}"))
    markup.add(types.InlineKeyboardButton("📤 الدفع عبر إرسال وصل (حول 1000 مثلاً)", callback_data=f"pay_receipt_{game_name}"))
    
    bot.send_message(call.message.chat.id, f"لقد اخترت: {game_name}\nالسعر: {price} د.ع\nرصيدك الحالي: {balance} د.ع\n\nاختر طريقة الدفع:", reply_markup=markup)

print("Bot is running...")
bot.infinity_polling()
