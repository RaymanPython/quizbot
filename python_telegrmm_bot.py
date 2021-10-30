import telebot
from telebot import types

# from telebot import apihelper  # Нужно для работы Proxy

# import urllib.request  # request нужен для загрузки файлов от пользователя

# botproblems = telebot.TeleBot('2077087274:AAG5wuDxn1DizPkPsZ1bqCeRLj-NbwKB4bY')  # Передаём токен из файла config.py
bot = telebot.TeleBot('2061916568:AAF6ECVmanauGayXERsBJ9tDIKUGemePxI0')  # Передаём токен из файла config.py


# apihelper.proxy = {'http': 'socks5://Proxy_User:Proxy_Password@Proxy_IP:Proxy_Port'}  # Передаём Proxy из файла config.py


class What:
    def __init__(self, name, text, answer, answers):
        self.name = name
        self.text = text
        self.answer = answer
        self.answers = answers
        self.photo = None


class Person:
    def __init__(self, name, last_name, username):
        self.name = name
        self.last_name = last_name
        self.username = username

    def __ge__(self, other):
        self.telname = other.username

    def __str__(self):
        return ' '.join([self.name, self.last_name, self.username])


Whats = [What('names', 'texts', 0, ['1', '2']), What('names1', 'texts1', 0, ['5', '55'])]
Persons = dict()
Personsname = dict()
Comand = dict()
Comandpeople = dict()
UsersOrg = ['RayGammi']
Chats = []
GO = 1


def gets_whats():
    a = dict()
    for i in Whats:
        a[i.name] = [0, 0]
    return a


def add_person(name, last_name, username):
    Personsname[username] = Person(name, last_name, username)


def add(name, x, i):
    if x > 0:
        if name not in Persons.keys():
            Comandpeople[name] = [name]
            Comand[name] = name
        Persons[name] = Persons.get(name, gets_whats())
        if Persons[name][Whats[i].name][0] == 0:
            Persons[name][Whats[i].name][0] += x
    else:
        Persons[name] = Persons.get(name, gets_whats())
        Persons[name][Whats[i].name][1] += x


def if_name(name, i):
    return Persons.get(name, gets_whats())[Whats[i].name][0] == 0


def sum_user(name):
    s = 0
    for i in Whats:
        x = sum(Persons[name][i.name])
        if x < 0:
            x = 0
        s += x
    return s


