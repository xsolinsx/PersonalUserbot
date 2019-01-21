import datetime
import json
import logging
import math
import os
import pprint
import re
import time

import pyrogram

import utils

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.ERROR)

print_string = "######################\n[{0}] {1}, @{2} ({3}): {4}"

# check telegram api key
app = pyrogram.Client(session_name="Pyrogram",
                      workers=2)
ERROR = "<b>Eval Expression:</b>\n<code>{0}</code>\n<b>Error:</b> {1}"
SUCCESS = "<b>Eval Expression:</b>\n<code>{0}</code>\n<b>Success</b>"
RESULT = "<b>Eval Expression:</b>\n<code>{0}</code>\n<b>Result:</b>\n<code>{1}</code>"


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="meeval", prefix=["/", "!", "#", "."]))
def CmdEval(client: pyrogram.Client,
            msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    expression = " ".join(msg.command[1:])

    if expression:
        try:
            result = eval(expression, {"client": client,
                                       "msg": msg})
        except Exception as error:
            if len(ERROR.format(expression,
                                error)) > 4096:
                file_name = "message_too_long_{0}.txt".format(str(time.time()))
                with open(file_name, "w") as f:
                    f.write(ERROR.format(expression,
                                         error))
                app.send_document(chat_id=msg.chat.id,
                                  document=file_name,
                                  reply_to_message_id=msg.message_id)
                os.remove(file_name)
            else:
                msg.reply(text=ERROR.format(expression,
                                            error),
                          parse_mode=pyrogram.ParseMode.HTML)
        else:
            if result is None:
                if len(SUCCESS.format(expression)) > 4096:
                    file_name = "message_too_long_{0}.txt".format(
                        str(time.time()))
                    with open(file_name, "w") as f:
                        f.write(SUCCESS.format(expression))
                    app.send_document(chat_id=msg.chat.id,
                                      document=file_name,
                                      reply_to_message_id=msg.message_id)
                    os.remove(file_name)
                else:
                    msg.reply(text=SUCCESS.format(expression),
                              parse_mode=pyrogram.ParseMode.HTML)
            else:
                result = utils.CensorPhone(result)
                if len(RESULT.format(expression,
                                     result)) > 4096:
                    file_name = "message_too_long_{0}.txt".format(
                        str(time.time()))
                    with open(file_name, "w") as f:
                        f.write(RESULT.format(expression,
                                              result))
                    app.send_document(chat_id=msg.chat.id,
                                      document=file_name,
                                      reply_to_message_id=msg.message_id)
                    os.remove(file_name)
                else:
                    msg.reply(text=RESULT.format(expression,
                                                 result),
                              parse_mode=pyrogram.ParseMode.HTML)
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="mehelp", prefix=["/", "!", "#", "."]))
def CmdHelp(client: pyrogram.Client,
            msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    msg.reply(text="""HELP
<code>!mehelp</code>: Sends this message.
<code>!metodo {text}</code>: Sends {text} to yourself.
<code>!mevardump [{reply}]</code>: Sends vardump of reply or actual message.
<code>!merawinfo [{id}|{username}|{reply}]</code>: Sends chosen object if possible.
<code>!meinfo [{id}|{username}|{reply}]</code>: Sends chosen object formatted properly if possible.
<code>!meeval {code}</code>: Executes code and return the result.""",
              parse_mode=pyrogram.ParseMode.HTML)
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="metodo", prefix=["/", "!", "#", "."]))
def CmdTodo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    # remove the actual command
    msg.command.remove(msg.command[0])

    message = ""
    if len(msg.command) > 0:
        # reconstruct the path in case there are spaces (pyrogram.Filters.command uses spaces as default separator)
        message += " ".join(msg.command)
    app.send_message(chat_id="me",
                     text="#TODO " + message)
    if msg.reply_to_message:
        app.forward_messages(chat_id="me",
                             from_chat_id=msg.chat.id,
                             message_ids=msg.reply_to_message.message_id)
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="mevardump", prefix=["/", "!", "#", "."]))
def CmdVardump(client: pyrogram.Client,
               msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    try:
        if msg.reply_to_message:
            msg = msg.reply_to_message
        msg = utils.CensorPhone(msg)
    except Exception as e:
        msg = e
    if len(str(msg)) > 4096:
        file_name = "message_too_long_{0}.txt".format(str(time.time()))
        with open(file_name, "w") as f:
            f.write(str(msg))
        app.send_document(chat_id=msg.chat.id,
                          document=file_name,
                          reply_to_message_id=msg.message_id)
        os.remove(file_name)
    else:
        msg.reply(text="VARDUMP\n" + str(msg))
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="merawinfo", prefix=["/", "!", "#", "."]))
def CmdRawInfo(client: pyrogram.Client,
               msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    obj: pyrogram.User = None
    try:
        if len(msg.command) > 1:
            obj = app.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1]))
        elif msg.reply_to_message:
            obj = app.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = app.get_chat(chat_id=msg.chat.id)
        obj = utils.CensorPhone(obj)
    except Exception as e:
        obj = e
    msg.reply(text="INFO\n" + str(obj))
    msg.delete()


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="meinfo", prefix=["/", "!", "#", "."]))
def CmdInfo(client: pyrogram.Client,
            msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    # TODO ADD GROUPDATA FOR USERS
    obj: pyrogram.User = None
    text = "INFO\nID: {0}\nType: {1}\nUsername: {2}\nName: {3}\nSurname: {4}\nDescription: {5}\nDate: {6}"
    try:
        if len(msg.command) > 1:
            obj = app.get_chat(chat_id=msg.command[1] if not utils.IsInt(
                msg.command[1]) else int(msg.command[1]))
        elif msg.reply_to_message:
            obj = app.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = app.get_chat(chat_id=msg.chat.id)

        type_ = obj.type
        text = text.format(obj.id,
                           obj.type,
                           obj.username,
                           obj.first_name,
                           obj.description,
                           datetime.datetime.now().time())
    except Exception as e:
        text = "INFO\n" + str(e)
    msg.reply(text=text)
    msg.delete()


app.start()
user = app.get_me()
print(user)
app.idle()