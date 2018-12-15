import random

import requests
import vk_api

from сonfig_ import *


def write_msg_attach(user_id, text, att_url):
    vk_bot.method('messages.send',
                  {'user_id': user_id, 'attachment': att_url, 'message': text, 'random_id': random.randint(0, 1000)})


vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']
print('готов к работе')

while True:
    long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=500'.format(server=server, act='a_check', key=key,
                                                                       ts=ts)).json()
    update = long_poll['updates']
    if 'картинк' in update[0][6]:
        user_id = update[0][3]
        write_msg_attach(user_id, 'ndjz rfhnbyrf', '1.jpg')

    ts = long_poll['ts']
