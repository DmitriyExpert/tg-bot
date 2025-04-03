import telebot
from telebot import types
import config
import random

bot = telebot.TeleBot(config.TG_API_TOKEN)

user_equations = {}


@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("GitHub", url='https://github.com/DmitriyExpert')
    markup.add(button1)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Я тестовый бот! А вот github моего создателя!".format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Вот мои команды:\n/help - показать команды\n/start - запуск бота\n/rnd - рандомное число от 0 до 1.000.000 (диапазон в разработке)"
        "\n/math решение простых уравнений\n/about - информация о создателе\n/joke - рандомная шутка или анекдот",
    )


@bot.message_handler(commands=["rnd"])
def send_number(message):
    chat_id = message.chat.id
    user_equations[chat_id] = None
    bot.send_message(
        message.chat.id,
        "Введите диапазон значений через пробел (пример: 1 100)",
    )
    bot.register_next_step_handler(message, get_random)

def get_random(message):
    chat_id = message.chat.id
    equation = message.text
    user_equations[chat_id] = equation.lower()
    if equation.lower() == "stop":
        return bot.send_message(
            chat_id,
            "Вы вышли из режима вывода рандомных чисел",
        )
    if equation.count(' ') == 0 and equation[-1] != " ":
        bot.send_message(
            chat_id,
            "Числа записаны не через пробел, или последний символ равен пробелу",
        )
        bot.send_message(
            chat_id,
            "Введите еще диапазон или напишите stop для завершения ввода"
        )
        return bot.register_next_step_handler(message, get_random)
    first_num = equation[:equation.index(" ")]
    second_num = equation[equation.index(" ") + 1:]
    if first_num.isdigit() and second_num.isdigit():
        random_number = random.randint(int(first_num), int(second_num))
        bot.send_message(
            chat_id,
            random_number,
        )
        bot.send_message(
            chat_id,
            "Введите еще диапазон или напишите stop для завершения ввода"
        )
        return bot.register_next_step_handler(message, get_random)
    else:
        bot.send_message(
            chat_id,
            "Какое то из значений не является числом, введите диапазон еще раз"
        )
        return bot.register_next_step_handler(message, get_random)


@bot.message_handler(commands=["math"])
def send_number(message):
    chat_id = message.chat.id
    user_equations[chat_id] = None
    bot.send_message(
        message.chat.id,
        "Введите ваше уравнение (в уравнении должны присутствовать переменные x или y знак равенства (=)); Вводите в формате, пример: 3x = 9",
    )
    bot.register_next_step_handler(message, get_equation)


def get_equation(message):

    chat_id = message.chat.id
    equation = message.text
    user_equations[chat_id] = equation.lower()
    if equation.lower() == "stop":
        return bot.send_message(
            chat_id,
            "Вы вышли из режима решения уравнений, можно пользоваться ботом дальше!",
        )
    if len(equation) != 0 and ("x" in equation or "y" in equation) and "=" in equation:

        if equation[0] != " ":
            pass
        else:
            bot.send_message(chat_id, "Напишите без пробела в начале")
            bot.register_next_step_handler(message, get_equation)
        if (
            equation.count("x") > 1
            or equation.count("y") > 1
            or equation.count("=") > 1
        ):
            bot.send_message(
                chat_id,
                "В уравнении не может быть более одной переменной или знака равно",
            )
            bot.register_next_step_handler(message, get_equation)
        else:
            index_ravn = equation.index("=")
            if (equation[index_ravn - 1] and equation[index_ravn + 1]) != " ":
                bot.send_message(
                    chat_id,
                    "Уравнение написано не по формату: нет пробелов перед и после знака '='",
                )
                return bot.register_next_step_handler(message, get_equation)
            before_ravn = equation[: index_ravn - 1]
            after_ravn = equation[index_ravn + 2 :]
            string = before_ravn + after_ravn
            first_num = ""
            second_num = ""
            flag_ravn = 0
            for char in string:
                if flag_ravn == 0:
                    if char not in ["x", "y"]:
                        first_num += char
                    else:
                        flag_ravn = 1
                else:
                    second_num += char
            if second_num.isdigit() and first_num == "":
                bot.send_message(
                    chat_id,
                    f"Ответ на уравнение: {str(int(second_num) / 1)}, представлен с плавающей точкой",
                )
                bot.send_message(
                    chat_id,
                    f"Можете ввести еще одно уравнение, либо написать 'stop', чтобы прекратить использование /math",
                )
                return bot.register_next_step_handler(message, get_equation)
            if first_num.isdigit() and second_num.isdigit():
                bot.send_message(
                    chat_id,
                    f"Ответ на уравнение: {str(int(second_num) / int(first_num))}, представлен с плавающей точкой",
                )
                bot.send_message(
                    chat_id,
                    f"Можете ввести еще одно уравнение, либо написать 'stop', чтобы прекратить использование /math",
                )
                return bot.register_next_step_handler(message, get_equation)
            else:
                bot.send_message(
                    chat_id,
                    "Делимое или делитель, не являются числами.\n Введите уравнение еще раз или напишите 'stop'",
                )
                return bot.register_next_step_handler(message, get_equation)
    else:
        bot.send_message(
            chat_id,
            "Вы отправили пустое сообщение, или ваше сообщение не является уравнением. \nПосмотрите наличие (x или y, а также знака равно)",
        )
        bot.send_message(chat_id, "Введите уравнение еще раз")
        bot.register_next_step_handler(message, get_equation)


