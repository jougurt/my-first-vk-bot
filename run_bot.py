import random
import time
from os import name


import vk_api
import requests
from requests import *

from config import *


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


vk_bot = vk_api.VkApi(token=ACCESS_TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']
print('готов к работе')

while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=500'.format(server=server, act='a_check', key=key,
                                                                       ts=ts)).json()
    update = long_poll['updates']
    if update[0][0] == 4:
        if update[0][6] == 'Привет':
            user_id = update[0][3]
            user_name = vk_bot.method('users.get', {'user_ids': user_id})
            write_msg(user_id,
                      'Здравствуй, ' + (user_name[0]['first_name']) + ', хочешь потренироваться? Держи рудимент!')
            write_msg(user_id, 'Как насчет single stroke roll?' + '01-single-stroke-rol(1)')
            print(str(user_name[0]['first_name']) + ' ' + str(
                user_name[0]['last_name']) + ' написал(а) боту - ' + str(
                update[0][6]))
        elif update[0][6] == 'Еще':
            user_id = update[0][3]
            user_name = vk_bot.method('users.get', {'user_ids': user_id})

            pfile = post(api.photos.getMessagesUploadServer(peer_id=update['object']['user_id'])['upload_url'],
                         files={'photo': open('01-single-stroke-roll', 'rb')}).json()
            photo = api.photos.saveMessagesPhoto(server=pfile['server'], photo=pfile['photo'],
                                                    hash=pfile['hash'])[0]
            api.messages.send(peer_id=update['object']['users_id'], message='Привет,%s &#128521;' % name,
                              attachment='photo{photo["id"]}_{photo["id"]}')
            print(str(user_name[0]['first_name']) + ' ' + str(
                user_name[0]['last_name']) + ' написал(а) боту - ' + str(
                update[0][6]))
    else:
        user_id = update[0][3]
        try:
            write_msg(user_id, 'Error')
        except Exception as e:
            print(e)
        time.sleep(5)
    ts = long_poll['ts']
