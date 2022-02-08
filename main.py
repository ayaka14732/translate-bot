import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credential.json'

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import escape_md
from google.cloud import translate
import json

def load_config():
    with open('config.json') as f:
        o = json.load(f)
    return o['api_token'], o['project_id']

API_TOKEN, PROJECT_ID = load_config()

client = translate.TranslationServiceClient()

def is_english(text: str):
    parent = f'projects/{PROJECT_ID}/locations/global'
    response = client.detect_language(request={
        'parent': parent,
        'content': text,
        'mime_type': 'text/plain',
    })
    return response.languages[0].language_code == 'en'

def translate_text(text: str, lang: str):
    parent = f'projects/{PROJECT_ID}/locations/global'
    response = client.translate_text(request={
        'parent': parent,
        'contents': [text],
        'mime_type': 'text/plain',
        'source_language_code': 'en-US',
        'target_language_code': lang,
    })
    return response.translations[0].translated_text

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    text = message.text
    if is_english(text):
        await message.reply(escape_md(f'''🇩🇰 {translate_text(text, lang='da')}
🇩🇪 {translate_text(text, lang='de')}'''), parse_mode='MarkdownV2')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
