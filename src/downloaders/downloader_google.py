from parsers.google_parser_v3 import GoogleParser_v3

url = "https://www.google.com/search?q="
suf_url = "&gs_l=psy-ab.3..0i67k1j0i131k1j0l2j0i131k1j0l2j0i131k1j0l2.829898.832060.0.832979.8.8.0.0.0.0.169.737.7j1.8.0....0...1.1.64.psy-ab..0.8.735...35i39k1.0.cGY3eIJaieU"

request_list = ["сбербанк+онлайн",
                "танки+онлайн",
                "яндекс+маркет",
                "одноклассники.мобильная+версия",
                "спорт+экспресс",
                "скачать+музыку",
                "поздравления+с+днем+рождения",
                "онлайн+переводчик",
                "карта+метро",
                "расписание+электричек",
                "игры+онлайн",
                "яндекс+пробки",
                "смотреть+фильм",
                "скачать+музыку+бесплатно",
                "программа+тв",
                "прогноз+погоды",
                "отслеживание+почтовых+отправлений",
                "курс+доллара",
                "фотошоп+онлайн",
                "точное+время",
                "теория+большого+взрыва",
                "с+днем+рождения",
                "эротические+рассказы",
                "электронный+журнал",
                "скачать+игры",
                "карта+москвы",
                "футбол+онлайн",
                "сбербанк+бизнес+онлайн",
                "расписание+поездов",
                "работа+в+москве",
                "маша+и+медведь+все+серии",
                "гороскоп+на+сегодня",
                "скачать+фильмы",
                "скачать+бесплатно+музыку",
                "санкт+петербург",
                "продажа+авто",
                "игровые+автоматы",
                "сайт+знакомств",
                "обои+для+рабочего+стола",
                "кредитный+калькулятор",
                "конвертер+валют",
                "яндекс+переводчик",
                "совместные+покупки",
                "свадебные+платья",
                "игры+бесплатно",
                "пдд+онлайн",
                "новости+украины",
                "дешевые+авиабилеты",
                "работа+на+дому",
                "смотреть+фильмы"]

for i in range(len(request_list)):

    full_url = url + request_list[i] + suf_url
    file_name = "../../golden/google/" + str(i)
    """
    response = requests.get(full_url)
    with open(file_name + ".html", "w") as file:
        file.write(response.text)
    """
    print("i =", i)
    parser = GoogleParser_v3()
    with open(file_name + ".json", "w") as file:
        with open(file_name + ".html", "r") as input:
            file.write(str(parser.parse(input.read())))
    with open(file_name + "_markup.json", "w") as file:
        file.write(str(parser.extract_markup(file_name + ".html")))
