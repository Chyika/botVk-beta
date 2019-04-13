#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, '../')

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import vk_api
from datetime import datetime
import random
import data
from datetime import datetime, timedelta

# login, password='login','password'
# vk_session = vk_api.VkApi(login, password)
# vk_session.auth()

vk_session = vk_api.VkApi(token=data.token_group())

# session_api = vk_session.get_api()
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)

dict_status = {}
dict_status_buy = {}
status_buy = False

def create_keyboard(response):
    global status_buy
    keyboard = VkKeyboard(one_time=False)
    status_buy

    print(str(response == '/admin' or response == 'активировать закупку'))
    if response == "/help" or response == "!начать" or response == "!старт" or response == "старт" or response == "начать" or response == "назад" or response == "/start" or response == "start" or response == "!start" or response == "команды" or response == "!команды" or response == "/команды":
        keyboard.add_button('Купить', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Продать', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пруфы', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()

        keyboard.add_button('Отключить бота', color=VkKeyboardColor.NEGATIVE)

    elif response == 'купить':
        keyboard.add_button('100к', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('500к', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('1кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('5кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Другое', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == 'продать':
        keyboard.add_button('До 1кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('1кк-5кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('5кк-15кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('От 15кк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == '/admin' and not status_buy and (event.user_id==269593957 or event.user_id==299405534  or event.user_id==150297123):
        keyboard.add_button('Активировать закупку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    elif response == '/admin' and status_buy and (event.user_id==269593957 or event.user_id==299405534  or event.user_id==150297123):
        keyboard.add_button('Дезактивировать закупку', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif (response == '/admin' or response == 'дезактивировать закупку') and status_buy and (event.user_id==269593957 or event.user_id==299405534  or event.user_id==150297123):
        if response == 'дезактивировать закупку':
            status_buy = False
        keyboard.add_button('Активировать закупку', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    elif (response == '/admin' or response == 'активировать закупку') and not status_buy and (event.user_id==269593957 or event.user_id==299405534  or event.user_id==150297123):
        if response == 'активировать закупку':
            status_buy = True
        keyboard.add_button('Дезактивировать закупку', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == 'отключить бота':
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), "%d%m%Y")
            if vk.messages.search(peer_id=event.user_id, date=tomorrow, count=1)['count'] == 1:
                vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                 message='Здравствуй! Мы рады видеть тебя здесь. Скорее пиши "Старт", чтобы активировать бота.')
            else:
                if dict_status.get(event.user_id) == None:
                    dict_status[event.user_id] = True

                print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print('Текст сообщения: ' + str(event.text))
                print(event.user_id)
                response = event.text.lower()
                keyboard = create_keyboard(response)

                if event.from_user and not event.from_me:
                    if response == "/help" or response == "!начать" or response == "!старт" or response == "старт" or response == "начать" or response == "/start" or response == "start" or response == "!start" or response == "команды" or response == "!команды" or response == "/команды":
                        dict_status[event.user_id] = True
                        dict_status_buy[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                         message='Другие доступные команды: \n\nКупить - Данная команда вызывает инструкцию для покупки VKCs.\n\nПродать - Данная подсказка вызывает инструкцию, которая помогает вам продать нам VKCs.\n\nПруфы - Данная команда предоставит вам доказательство, что мы не мошенники.\n\nСтатус - статус закупки.',
                                         keyboard=keyboard)

                    elif response == "купить" and dict_status.get(event.user_id):
                        dict_status_buy[event.user_id] = True
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Выберите товар из списка и нажмите "Написать продавцу" .\nКаталог товаров - https://vk.com/market-151512230', keyboard=keyboard)

                    elif response == "продать" and dict_status.get(event.user_id):
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Выберите сумму, которую хотите продать. Обязательно приложите скрин, доказывающий наличиe указанной суммы на вашем балансе.', keyboard=keyboard)

                    elif response == 'пруфы' and dict_status.get(event.user_id):
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Все пруфы можно найти в обсуждениях группы.\nОбсуждения - https://vk.com/board151512230')

                    elif response == "статус" and dict_status.get(event.user_id):
                        if status_buy:
                            msg = 'Закупка активна'
                        else:
                            msg = 'Закупка приостановлена'

                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message=msg)

                    elif response == 'отключить бота' and dict_status.get(event.user_id):
                        dict_status[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                         message='Если вы хотите снова включить бота, напишите "Старт"', keyboard=keyboard)

                    elif response == 'включить бота' and dict_status.get(event.user_id):
                        dict_status[event.user_id] = True
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                     message='Включить бота', keyboard=keyboard)
                    elif response == 'назад'  and dict_status.get(event.user_id):
                        dict_status_buy[event.user_id] = False
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='Выберите действие.', keyboard=keyboard)

                if event.from_user and not event.from_me:
                    if response == '100к' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423932')
                    elif response == '500к' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423937%2Fquery')
                    elif response == '1кк' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2423940%2Fquery')
                    elif response == '5кк' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='https://vk.com/market-151512230?w=product-151512230_2428516%2Fquery')
                    elif response == 'другое' and dict_status_buy.get(event.user_id) == True:
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message='Отправьте сообщение с суммой которую хотите приобрести.\nОбразец - #купить 50кк\nПисать сюда - https://vk.com/chyika2015')

                if event.from_user and not event.from_me:
                    if status_buy == True:
                        msg = 'Ожидайте ответа, я позвал администратора.'
                    else:
                        msg = 'Простите, но в данный момент скупка приостановлена.'
                    if response == 'до 1кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == '1кк-5кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == '5кк-15кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)
                    elif response == 'от 15кк':
                        vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),  message=msg)

                try:
                    if event.from_user and not event.from_me and (event.user_id==269593957 or event.user_id==299405534 or event.user_id==150297123):
                        if response == '/admin':
                            vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                         message='Админ-панель активирована.', keyboard=keyboard)
                        elif response == 'активировать закупку' and status_buy:
                            vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                             message='Статус закупки успешно изменен.', keyboard=keyboard)
                        elif response == 'дезактивировать закупку' and not status_buy:
                            vk.messages.send(peer_id=event.user_id, random_id=random.randint(-2147483648, +2147483648),
                                             message='Статус закупки успешно изменен.', keyboard=keyboard)
                except:
                    print('Error!!!!')
                print('-' * 30)

