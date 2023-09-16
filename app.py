import telebot
from config import keys, TOKEN
from utils import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Для начала работы введите информацию в следующем формате:\n<имя валюты> \n<в какую валюту перевести> \n<колличество валюты> \n Чтобы увидеть список всех доступных валют введите /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values =  message.text.split(' ')

        if len(values) > 3:
            raise ConvertionExeption('Введите 3 параметра.')

        quote, base, amount = values

        total_base = CryptoConverter.convert(quote, base, amount, message.chat.id)

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    except ConvertionExeption as e:
        bot.send_message(message.chat.id, e)


bot.polling()