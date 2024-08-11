import telebot
import speech_recognition as sr
import soundfile as sf
from io import BytesIO
from pprint import pprint
from conf import LOGGER as logging, BASE_DIR, CONFIG


def get_chat_info(bot:telebot.TeleBot, message:telebot.types.Message):
    '''
    :param bot:
    :param message:
    :return:
    chat type
    chat id
    is follower
    '''
    chat_type = None
    chat_id = message.chat.id
    is_follower = False
    if message.chat.type == 'private':
        chat_type = 'user'
        if bot.get_chat_member(CONFIG['OWNER_CHANNEL_ID'], message.chat.id):
            is_follower = True
    elif 'group' in message.chat.type:
        chat_type = 'group'
        for i in bot.get_chat_administrators(message.chat.id):
            if not i.user.is_bot and bot.get_chat_member(CONFIG['OWNER_CHANNEL_ID'], i.user.id):
                is_follower = True
                break
    return (chat_type, chat_id, is_follower)


def get_message_author_name(message:telebot.types.Message):
    if message.json.get('forward_origin', {}).get('type') == 'user':
        return message.json['forward_origin']['sender_user']['first_name']
    elif message.json.get('from', {}).get('first_name'):
        return message.json['from']['first_name']


def bytes_to_file(file_name, data):
    with open(file_name, "wb") as outfile:
        outfile.write(data)


def convert_ogg_to_wav(input_file):
    buf = BytesIO()
    data, samplerate = sf.read(input_file)
    sf.write(buf, data, samplerate, format='WAV')
    buf.seek(0)
    return buf


def transcribe_audio(audio_file, language_code=None):
    language_code = language_code or 'ru'
    r = sr.Recognizer()
    file = sr.AudioFile(audio_file)
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio, language=language_code)
    return result

