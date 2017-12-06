from parsers.kinopoisk_parser import KinopoiskParser
import requests

url = "https://www.kinopoisk.ru/index.php?kp_query="
suf_url = ""

request_list = ["Побег из Шоушенка",
                "Зеленая миля",
                "Форрест Гамп",
                "Список Шиндлера",
                "1+1",
                "Начало",
                "Король Лев",
                "Леон",
                "Бойцовский клуб",
                "Иван Васильевич меняет профессию",
                "Жизнь прекрасна",
                "Достучаться до небес",
                "Крестный отец",
                "Игры разума",
                "Престиж",
                "Криминальное чтиво",
                "Шурик",
                "Интерстеллар",
                "Властелин колец: Возвращение Короля",
                "Гладиатор",
                "Назад в будущее",
                "Карты, деньги, два ствола",
                "Иван",
                "Поймай меня, если сможешь",
                "В бой идут одни «старики»",
                "Властелин колец: Братство кольца",
                "Бриллиантовая рука",
                "Отступники",
                "Матрица",
                "Властелин колец: Две крепости",
                "Американская история X",
                "ВАЛЛ·И",
                "Большой куш",
                "Остров проклятых",
                "Джентльмены удачи",
                "Темный рыцарь",
                "Пираты Карибского моря: Проклятие Черной жемчужины",
                "Пролетая над гнездом кукушки",
                "Пробуждение",
                "Василий",
                "12 разгневанных мужчин",
                "Титаник",
                "Хатико: Самый верный друг",
                "В джазе только девушки",
                "Унесённые призраками",
                "Запах женщины",
                "Эта замечательная жизнь",
                "Огни большого города",
                "Михаил",
                "Квентин"]

for i in range(len(request_list)):

    full_url = url + request_list[i] + suf_url
    file_name = "../../golden/kinopoisk/" + str(i)
    """
    response = requests.get(full_url)
    with open(file_name + ".html", "w") as file:
        file.write(response.text)
    """
    print("i =", i)

    parser = KinopoiskParser()
    with open(file_name + ".json", "w") as file:
        with open(file_name + ".html", "r") as input:
            file.write(str(parser.parse(input.read())))
    with open(file_name + "_markup.json", "w") as file:
        file.write(str(parser.extract_markup(file_name + ".html")))