def print_Persons_i(i):
    print(Persons[i])
    return i + ' ' + ' '.join(list(map(lambda x: str(x) + ':' + str(Persons[i][x]) + ', ', Persons[i].keys())))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global GO
    # Если написали «Приветs
    if '/stop' == message.text:
        5 / 0
    elif '/result' == message.text:
        print('/result')
        a = sorted(Comandpeople.keys(), key=sum_user)
        a = a[::-1]
        for i in range(len(a)):
            bot.send_message(message.chat.id, str(i + 1) + ' место ' + a[i] + ' с балами ' + str(sum_user(a[i])))
    try:
        if message.text == "Привет" or message.text == "/start":
            bot.send_message(message.chat.id, 'Здравствуйте!' + '\n'
                             + 'Если Вы хотите узнать вопросы,  наберите команду /problems!' + '\n'
                             + 'Если Вы хотите унать свои результаты, то наберите команду /result' + '\n'
                             + 'Если же Вы хоите зарегистрировать команду, то введите /regestr название команды: никнеймы в телеграмме участников через пробел!' + '\n'
                             + 'Спасибо за участие!')
        if message.text == '/problems':
            if GO == 1:
                bot.send_message(message.from_user.id, 'Виекторина ещё неначалась!')
            elif GO == 2 or GO == 3:
                # Пишем приветствие+
                bot.send_message(message.from_user.id, "Привет, сейчас я расскажу вопросы")
                # Готовим кнопки
                keyboard = types.InlineKeyboardMarkup()
                keys = []
                for i in range(len(Whats)):
                    keys.append(types.InlineKeyboardButton(text=Whats[i].name, callback_data=str(i)))
                    # И добавляем кнопку на экран
                    keyboard.add(keys[-1])
                bot.send_message(message.from_user.id, text='Выберите название вопроса', reply_markup=keyboard)
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши Привет")
        else:
            if message.from_user.username not in UsersOrg and message.from_user.id == message.chat.id:
                bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        if '/regestr' in message.text:
            try:
                s = message.text
                s = ''.join(s.split('/regestr'))
                name, a = map(str, s.split(':'))
                name = ''.join(name.split())
                if name in Comandpeople.keys():
                    bot.send_message(message.from_user.id, "Команда " + name + " уже зарегстрированна")
                else:
                    a = a.split()
                    for i in a:
                        Comand[''.join(i.split())] = name
                    Comandpeople[name] = a
                    Persons[name] = Persons.get(name, gets_whats())
                    bot.send_message(message.from_user.id, "Команда " + name + " зарегстрированна")
            except:

                bot.send_message(message.from_user.id, "Ошибка в регистрации")
        elif '/result' == message.text:
            print('/result')
            a = sorted(Comandpeople.keys(), key=sum_user)
            a.reverse()
            for i in range(len(a)):
                if a[i] == Comand[message.from_user.username]:
                    bot.send_message(message.from_user.id,
                                     'Ваше место ' + str(i + 1) + ', ' + a[i] + ' с балами ' + str(sum_user(a[i])))
                    break
        if message.from_user.username in UsersOrg:
            # print(5)
            if '/new' in message.text:
                s = message.text[4:]
                a = []
                # print(len(s.split('\n')))
                for i in s.split('\n'):
                    # print(i)
                    if 'answers' in i:
                        answers = i.split()[1:]
                    elif 'answer' in i:
                        answer = int(i.split()[1])
                    elif 'name' in i:
                        name = i.split()[1]
                    else:
                        a.append(i)
                try:
                    Whats.append(What(name, '\n'.join(a), answer, answers))
                    for i in Persons:
                        Persons[i][name] = [0, 0]
                    bot.send_message(message.from_user.id, "Всё введено!")
                except:
                    bot.send_message(message.from_user.id, "Не всё введено!")
                # print(name)
                # print('/n'.join(a))
                # print(a)
                # print(answer)
                # print(answers)
                # print(message.text[4:])
            elif message.text == '/print':
                print(Comandpeople)
                print(Persons)
                print(Comand)
                bot.send_message(message.from_user.id, 'Whats')
                for i in Whats:
                    bot.send_message(message.from_user.id, i.name)
                bot.send_message(message.from_user.id, 'Coomandpeople')
                for i in Comandpeople:
                    bot.send_message(message.from_user.id, i + ' ' + ' '.join(Comandpeople[i]))
                bot.send_message(message.from_user.id, 'Persons')
                for i in Persons:
                    bot.send_message(message.from_user.id, print_Persons_i(i))
                    print(print_Persons_i(i))
            elif '/addorg' in message.text:
                UsersOrg.append(message.text.split()[1])
                bot.send_message(message.chat.id, 'Организатор ' + message.text.split()[1] + ' добавлен')
            elif '/result' == message.text:
                print('/result')
                a = sorted(Comandpeople.keys(), key=sum_user)
                a = a[::-1]
                for i in range(len(a)):
                    bot.send_message(message.chat.id,
                                     str(i + 1) + ' место ' + a[i] + ' с балами ' + str(sum_user(a[i])))
            elif '/go' == message.text:
                GO = 2
                bot.send_message(message.chat.id, 'Викторина началась!')
            elif '/finish' == message.text:
                GO = 3
                bot.send_message(message.chat.id, 'Викторина закончилась!')
            elif '/delp' in message.text:
                name = message.text.split()[1]
                c = True
                for i in range(len(Whats)):
                    if Whats[i].name == name:
                        Whats.pop(i)
                        bot.send_message(message.chat.id, 'Задача ' + name + ' удалена!')
                        c = False
                        break
                if c:
                    bot.send_message(message.chat.id, 'Задача ' + name + ' не найдена!')
            elif '/del' in message.text:
                name = ''.join(''.join(message.text.split('/del')).split())
                for i in Comandpeople[name]:
                    del Comand[i]
                del Comandpeople[name]
                Persons[name] = gets_whats()
                bot.send_message(message.chat.id, 'Команда ' + name + ' удалена!')
            elif '/proborg' == message.text:
                for name in UsersOrg:
                    Persons[name] = gets_whats()
                bot.send_message(message.chat.id, 'результаты организаторов онулированы')
            elif '/probx' in message.text:
                name = message.text.split()[1]
                namep = message.text.split()[2]
                x = int(message.text.split()[3])
                y = int(message.text.split()[4])
                for i in range(len(Whats)):
                    if Whats[i].name == namep:
                        k = i
                        break
                if x == 1:
                    Persons[name][namep][x] -= y
                    if Persons[name][namep][x] < 0:
                        Persons[name][namep][x] = 0
                    bot.send_message(message.chat.id,
                                     str(y) + ' попыток у команды' + name + ' с задачей' + namep + ' удалены')
                else:
                    Persons[name][namep][x] -= y
                    if Persons[name][namep][x] < 0:
                        Persons[name][namep][x] = 0
                    bot.send_message(message.chat.id, str(
                        y) + ' выигрышная попытка у команды' + name + ' с задачей' + namep + ' удалены')







    except:
        bot.send_message(message.from_user.id, 'Ошибка ввода!')


