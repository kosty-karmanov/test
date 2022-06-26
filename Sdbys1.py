import glob
import json
import os
import string
import random

import discord
from discord.ext import commands
import asyncio

from javascript import On, Once

from help import *

myname = str(os.path.basename(__file__)).replace(".py", "")
mineflayer = require('mineflayer')
bot = mineflayer.createBot({'host': "mc.mineblaze.net", 'username': myname, 'version': "1.16.5"})
mcData = require('minecraft-data')(bot.version)
Block = require('prismarine-block')(bot.version)
Item = require('prismarine-item')(bot.version)
Vec3 = require('vec3').Vec3
pathfinder = require('mineflayer-pathfinder')
bot.loadPlugin(pathfinder.pathfinder)
movements = pathfinder.Movements(bot, mcData)
movements.blocksToAvoid.delete(mcData.blocksByName.wheat.id)
bot.pathfinder.setMovements(movements)

with open('bad.txt', encoding='utf-8') as f2:
    bad = json.load(f2)
with open('settings.txt', encoding='utf-8') as f2:
    msg1 = json.load(f2)
    settings = {"mat": msg1['mat'],
                "mat_random": msg1['mat'],
                "mat_answer": msg1['mat_answer'],
                "mat_time": msg1["mat_time"],
                "reklam": msg1["reklam"],
                "reklam_random": msg1["reklam_random"],
                "reklam_msg": msg1["reklam_msg"],
                "reklam_answer": msg1["reklam_answer"],
                "reklam_time": msg1["reklam_time"],
                "mod": msg1["mod"],
                "mod_random": msg1["mod_random"],
                "mod_answer": msg1["mod_answer"],
                "mod_time": msg1["mod_time"],
                "time_for_game": msg1["time_for_game"],
                "death": ["бездну", "убит"],
                "friends": msg1["friends"],
                "my": msg1["my"],
                "my_random": msg1["my_random"],
                "my_reklam": msg1["my_reklam"],
                "chat": msg1["chat"]
                }

oldmsg = ["", ""]

ierarh = []
save = {"msg": ["", ""], "author": ["", ""]}
for name in glob.glob(r"*.py"):
    ierarh.append(name.replace(".py", ""))
filter1 = ["§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§0", "§a", "§c", "§e", "§b", "§d", "§f", "§k", "§m",
           "§o", "§l", "§n", "§r", "§F", "→", "[Всем]", "[MAGMA]" "[LEGEND]", "[Игрок]", "[GOLD]",
           "[EMERALD]", "[DIAMOND]", "▸", "■", "|"]

flags = {"time": int(datetime.datetime.today().strftime("%M")) + settings["time_for_game"], "new_game": False,
         "in_game": False, "in_party": False, "party_msg": True, "Checking": False, "is_walking": False,
         "math_start": False, "answ": 0, "math_time": int(datetime.datetime.today().strftime("%M")), "count": 2,
         "send": True}
print(f"Бот {myname} успешно запущен!")


def findAuthor(msg):
    messagenew = ""
    for i in msg:
        messagenew += i['text']
    for i in filter1:
        messagenew = messagenew.replace(i, '')
    try:
        author, message = messagenew.lstrip().split(' ', 1)
        if is_nick(author) or author in settings["friends"]:
            author = "System"
            message = messagenew.lstrip()
        return author, message
    except:
        return myname, "20221"


def is_nick(text):
    return not set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя').isdisjoint(text.lower())


def is_reklam(msg, author):
    if not flags["in_game"]:
        return
    if settings["reklam"] == "True":
        for rekmsg in settings["reklam_msg"]:
            if rekmsg in msg.lower():
                if settings["reklam_random"] == "True":
                    bot.chat(f'!{author}! {random.choice(settings["reklam_answer"])}')
                else:
                    bot.chat(f'!{author}! {settings["reklam_answer"][0]}')
                flags["time"] += settings["reklam_time"]
                return


def is_death(msg, author):
    if author == "BedWars":
        for i in settings["death"]:
            if i in msg:
                return True
    return False


def is_mat(msg, author):
    if not flags["in_game"]:
        return
    if settings["mat"] == "True":
        for i in msg.split(' '):
            if i.lower().translate(str.maketrans('', '', string.punctuation)) in bad:
                flags["time"] += settings["mat_time"]
                if settings["mat_random"] == "True":
                    bot.chat(f'!{author}, {random.choice(settings["mat_answer"])}')
                else:
                    bot.chat(f'!{author}, {settings["mat_answer"][0]}')
                break


