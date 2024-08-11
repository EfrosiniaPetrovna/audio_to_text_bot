import os, datetime, json, requests, time, io
from pprint import pprint
import telebot
from conf import LOGGER as logging, BASE_DIR, CONFIG
import utils

logging.info(f'bot: {CONFIG["LOAD_BOT_NAME"]}')

bot = telebot.TeleBot(CONFIG['TOKEN'])


@bot.message_handler(commands=['help'], content_types=['text'])
def help_message(message:telebot.types.Message):
    logging.info(f'Новый запрос (text): {message.json}')
    text = ('1. Добавьте бот в вашу группу\n'
            '2. Убедитесь, что бот имеет доступ к сообщениям\n'
            '3. Для скрытия ссылки на наш канал вы или любой из админов группы (для групп) '
            f'должны быть подписаны на наш канал {CONFIG["OWNER_CHANNEL_LINK"]}')
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(content_types=['voice'])
def voice_message(message:telebot.types.Message):
    logging.info(f'Новый запрос (text): {message.json}')
    language_code = message.json.get('from', {}).get('language_code')
    data = bot.download_file(bot.get_file(message.voice.file_id).file_path)
    file_name = os.path.join('voice', f'{message.chat.id}_{message.date}_voice')
    utils.bytes_to_file(file_name, data)
    audio_file = utils.convert_ogg_to_wav(file_name)
    try:
        result = utils.transcribe_audio(audio_file, language_code)
    except utils.sr.exceptions.UnknownValueError:
        result = 'Речь не распознана'
    chat_type, chat_id, is_follower = utils.get_chat_info(bot, message)
    author = utils.get_message_author_name(message)
    if author:
        result = f'<b>{author}</b>:\n{result}'
    if not is_follower:
        result += f'\n<i>by {CONFIG["OWNER_CHANNEL_LINK"]}</i>'
    bot.send_message(message.chat.id, text=result, parse_mode='html')
    os.remove(file_name)


if CONFIG['LOAD_BOT_NAME'] == 'test_bot':
    bot.polling(none_stop=True, interval=0)
else:
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            logging.error(f'bot.polling -- {e}')
            time.sleep(15)





