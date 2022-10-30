import dataclasses
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('TG_ID')
api_hash = os.getenv('TG_HASH')

DATABASE_URL = 'postgresql://postgres:area@localhost:5432/news'
POST_CHANNEL = -1001839268196


@dataclasses.dataclass
class Source:
    channel_name: str
    bloat: Optional[list[str]] = None
    bias: str = ''


OWN_SOURCES = {
    # -1001839268196:Source('Test'),  # Test
    # 1317941240:Source('MN-Bot',  # MN-bot
    -1001391125365: Source('Test2', [
        '<a href="https://t.me/+un4Mel3_naU1ZjZi">TEST-FOOTER</a>'
    ]),  # Test2
    #   -1001526741474:Source('MNChat'),  # MNChat
    -1001486678205: Source('Militär-Memes', [
        '🔰 Subscribe to @MilitaerMemes for more'
    ]),  # todo: also handle DE footer
    -1001240262412: Source('Militär-News🔰', [
        '🔰 Abonniere @MilitaerNews\n🔰 Diskutiere im @MNChat'
    ]),
}

SOURCES = {
    **OWN_SOURCES,

    # Ukrainian
    -1001452778151: Source('Krugozor', [
        '<a href="https://t.me/krugozor_news">Кругозор</a>'
    ], '🇺🇦'),
    -1001619608359: Source('TiskSnip', bias='🇺🇦'),
    -1001594428146: Source('Werochna Rada', bias='🇺🇦'),
    -1001469021333: Source('DeepState', bias='🇺🇦'),
    -1001355310059: Source('EspresoTV', bias='🇺🇦'),
    -1001759230769: Source('Bayraktar', [
        '<a href="https://t.me/+WPl-WyPpW3QyMjgy">Свежие крипто-новости тут</a>'
    ], '🇺🇦'),
    -1001201459971: Source('Rysnya', bias='🇺🇦'),
    # -1001218743574: Source('Goncharenko', bias='🇺🇦'),
    -1001413275904: Source('NEXTA', [
        'Прислать нам информацию: @nextamail_bot или info@nexta.tv\n\nПоддержать работу нашей редакции можно через\nPayPal: https://paypal.me/nexta\nPatreon: https://patreon.com/nexta_tv\nИли другие варианты (криптовалюта): https://nexta.tv/support\n\nНаш YouTube\nhttps://www.youtube.com/nexta_tv\nhttps://www.youtube.com/nexta_live\n\nНаш Twitter (In '
        'English)\nhttps://twitter.com/nexta_tv\n\nНаш TikTok\nwww.tiktok.com/@nexta_tv\n\nШойгу пошёл против Путина / Ну и новости!\nhttps://youtu.be/6T40_Ll1mMs\n\nФСБ готовит госпереворот / Ну и новости!\nhttps://youtu.be/aIiUeuTxJJs '
    ], '🇺🇦'),
    -1001011817559: Source('Militarniy', [
        '@milinua'
    ], '🇺🇦'),
    -1001414210176: Source('First Division', bias='🇺🇦'),
    -1001767825089: Source("Verteidigungsministerium UA", bias='🇺🇦'),
    -1001606301574: Source("Verteidigungsnachrichtendienst UA", bias='🇺🇦'),
    -1001223955273: Source("Luftwaffe UA", bias='🇺🇦'),
    -1001686012322: Source("Oberbefehlshaber ZSU", bias='🇺🇦'),
    -101296487842: Source('Operativu ZSU', bias='🇺🇦'),
    -1001721372338: Source("SSO", bias='🇺🇦'),
    -1001470200990: Source("Suspilne", bias='🇺🇦'),
    -1001641260594: Source("Monitor", bias='🇺🇦'),
    -1001673614390: Source("Taras Hryhorovych", bias='🇺🇦'),
    -1001727181613: Source("NMFTE", bias='🇺🇦'),

    # Russian
    -1001141171940: Source('Ramzan Kadyrow', bias='🇷🇺'),
    -1001076431027: Source('ItsDonezk', [
        '<a href="https://t.me/joinchat/QCkIs9PWI4jWPgNy">Подписаться</a>  |  <a href="https://t.me/EtoDonetsk_bot">Предложить новость</a>',
        '<a href="https://t.me/joinchat/QCkIs9PWI4jWPgNy">Подписаться</a>  |  <a href="https://t.me/EtoDonetsk_bot">Предложить новость</a>'
    ], '🇷🇺'),
    -1001260622817: Source('Readovka', bias='🇷🇺'),
    -1001149896996: Source('Interfax', [
        '@interfaxonline'
    ], '🇷🇺'),
    -1001543896043: Source('Russia Medwed', [
        'Вся ЖЕСТЬ СВО у нас в резерве 👉 <a href="https://t.me/+bSe6VmuHMlthYWEy">Смотреть</a>.'
    ], '🇷🇺'),
    -1001135021433: Source('WarGonzo', [
        '@wargonzo\n\n*наш проект существует на средства подписчиков, карта для помощи\n4279 3806 9842 9521',
        '@wargonzo\n\n<em>*наш проект существует на средства подписчиков, карта для помощи</em>\n4279 3806 9842 9521'
    ], '🇷🇺'),
    -1001708761316: Source('Prjamoy Efir',
                           ['<a href="https://t.me/+jQvaOFH1zhAzMzIy">Прямой эфир - подписаться</a>'],
                           '🇷🇺'),
    -1001382288937: Source('BalkanSniper', [
        '@balkanossiper — задаём мировые тренды с 28 июня 1914 года'
    ], '🇷🇺'),
    -1001099737840: Source('Rusvesna', [
        '<a href="<strong>t.me/rusvesnasu</strong>"><strong>t.me/rusvesnasu</strong></a>'
    ], '🇷🇺'),
    -1001326223284: Source('Rybar', [
        '@rybar\n\n<em>*Поддержать нас: </em><code>4377 7278 0407 7977</code>',
        '@rybar совместно с @voin_dv\n\n*<em>Поддержать нас:</em> <code>4377 7278 0407 7977</code> pattern :::: @ryba\n\n<em>*Поддержать нас: <\/em><code>4377 7278 0407 7977<\/code>'
    ], '🇷🇺'),
    -1001730870551: Source('Reverse Side of the Medal', [
        'Война История Оружие\nПодписаться на канал (https://t.me/historywarweaponmain)'
    ], '🇷🇺'),

    -1001393505038: Source('Karpatska Sich', bias='🇷🇺'),
    -1001093357968: Source('Epoddubny', bias='🇷🇺'),
    -1001205641526: Source('Krieg Geschichte Waffen', [
        'Война История Оружие\n<a href="https://t.me/historywarweaponmain">Подписаться на канал</a>'
    ], '🇷🇺'),
    -1001318802260: Source('Anatolij Shtitlitz', [
        '@a_shtitlitz'
    ], '🇷🇺'),
    -1001736828635: Source('Slavyangrad', [
        '@Slavyangrad\nJoin SLG 🔺 Intelligence Briefings, Strategy and Analysis, Expert Community',
        '@Slavyangrad<strong> / </strong>SLG Spetsnaz Detachment (Inna)\nJoin SLG 🔺 Intelligence Briefings, Strategy and Analysis, Expert Community',
        '@Slavyangrad / SLG Spetsnaz Detachment (Inna)\nJoin SLG 🔺 Intelligence Briefings, Strategy and Analysis, Expert Community',
        '<strong>Join Slavyangrad</strong>',
    ], '🇷🇺'),
    -1001355540894: Source('RVoenkor', [
        '<a href="<strong>t.me/RVvoenkor</strong>"><strong>t.me/RVvoenkor</strong></a>'
    ], bias='🇷🇺'),
    -1001082968817: Source('Verteidigungsministerium RU', [
        '@mod_russia'
    ], '🇷🇺'),
    -1001074511071: Source('Außenministerium RU', bias='🇷🇺'),
    -1001584480250: Source('Troyka', bias='🇷🇺'),
    -1001101170442: Source('RIA Novosti', bias='🇷🇺'),
    -1001050820672: Source('TASS', bias='🇷🇺'),
    -1001101806611: Source('Boris Rozhin', bias='🇷🇺'),
    -1001498939244: Source('Voenacher', bias='🇷🇺'),
    -1001627480627: Source('Cyberspec News', bias='🇷🇺'),
    -1001632157043: Source('Katya Valya DNR', bias='🇷🇺'),
    -1001769400021: Source('RUSVARG', [
        '@rusvarg'
    ], '🇷🇺'),
    -1001283996236: Source('Res Ipsa Loquitur', bias='🇷🇺'),
    -1001387701698: Source('Rosich', [
        '@rosich_ru'
    ], '🇷🇺'),
    -1001475054987: Source('Notizbuch des Propagandisten', bias='🇷🇺'),
    -1001850958866: Source('Russian Lives Matter', [
        '<a href="https://t.me/+3kXxJL_C4iE3YTgy">Russian Lives Matter</a>'
    ], '🇷🇺'),

    # Polish
    -1001577023152: Source('Syrenka', [

        '@pl_syrenka — Польша не заграница'
    ], '🇵🇱🇷🇺'),

    # Azeri
    -1001261746950: Source('AAF', [
        r'<a href="http://t.me/military_az"><strong>AАF</strong></a><strong>\s*|\s*</strong><a href="https://t.me/joinchat/TCl5uh3G0Mhx42Kd"><strong>Чат24/7</strong></a><strong>\s*|\s*</strong><a href="https://t.me/AslanAslanoff"><strong>Сотрудничество</strong></a>'
    ], '🇦🇿'),

    # Armenia
    - 1001430291550: Source('Wirtschaftsministerium RA', bias='🇦🇲'),

    # Brazil
    -1001321593888: Source('Tupi Report', bias='🇧🇷'),

    # Unclear
    -1001658917464: Source('KhersonNonFake', [
        '</strong><strong>@kherson_non_fake</strong>',
        'Точную инфу срочно сюда \n👉 </strong><strong>@non_fake_ks</strong>'
    ], '🇺🇦'),
    -1001731636769: Source('Batallion Monaco', [
        '<a href="https://t.me/+un4Mel3_naU1ZjZi">Батальон «Монако» 💎</a>'
    ]),
    -1001602838096: Source('Chronik UAV'),
    -1001689244469: Source('UMF'),
    -1001253415143: Source('MariuopolNow'),
    -1001393134139: Source('Middle-east in Ukrainian', ['@MiddleEastinUkrainian']),
    - 1001175084215: Source('Ukraina.ru', bias='🇷🇺'),

}
