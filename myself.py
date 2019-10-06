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

# check telegram api key
app = pyrogram.Client(session_name="Pyrogram",
                      workers=4)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meexec", prefixes=["/", "!", "#", "."]))
def CmdExec(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    expression = " ".join(msg.command[1:])

    if expression:
        text = None
        try:
            text = exec(expression,
                        {"client": client, "msg": msg})
        except Exception as ex:
            text = str(ex)

        if text:
            text = str(text)
            if len(text) > 4096:
                file_name = f"message_too_long_{time.time()}.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(text)
                msg.reply_document(document=file_name)
                os.remove(file_name)
            else:
                msg.reply_text(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meeval", prefixes=["/", "!", "#", "."]))
def CmdEval(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    expression = " ".join(msg.command[1:])

    if expression:
        text = None
        try:
            text = str(eval(expression,
                            {"client": client, "msg": msg}))
        except Exception as ex:
            text = str(ex)

        if len(text) > 4096:
            file_name = f"message_too_long_{time.time()}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
            msg.reply_document(document=file_name)
            os.remove(file_name)
        else:
            print("TEXT IS => " + text)
            msg.reply_text(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mehelp", prefixes=["/", "!", "#", "."]))
def CmdHelp(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    msg.edit_text(text="""HELP
<code>!mehelp</code>: Sends this message.
<code>!meping</code>: Ping the userbot.
<code>!metodo {text}</code>: Sends {text} to yourself.
<code>!mevardump [{reply}]</code>: Sends vardump of reply or actual message.
<code>!merawinfo [{id}|{username}|{reply}]</code>: Sends chosen object if possible.
<code>!meinfo [{id}|{username}|{reply}]</code>: Sends chosen object formatted properly if possible.
<code>!meeval {one_line_of_code}</code>: Returns the result of {one_line_of_code}.
<code>!meexec {code}</code>: Executes {code}.""",
                  parse_mode="html")


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("metodo", prefixes=["/", "!", "#", "."]))
def CmdTodo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
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


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mevardump", prefixes=["/", "!", "#", "."]))
def CmdVardump(client: pyrogram.Client,
               msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    text = None
    try:
        if msg.reply_to_message:
            text = msg.reply_to_message
        else:
            text = msg
        text = str(utils.CensorPhone(msg))
    except Exception as ex:
        text = str(ex)
    if text:
        if len(text) > 4096:
            file_name = f"message_too_long_{time.time()}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
            msg.reply_document(document=file_name)
            msg.delete()
            os.remove(file_name)
        else:
            msg.edit_text(text=f"VARDUMP\n{text}")


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("merawinfo", prefixes=["/", "!", "#", "."]))
def CmdRawInfo(client: pyrogram.Client,
               msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    obj: pyrogram.User = None
    try:
        if len(msg.command) > 1:
            obj = str(client.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1])))
        elif msg.reply_to_message:
            obj = str(client.get_chat(chat_id=msg.reply_to_message.user.id))
        else:
            obj = str(client.get_chat(chat_id=msg.chat.id))
    except Exception as ex:
        obj = ex
    msg.edit_text(text="INFO\n" + str(obj))


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meinfo", prefixes=["/", "!", "#", "."]))
def CmdInfo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    # TODO ADD GROUPDATA FOR USERS
    obj: pyrogram.User = None
    try:
        if len(msg.command) > 1:
            obj = client.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1]))
        elif msg.reply_to_message:
            obj = client.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = client.get_chat(chat_id=msg.chat.id)

        text = f"INFO\nID: {obj.id}\nType: {obj.type}\nUsername: {obj.username}\nName: {obj.first_name}\nSurname: {obj.last_name if obj.last_name else ''}\nDescription: {obj.description}\nDate: {datetime.datetime.now().time()}"
    except Exception as ex:
        text = f"INFO\n{ex}"
    msg.edit_text(text=text)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("meping", prefixes=["/", "!", "#", "."]))
def CmdPing(client: pyrogram.Client,
            msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    msg.edit_text(text=msg.text.replace("i", "o"))


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command("mereboot", prefixes=["/", "!", "#", "."]))
def CmdReboot(client: pyrogram.Client,
              msg: pyrogram.Message):
    print("\n[ UTC {0} ] ".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")) +
          (msg.chat.title if msg.chat.title else (msg.chat.first_name + (f" {msg.chat.last_name}" if msg.chat.last_name else ""))) +
          " (" + (f"@{msg.chat.username} " if msg.chat.username else " ") +
          f"#chat{msg.chat.id}): " +
          msg.text)
    msg.delete()
    python = sys.executable
    os.execl(python, python, *sys.argv)


app.start()
app.set_parse_mode(parse_mode=None)
user = app.get_me()
print(user)
app.send_message(chat_id=user.id,
                 text="Bot started!\nUTC {0}".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")))
app.idle()
app.stop()
