import datetime
import json
import logging
import math
import os
import pprint
import re
import sys
import time

import pyrogram

import utils

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.ERROR)

info_string = "INFO\nID: {0}\nType: {1}\nUsername: {2}\nName: {3}\nSurname: {4}\nDescription: {5}\nDate: {6}"

# check telegram api key
app = pyrogram.Client(session_name="Pyrogram",
                      workers=2)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meexec", prefix=["/", "!", "#", "."]))
def CmdExec(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    expression = " ".join(msg.command[1:])

    if expression:
        text = "Done."
        try:
            result = exec(expression,
                          {"client": client, "msg": msg})
        except Exception as error:
            text = str(error)
        else:
            if result:
                text = result

        if len(text) > 4096:
            file_name = "message_too_long_{0}.txt".format(str(time.time()))
            with open(file_name, "w") as f:
                f.write(text)
            msg.reply_document(document=file_name)
            os.remove(file_name)
        else:
            msg.reply(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meeval", prefix=["/", "!", "#", "."]))
def CmdEval(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    expression = " ".join(msg.command[1:])

    if expression:
        text = "Done."
        try:
            result = eval(expression,
                          {"client": client, "msg": msg})
        except Exception as error:
            text = str(error)
        if result:
            text = result

        if len(str(text)) > 4096:
            file_name = "message_too_long_{0}.txt".format(str(time.time()))
            with open(file_name, "w") as f:
                f.write(text)
            msg.reply_document(document=file_name)
            os.remove(file_name)
        else:
            msg.reply(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mehelp", prefix=["/", "!", "#", "."]))
def CmdHelp(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    msg.edit_text(text="""HELP
<code>!mehelp</code>: Sends this message.
<code>!metodo {text}</code>: Sends {text} to yourself.
<code>!mevardump [{reply}]</code>: Sends vardump of reply or actual message.
<code>!merawinfo [{id}|{username}|{reply}]</code>: Sends chosen object if possible.
<code>!meinfo [{id}|{username}|{reply}]</code>: Sends chosen object formatted properly if possible.
<code>!meeval {one_line_of_code}</code>: Returns the result of {one_line_of_code}.
<code>!meexec {code}</code>: Executes {code}.""",
                  parse_mode="html")


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("metodo", prefix=["/", "!", "#", "."]))
def CmdTodo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    # remove the actual command
    msg.command.remove(msg.command[0])

    message = ""
    if len(msg.command) > 0:
        # reconstruct the path in case there are spaces (pyrogram.Filters.command uses spaces as default separator)
        message += " ".join(msg.command)
    client.send_message(chat_id="me",
                        text="#TODO " + message)
    if msg.reply_to_message:
        msg.reply_to_message.forward(chat_id="me")
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mevardump", prefix=["/", "!", "#", "."]))
def CmdVardump(client: pyrogram.Client,
               msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    txt = ""
    try:
        if msg.reply_to_message:
            txt = msg.reply_to_message
        txt = utils.CensorPhone(msg)
    except Exception as e:
        txt = e
    if len(str(txt)) > 4096:
        file_name = "message_too_long_{0}.txt".format(str(time.time()))
        with open(file_name, "w") as f:
            f.write(str(txt))
        msg.reply_document(document=file_name)
        msg.delete()
        os.remove(file_name)
    else:
        msg.edit_text(text="VARDUMP\n" + str(txt))


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("merawinfo", prefix=["/", "!", "#", "."]))
def CmdRawInfo(client: pyrogram.Client,
               msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " +
          msg.text)
    obj: pyrogram.User = None
    try:
        if len(msg.command) > 1:
            obj = client.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1]))
        elif msg.reply_to_message:
            obj = client.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = client.get_chat(chat_id=msg.chat.id)
        obj = utils.CensorPhone(obj)
    except Exception as e:
        obj = e
    msg.edit_text(text="INFO\n" + str(obj))


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meinfo", prefix=["/", "!", "#", "."]))
def CmdInfo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC " + datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") + "] " +
          msg.chat.title if msg.chat.title else (msg.chat.first_name + ((" " + msg.chat.last_name) if msg.chat.last_name else "")) +
          " (" + (("@" + msg.chat.username) if msg.chat.username else "") +
          " #user{0}".format(msg.chat.id) + "): " + msg.text)
    # TODO ADD GROUPDATA FOR USERS
    obj: pyrogram.User = None
    text = info_string
    try:
        if len(msg.command) > 1:
            obj = client.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1]))
        elif msg.reply_to_message:
            obj = client.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = client.get_chat(chat_id=msg.chat.id)

        text = text.format(obj.id,
                           obj.type,
                           obj.username,
                           obj.first_name,
                           obj.description,
                           datetime.datetime.now().time())
    except Exception as e:
        text = "INFO\n" + str(e)
    msg.edit_text(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mereboot", prefix=["/", "!", "#", "."]))
def CmdReboot(client: pyrogram.Client,
              msg: pyrogram.Message):
    python = sys.executable
    os.execl(python, python, *sys.argv)


app.start()
user = app.get_me()
print(user)
app.send_message(chat_id=user.id,
                 text="Bot started!\nUTC {0}".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")))
app.idle()