def is_mod(msg, author):
    if not flags["in_game"]:
        return
    if settings["mod"] == "True":
        lenth = len(save["msg"]) - 2
        if is_death(save["msg"][lenth], save["author"][lenth]):
            if len(save["msg"][lenth].split(' ')) > 1:
                if author in " ".join(
                        str(save["msg"][lenth]).lstrip().split(' ')[1:len(str(save["msg"][lenth]))]) and \
                        str(save["msg"][lenth]).lstrip().split(' ')[0] in msg:
                    flags["time"] += settings["mod_time"]
                    if settings["mod_random"] == "True":
                        bot.chat(f'!{author}, {random.choice(settings["mod_answer"])}')
                    else:
                        bot.chat(f'!{author}, {settings["mod_answer"][0]}')
                    if flags["in_party"]:
                        bot.chat("/party chat Обнаружил модоюзера!")


def check_bots(msg):
    for i in ierarh:
        if i in msg and msg.split()[0] != myname and "подключился" in msg:
            if flags["in_party"]:
                bot.chat("/party chat Извините, но в эту катку зашел мой друг. Я вынужден выйти!")
            return True
    return False


def check_leave(message, author):
    if (myname in message and is_death(message, author)) or \
            (flags["time"] <= int(datetime.datetime.today().strftime("%M"))) or \
            (check_bots(message)) or \
            ("Вы присоединились к игре как наблюдатель" in message): return True
    return False


def rassilka():
    for i in settings["friends"]:
        settings["friends"][i] = "True"
    if settings["my"] == "True":
        if settings["my_random"] == "True":
            for i in random.choices(settings["my_reklam"])[0]:
                time.sleep(5)
                bot.chat(f"!Цитата рандомного чела: {i}")


def check_party(author, message):
    if "System" in author and "Пати успешно создано" in message:
        flags["in_party"] = True
    if "Party" in author:
        if "Пати расформировано" in message:
            flags["in_party"] = False
            return
        if "Вы не можете зайти в игру в одиночку" in message and flags["party_msg"]:
            flags["party_msg"] = False
            flags["in_party"] = True
            bot.chat("/party chat Попытался зайди в игру без вас. Не получилось :( Жду вас!")
            bot.chat("/spawn")
            time.sleep(1)
        for fr in settings["friends"]:
            if fr in message:
                if "Приглашение в пати от игрока" in message:
                    time.sleep(5)
                    bot.chat("/party accept")
                if "say" in message:
                    bot.chat(str(message.split('say')[1]).lstrip())
                if "add time" in message:
                    try:
                        znach = int(message.split('add time')[1])
                        flags["time"] += znach
                    except:
                        bot.chat('/party chat Ошибка! Проверьте правильность команды: add time {число (минуты)}')
                    return
                if "time" in message:
                    bot.chat(f'/party chat {flags["time"]}')
                    return
                if "set" in message:
                    try:
                        sett, znach = str(message.split('set')[1]).lstrip().split()
                        if sett in settings:
                            if znach == "True" or znach == "False":
                                settings[sett] = znach
                                bot.chat(f'/party chat Успешно изменил значение {sett} на {znach}!')
                            else:
                                bot.chat(f'/party chat Ошибка! Введено неверное значение настройки!')
                        else:
                            bot.chat(f'/party chat Ошибка! Данной настройки не существует!')
                    except:
                        bot.chat('/party chat Ошибка! Проверьте правильность команды: set {настройка} {значение}')
                if "portal" in message:
                    bot.chat(f'/party chat Понял, захожу в портал. {flags["is_walking"]} {flags["in_game"]}')
                    go_to(0, 52, 40)
                if "new game" in message:
                    bot.chat("/party chat Понял, захожу в новую игру!")
                    new_game()


def check_err(author, msg):
    if flags["in_game"] or flags["Checking"] or flags["in_party"]:
        return
    flags["Checking"] = True
    if "Извините, но вас кикнули" in msg and "System" in author:
        flags["in_game"] = False
        flags["new_game"] = False
        return
    if "Ты перемещен в лобби" in msg and "System" in author:
        time.sleep(1)
        go_to(0, 52, 40)
        return
    if "подключился к игре" in msg:
        players = int(msg.split("/")[1])
        if players < 24:
            new_game()
            print(f"[LOG] В этой игре слишком мало игроков ({players}). Перезахожу!")
            return
    lenth = len(save["author"])
    if lenth >= 20:
        for i in range(lenth - 21, lenth - 1):
            if "BedWars" in save["author"][i]:
                return
    else:
        return
    print("[LOG] - Судя по всему, бот не смог зайти в портал! 2 попытка!")
    flags["new_game"] = False
    go_to(0, 52, 40)


