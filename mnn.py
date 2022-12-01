import configparser

import sqlite3
from telethon.sync import TelegramClient

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

from  telethon.tl.functions.channels  import  GetParticipantsRequest 
from  telethon.tl.types  import  ChannelParticipantsSearch 

import time



URL = []


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

with TelegramClient('egoisteq', api_id, api_hash) as client:
    client.session.save()

client.start()

async def pars(url):
    try:
        offset = 0
        limit = 100
        all_participants = []

        while True:
            time.sleep(1)
            participants = await client(GetParticipantsRequest(
                url, 
                ChannelParticipantsSearch(''), 
                offset, 
                limit,
                hash=0
            ))

            if not participants.users:
                break

            all_participants.extend(participants.users)
            offset += len(participants.users)
                

        all_users = []
        with open("invajt_done.txt ", "r") as file:
            invait_done = file.readlines()

        for participant in all_participants:
            if not participant.bot:
                if participant.username:
                    if '@' + participant.username + '\n' not in invait_done:
                        all_users.append('@' + participant.username + '\n')

        return all_users

    except Exception as _ex:
            print(_ex)

            
async def main():
    res_list = []
    for url in URL:
        try:
            print(url)
            all_users = await pars(url)

            for res in all_users:
                res_list.append(res)
        except Exception as _ex:
            print(_ex)
        
    print('добавление в базу данных')
    connection = sqlite3.connect("Userss.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Userss (username TEXT , numbers INTEGER, done INTEGER)")

    res_list_sort = []

    for user in res_list:
        if user not in res_list_sort:
            res_list_sort.append(user)
    
    res_list.sort()
    res_list_sort.sort()

    n = 0
    while True:
        try:
            if res_list_sort[0] == res_list[0]:
                del res_list[0]
                n += 1
            else:
                cursor.execute(f"INSERT INTO Userss VALUES ('{res_list_sort[0]}', '{n}', '0')")
                n = 0
                del res_list_sort[0]
        except Exception as _ex:
            print(_ex)
            break


    rows = cursor.execute("SELECT * FROM Userss").fetchall()
    connection.commit()
    connection.close()
    print('done')


with client:
    client.loop.run_until_complete(main())



