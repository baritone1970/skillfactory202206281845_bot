import telebot
from extensions import APIException, Convertor
from config import TOKEN, curencies_list

bot = telebot.TeleBot(TOKEN)


# Обработчик сообщений:
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    reply = 'Чтобы начать работу, введите команду в формате:' \
            '\n <имя валюты исходной валюты>' \
            '\n <в какую валюту перевести>' \
            '\n <количество исходной валюты>' \
            '\nУвидеть список доступных валют: /values'
    bot.reply_to(message, reply)


# Обрабатываются сообщения, содержащие команды '/values'.
@bot.message_handler(commands=['values'])
def handle_start_help(message: telebot.types.Message):
    reply = 'Доступные валюты:'
    for k in curencies_list:
        reply = '\n>'.join((reply, k))
    bot.reply_to(message, reply)


# Обработчик заданий на конвертацию.
@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    parameters = message.text.split(' ')
    try:
        if len(parameters) != 3:
            raise APIException('Неверное количество параметров!')
        answer = Convertor.get_price(*parameters)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception:
        bot.reply_to(message, f"Неизвестная ошибка")
    else:
        bot.reply_to(message, answer)


if __name__ == '__main__':
    # Запускаем телеграм-бота
    bot.polling(none_stop=True)