@bot.message_handler(content_types=['photo'])
def get_text_phtot(message):
    '''
    if True:
        print(5)
        #print(message)
        #message.photo[-1].file_id
        s = message.caption
        print(s)
        if  message.from_user.username in UsersOrg:
            if '/img' in s:
                name = s.split()[-1]
                k = -1
                for i in range(len(Whats)):
                    if Whats[i].name == name:
                        k = i
                        break
                if k != -1:
                    Whats[k].photo = message.photo[-1].file_id
                    bot.send_photo(message.chat.id, photo=message.photo[-1].file_id, caption='Аватарка на задачу ' + name + ' поставена!')
                else:
                    bot.send_message(message.chat.id, 'Задача не существует!')
    '''
    try:
        print(5)
        # print(message)
        # message.photo[-1].file_id
        s = message.caption
        print(s)
        if message.from_user.username in UsersOrg:
            if '/img' in s:
                name = s.split()[-1]
                k = -1
                for i in range(len(Whats)):
                    if Whats[i].name == name:
                        k = i
                        break
                if k != -1:
                    Whats[k].photo = message.photo[-1].file_id
                    bot.send_photo(message.chat.id, photo=message.photo[-1].file_id,
                                   caption='Аватарка на задачу ' + name + ' поставена!')
                else:
                    bot.send_message(message.chat.id, 'Задача не существует!')
    except:
        bot.send_message(message.chat.id, 'Ошибка вывода')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if ' ' not in call.data:
            i = int(call.data)
            if if_name(Comand.get(call.from_user.username, call.from_user.username), i):
                msg = Whats[i].text
                print(msg, call)
                # bot.send_message(call.message.chat.id, msg)
                keyboardans = types.InlineKeyboardMarkup()
                keys = []
                for j in range(len(Whats[i].answers)):
                    print(j)
                    keys.append(
                        types.InlineKeyboardButton(text=Whats[i].answers[j], callback_data=str(i) + ' ' + str(j)))
                    # И добавляем кнопку на экран
                    print(keys[-1])
                    keyboardans.add(keys[-1])
                    print(keyboardans)
                if Whats[i].photo == None:
                    bot.send_message(call.message.chat.id, text=msg, reply_markup=keyboardans)
                else:
                    bot.send_photo(call.message.chat.id, photo=Whats[i].photo)
                    bot.send_message(call.message.chat.id, text=msg, reply_markup=keyboardans)
            else:
                bot.send_message(call.message.chat.id, text='Вопрос уже выполнен!')
        else:
            if GO == 3:
                bot.send_message(call.message.chat.id, text='Викторина уже зкончилась!')
            elif GO == 2:
                i, j = map(int, call.data.split())
                if j == Whats[i].answer and if_name(Comand.get(call.from_user.username, call.from_user.username), i):
                    bot.send_message(call.message.chat.id, text='Верно!')
                    print(call.from_user)
                    # p = Person(call.from_user.first_name, call.from_user.last_name, call.from_user.username)
                    add(Comand.get(call.from_user.username, call.from_user.username), len(Whats[i].answers) - 1, i)
                    print(Persons)
                elif not if_name(Comand.get(call.from_user.username, call.from_user.username), i):
                    bot.send_message(call.message.chat.id, text='Вопрос уже выполнен!')
                else:
                    bot.send_message(call.message.chat.id, text='Неверно!')
                    add(Comand.get(call.from_user.username, call.from_user.username), -1, i)
                    print(Persons)
    except:
        bot.send_message(call.message.chat.id,
                         text='Скорее всего Вы воспользовались устаревшим сообщением, когда ддо того как удалили какую то задачу!')


# Запускаем постоянный опрос бота в Телеграме
# botproblems.polling(none_stop=True, interval=0)
bot.polling(none_stop=True, interval=0)