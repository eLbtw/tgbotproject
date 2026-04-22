import telebot
import requests
import feedparser
import xml.etree.ElementTree as ET

BOT_TOKEN = '8687808910:AAGCO0Ey4Ven19fu_zLT-g-fcaVFZauAM_g'
WEATHER_API = 'eef1647ee2d4a2f04b2ebcc49b8ce704'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я бот-агрегатор уведомлений.\n\n"
        "Вот что я умею:\n"
        "/weather — Узнать погоду в пгт. Гвардейское ⛅\n"
        "/news — Получить последние три новости дня 📰\n"
        "/currency — Актуальный курс валют 💵"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?id=707777&appid={WEATHER_API}&units=metric&lang=ru"
        response = requests.get(url).json()

        temp = round(response['main']['temp'])
        feels_like = round(response['main']['feels_like'])
        desc = response['weather'][0]['description']

        weather_text = f"⛅ Погода в пгт. Гвардейское:\nТемпература: {temp}°C (ощущается как {feels_like}°C)\nНа улице: {desc.capitalize()}"
        bot.send_message(message.chat.id, weather_text)
    except Exception as e:
        bot.send_message(message.chat.id, "Извините, не удалось получить данные о погоде.")

@bot.message_handler(commands=['news'])
def get_news(message):
    try:
        feed = feedparser.parse("https://lenta.ru/rss/news")
        news_text = "📰 Главные новости на данный момент:\n\n"

        for i in range(3):
            entry = feed.entries[i]
            news_text += f"{i+1}. {entry.title}\nЧитать далее: {entry.link}\n\n"

        bot.send_message(message.chat.id, news_text)
    except Exception as e:
        bot.send_message(message.chat.id, "Извините, не удалось загрузить новости.")

@bot.message_handler(commands=['currency'])
def get_currency(message):
    try:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url)
        tree = ET.fromstring(response.content)

        usdraw = tree.find(".//Valute[@ID='R01235']/Value").text
        eurraw = tree.find(".//Valute[@ID='R01239']/Value").text

        usd = round(float(usdraw.replace(',', '.')), 2)
        eur = round(float(eurraw.replace(',', '.')), 2)

        currency_text = f"📈 Официальный курс валют (ЦБ РФ):\n\n💵 USD: {usd} руб.\n💶 EUR: {eur} руб."
        bot.send_message(message.chat.id, currency_text)
    except Exception as e:
        bot.send_message(message.chat.id, "Извините, не удалось получить курс валют.")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