def new_game():
    time.sleep(1)
    flags["time"] = int(datetime.datetime.today().strftime("%M")) + settings["time_for_game"]
    flags["new_game"] = True
    flags["in_game"] = False
    flags["party_msg"] = True
    flags["Checking"] = False
    flags["math_start"] = False
    bot.chat("/leave")


def go_to(x1, y1, z1):
    if flags["in_game"] or flags["is_walking"]:
        return
    flags["is_walking"] = True
    possition = bot.entity.position
    p = bot.pathfinder
    v = Vec3(x1, y1, z1)
    t = walkTime(v, possition)
    p.setGoal(pathfinder.goals.GoalNear(v.x, v.y, v.z))
    time.sleep(t)
    p.stop()
    flags["is_walking"] = False


def start_math():
    type1 = random.randint(1, 4)
    if type1 == 1:
        time.sleep(5)
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        flags["answ"] = [a + b, 1]
        flags["math_start"] = True
        primer = f"!Решите пример и получите exp! {a} + {b} = ? Напишите только число!"
        bot.chat(primer)
    elif type1 == 2:
        time.sleep(5)
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
        flags["answ"] = [a - b, 2]
        flags["math_start"] = True
        primer = f"!Решите пример и получите exp! {a} - {b} = ? Напишите только число!"
        bot.chat(primer)
    elif type1 == 3:
        time.sleep(5)
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        flags["answ"] = [a * b, 3]
        flags["math_start"] = True
        primer = f"!Решите пример и получите exp! {a} * {b} = ? Напишите только число!"
        bot.chat(primer)
    elif type1 == 4:
        time.sleep(5)
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        flags["answ"] = [a ** b, 4]
        flags["math_start"] = True
        primer = f"!Решите пример и получите exp! {a} ^ {b} = ? Напишите только число!"
        bot.chat(primer)


@Once(bot, 'login')
def move_to_portal(*args):
    time.sleep(1)
    bot.chat("/register TEST12345 TEST12345")
    time.sleep(1)
    bot.chat("/login TEST12345")
    time.sleep(1)


@On(bot, 'kicked')
def kick(_, *args):
    print(f'[LOG] - ОШИБКА! Бота кикнуло! Причина: {args[0]}')


@On(bot, 'login')
def move_to_portal(_):
    if flags["new_game"]:
        time.sleep(1)
        print("[LOG] - Захожу в катку!")
        go_to(0, 52, 40)
        flags["new_game"] = False
        print("[LOG] - Закончил идти")
        return
    time.sleep(1)
    possition = bot.entity.position
    if possition.z == 809.5 and possition.x == 706.5:
        print("[LOG] - Захожу на сервер бедварса!")
        new_game()
        go_to(738, 73, 820)
        print("[LOG] - Зашел на сервер бедварса!")


@On(bot, 'message')
def chat(_, pos, *args):
    messages = pos['extra']
    if messages is not None:
        author, message = findAuthor(messages)
        save["msg"].append(message)
        save["author"].append(author)
        if settings["chat"] == "True":
            print(f"[{datetime.datetime.today().strftime('%H:%M')}] {author}: {message}")
        if author == myname:
            return
        is_reklam(message, author)
        is_mod(message, author)
        is_mat(message, author)
        check_party(author, message)
        check_err(author, message)
        if check_leave(message, author):
            print(f"[LOG] - Выхожу из игры")
            save["author"].append("NewGame")
            save["msg"].append("NewGame")
            new_game()
        if author in settings["friends"] and settings["friends"][author] == "True":
            bot.chat(f"!Ку, {author}!")
            settings["friends"][author] = "False"
        if "System" in author:
            if "КРОВАТНЫЕ ВОЙНЫ" in message:
                flags["in_game"] = True
                bot.chat(
                    "!Пожалуйста, не используйте читерские моды или читы в играх!")
                flags["time"] = int(datetime.datetime.today().strftime("%M")) + settings["time_for_game"]
                flags["math_time"] = int(datetime.datetime.today().strftime("%M")) + 2
                rassilka()
        if flags["math_start"]:
            try:
                if flags["answ"][0] == int(message):
                    with open('score.txt', encoding='utf-8') as f2:
                        score = json.load(f2)
                    if author not in score:
                        score[author] = flags["answ"][1]
                    else:
                        score[author] += flags["answ"][1]
                    bot.chat(f'!Верно, {author}! Ты получаешь {flags["answ"][1]} exp!')
                    flags["time"] += 4
                    flags["math_time"] = int(datetime.datetime.today().strftime("%M")) + 2
                    flags["math_start"] = False
                    with open('score.txt', 'w+', encoding='utf-8') as f1:
                        json.dump(score, f1)
            except:
                pass
        else:
            if int(datetime.datetime.today().strftime("%M")) == flags["math_time"] and flags["in_game"]:
                start_math()