@bot.message_handler(commands=["about"])
def send_number(message):
    about = "Имя содателя: Дмитрий \n" "Nick name: distinkt \n" "Почта: ddpemvr@mail.ru"
    bot.send_message(message.chat.id, about)


@bot.message_handler(commands=["joke"])
def send_number(message):
    jokes = [
        "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25!",
        "Что сказала одна стена другой? Встретимся на углу!",
        "Зачем программисту очки? Чтобы видеть C#.",
        "Почему привидения так плохи во лжи? Потому что они прозрачные!",
        "Сидят два программиста. Один говорит: 'Вчера всю ночь баги ловил'. Второй: 'А я их развожу'.",
        "Что такое оптимизм? Это когда покупаешь клетку для попугая, даже если у тебя нет попугая.",
        "Штирлиц шел по улице и увидел, как падают кирпичи. 'Кирпич' - подумал Штирлиц.",
        "— Почему блондинка идет в аптеку с пустым стаканом?\n— Сдать анализ мочи на трезвость.",
        "— Что общего между программистом и динозавром?\n— Оба вымерли, но программисты еще не знают об этом.",
        "— Что такое абсолютная тишина?\n— Когда даже комары летают на mute.",
        "— Что делает программист, когда у него запор?\n— Использует команду flush.",
        "— Что такое любовь с точки зрения математики?\n— Это когда два нуля встречаются и получается восьмерка.",
        "— Как поймать уникального кролика?\n— Уникального кролика не поймаешь. Но можно попытаться поймать кролика не таким, как все.",
        "— Почему помидоры красные?\n— Потому что они стесняются, когда их раздевают.",
        "— Доктор, у меня раздвоение личности!\n— Садитесь оба.",
        "— Что такое вечность?\n— Это когда комар кусает лысого.",
        "— Что такое черный юмор?\n— Это как еда, не всем нравится.",
        "— Как называется боязнь Санта-Клауса?\n— Клаустрофобия.",
        "Идет мужик по улице, видит – лужа. Думает: 'Обойду'. Обошел. Видит – вторая лужа. Думает: 'Перепрыгну'. Перепрыгнул. Видит – третья лужа. Думает: 'Да ну ее, домой пойду'. Пришел домой, а там – потоп.",
        "– Почему у собаки нет блога?\n– Потому что она не умеет печатать.",
    ]

    randomJoke = jokes[random.randint(0, len(jokes) - 1)]
    bot.send_message(message.chat.id, randomJoke)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message_1 = "Кто ты такой?".lower()
    message_2 = "Как дела?".lower()
    message_3 = "Почему ты тут?".lower()
    if message.text.lower() == message_1:
        bot.send_message(message.chat.id, "Я бот телеграмм test")
    elif message.text.lower() == message_2:
        bot.send_message(
            message.chat.id,
            "А какие у бота могут быть дела? Живу пока не закроют программу!",
        )
    elif message.text.lower() == message_3:
        bot.send_message(message.chat.id, "Меня включил создатель!")
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды!")


bot.infinity_polling()
