import dataclasses
import os
import re

from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv("TG_ID")
api_hash = os.getenv("TG_HASH")

DATABASE_URL = "postgresql://postgres:area@localhost:5432/news"
POST_CHANNEL = -1001839268196

FLAG_EMOJI = re.compile(r"🏴|🏳️|([🇦-🇿]{2})")
PLACEHOLDER = "║"

@dataclasses.dataclass
class Source:
    channel_name: str
    footer: str = r"\s*"
    bias: str = ""


CHANNELS = {
    # -1001839268196:Source("Test"),  # Test
    # 1317941240:Source("MN-Bot",  # MN-bot
    -1001391125365: Source("Test2"),  # Test2
  #   -1001526741474:Source("MNChat"),  # MNChat
    -1001486678205: Source("Militär-Memes", "🔰 Subscribe to @MilitaerMemes for more"),  # todo: also handle DE footer
    -1001240262412: Source("Militär-News🔰", "🔰 Abonniere @MilitaerNews\n🔰 Diskutiere im @MNChat"),

    # Ukrainian
    -1001452778151: Source("Krugozor", "<a href='https//t.me/krugozor_news'>Кругозор</a>", "🇺🇦"),
    -1001619608359: Source("TiskSnip", bias="🇺🇦"),
    -1001594428146: Source("WerochnaRada", bias="🇺🇦"),
    -1001469021333: Source("DeepState", bias="🇺🇦"),
    -1001759230769: Source("Bayraktar", "<a href='https://t.me/+WPl-WyPpW3QyMjgy'>Свежие крипто-новости тут</a>", "🇺🇦"),
    -1001201459971: Source("Rysnya", bias="🇺🇦"),
    -1001218743574: Source("Goncharenko", bias="🇺🇦"),
    -1001413275904: Source("NEXTA", bias="🇺🇦"),
    -1001011817559: Source("Militarnij", "@milinua", "🇺🇦"),
    -1001414210176: Source("FirstDivision", bias="🇺🇦"),

    # Russian
    -1001141171940: Source("Kadyrow", bias="🇷🇺"),
    -1001076431027: Source("ItsDonezk",
                           "<a href='https://t.me/joinchat/QCkIs9PWI4jWPgNy'>Подписаться</a>  |  <a href='https://t.me/EtoDonetsk_bot'>Предложить новость</a>",
                           "🇷🇺"),
    -1001260622817: Source("Readovka", bias="🇷🇺"),
    -1001149896996: Source("Interfax", "@interfaxonline", "🇷🇺"),
    -1001543896043: Source("RussiaMedwed",
                           "Вся ЖЕСТЬ СВО у нас в резерве 👉 <a href='https://t.me/+bSe6VmuHMlthYWEy'>Смотреть</a>.",
                           "🇷🇺"),
    -1001135021433: Source("WarGonzo",
                           "@wargonzo\n\n*наш проект существует на средства подписчиков, карта для помощи\n4279 3806 9842 9521",
                           "🇷🇺"),
    -1001708761316: Source("PrjamoyEfir", r"<a href='https://t.me/+jQvaOFH1zhAzMzIy'>Прямой эфир - подписаться</a>",
                           "🇷🇺"),
    -1001382288937: Source("BalkanSniper", bias="🇷🇺"),
    -1001099737840: Source("Rusvesna",
                           "<a href='<strong>t.me/rusvesnasu</strong>'><strong>t.me/rusvesnasu</strong></a>", "🇷🇺"),
    -1001326223284: Source("Rybar", "@rybar\n\n<em>*Поддержать нас: </em><code>4377 7278 0407 7977</code>", "🇷🇺"),
    -1001730870551: Source("RSOTM", bias="🇷🇺"),

    # Polish
    -1001577023152: Source("Syrenka", "@pl_syrenka — Польша не заграница", "🇵🇱"),

    # Azeri
    -1001261746950: Source("AAF",
                           "<a href='http://t.me/military_az'><strong>AАF</strong></a><strong> | </strong><a href='https://t.me/joinchat/TCl5uh3G0Mhx42Kd'><strong>Чат24/7</strong></a><strong> |</strong><a href='https://t.me/AslanAslanoff'><strong>Сотрудничество</strong></a>",
                           "🇦🇿"),

    # Unclear
    -1001658917464: Source("KhersonNonFake", "</strong><strong>@kherson_non_fake</strong>", "🇺🇦"),
    -1001731636769: Source("Batalion «Monako»", "<a href='https://t.me/+un4Mel3_naU1ZjZi'>Батальон «Монако» 💎</a>"),
    -1001602838096: Source("KronikaBpla", ),
    -1001689244469: Source("UMF"),

}
