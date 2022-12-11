import re

from deep_translator import GoogleTranslator
from deepl import QuotaExceededException, Translator

from config import DEEPL
from constant import TAG_TRAILING, HASHTAG, PLACEHOLDER, FLAG_EMOJI, TAG_EMPTY
from src.input import sources, sources_full

translator = Translator(DEEPL)


def debloat(event, chat_id=None):
    text = event.text

    if chat_id is None:
        chat_id = event.chat_id

    channel = sources_full[chat_id]

    if channel.bloat is not None:
        bloats = [
            e.replace("/", r"\/").replace(".", r"\.").replace("+", r"\+").replace("|", r"\|").replace(" ", r"\s*")
            for e in channel.bloat
        ]  # .replace("<strong>","").replace("</strong>","")
        print("bloats ::::", bloats, event.text)
        if len(bloats) != 0:
            for m in bloats:
                text = re.sub(m, '', text)
            #   print("replace::::::::::", text, "pattern ::::", m)

    print("debloat ::::", text)
    return text


def sanitize(text: str):
    cleaned_empty = re.sub(TAG_EMPTY, '', text)

    g = re.search(TAG_TRAILING, cleaned_empty)
    print("GROUP::::::::::::::::::::", cleaned_empty, g)

    if g is not None:
        for m in g.groups():
            cleaned_empty = re.sub(TAG_TRAILING, f"</{m}>", cleaned_empty, 1)
            print("MATCH ::::::::::::::", cleaned_empty)

    sub_text = re.sub(HASHTAG, '', cleaned_empty)
    print("subbbbbbbb ", sub_text)

    sub_text = sub_text.replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>",
                                                                                                               "</i>")
    print("sanitized ::::", sub_text)
    return sub_text


def translate_text(text:str):
    filtered = re.findall(FLAG_EMOJI, text)
    text_to_translate = re.sub(FLAG_EMOJI, PLACEHOLDER, text)

    try:
        translated_text= translator.translate_text(text_to_translate, target_lang="de", tag_handling="html",
                                         preserve_formatting=True).text

    except QuotaExceededException:
        print("--- Quota exceeded ---")
        translated_text =GoogleTranslator(target="de").translate(text=text_to_translate)
    except Exception as e:
        print("--- other error translating --- ", e)

        translated_text= GoogleTranslator(target="de").translate(text=text_to_translate)

    for emoji in filtered:
        translated_text = re.sub(PLACEHOLDER, emoji, translated_text, 1)

    return translated_text


async def translate(event, chat_id=None):
    if chat_id is None:
        chat_id = event.chat_id

    sub_text = sanitize(debloat(event, chat_id))

    if sub_text == "" or sub_text is None:
        return

    emojis = re.findall(FLAG_EMOJI, sub_text)
    translated_text = translate_text(re.sub(FLAG_EMOJI, PLACEHOLDER, sub_text))

    for emoji in emojis:
        translated_text = re.sub(PLACEHOLDER, emoji, translated_text, 1)

    print("translated_text :::::", translated_text)

    return translated_text


def format_text(translated_text: str, event, backup_id: int, chat_id=None):
    if chat_id is None:
        chat_id = event.chat_id

    channel = sources_full[chat_id]

    if channel.username is None:
        link = f"tg://privatepost?channel={str(event.chat_id)[4:]}&post="
    else:
        link = f"https://t.me/{channel.username}/"

    if channel.invite is not None:
        inv_link = f" | <a href='https://t.me/+{channel.invite}'>🔗Einladungslink</a>"
    else:
        inv_link = ""

    if channel.display is not None:
        name = channel.display
    else:
        name = channel.name

    if channel.bias is not None:
        bias = f" {channel.bias}"
    else:
        bias = ""

    backup = f"| <a href='https://t.me/nn_backup/{backup_id}'> 💾 </a>"
    source = f"Quelle: <a href='{link}{event.original_update.message.id}'>{name}{bias} </a>"
    footer = "👉🏼 Folge @NYX_News für mehr!"

    return f"{translated_text}\n\n{source}{backup}{inv_link}\n\n{footer}"
