import datetime
import json
import logging
import math
import os
import pprint
import re
import time

import pyrogram

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.ERROR)

print_string = "######################\n[{0}] {1}, @{2} ({3}): {4}"

# check telegram api key
app = pyrogram.Client(session_name="Pyrogram",
                      workers=2)


def SizeFormatter(b: int) -> str:
    """
    Adjust the size from biys to the right measure.

    b (``int``): Number of bits.


    SUCCESS Returns the adjusted measure (``str``).
    """
    B = float(b / 8)
    KB = float(1024)
    MB = float(pow(KB, 2))
    GB = float(pow(KB, 3))
    TB = float(pow(KB, 4))

    if B < KB:
        return "{0} B".format(B)
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B/KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B/MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B/GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B/TB)


def TimeFormatter(milliseconds: int) -> str:
    """
    Adjust the time from milliseconds to the right measure.

    milliseconds (``int``): Number of milliseconds.


    SUCCESS Returns the adjusted measure (``str``).
    """
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days > 0 else "") + \
        ((str(hours) + "h, ") if hours > 0 else "") + \
        ((str(minutes) + "m, ") if minutes > 0 else "") + \
        ((str(seconds) + "s, ") if seconds > 0 else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds > 0 else "")
    return tmp[:-2]


def IsInt(v) -> bool:
    """
    Check if the parameter can be int.

    v: Variable to check.


    SUCCESS Returns ``True``.

    FAILURE Returns ``False``.
    """
    try:
        int(v)
        return True
    except Exception as e:
        print(e)
        return False


def DFromUToTelegramProgress(client: pyrogram.Client,
                             current: int,
                             total: int,
                             msg: pyrogram.Message,
                             chat_id: int or str,
                             text: str,
                             start: float) -> None:
    """
    Use this method to update the progress of a download from/an upload to Telegram, this method is called every 512KB.
    Update message every ~4 seconds.

    client (:class:`Client <pyrogram.Client>`): The Client itself.

    current (``int``): Currently downloaded/uploaded bytes.

    total (``int``): File size in bytes.

    msg (:class:`Message <pyrogram.Message>`): The Message to update while downloading/uploading the file.

    chat_id (``int`` | ``str``): Unique identifier (int) or username (str) of the target chat. For your personal cloud (Saved Messages) you can simply use "me" or "self". For a contact that exists in your Telegram address book you can use his phone number (str). For a private channel/supergroup you can use its *t.me/joinchat/* link.

    text (``str``): Text to put into the update.

    start (``str``): Time when the operation started.


    Returns ``None``.
    """
    # 1048576 is 1 MB in bytes
    now = time.time()
    diff = now - start
    if round(diff % 4.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        # 0% = [░░░░░░░░░░░░░░░░░░░░]
        # 100% = [████████████████████]
        progress = "[{0}{1}] {2}%\n".format(''.join(["█" for i in range(math.floor(percentage / 5))]),
                                            ''.join(
                                                ["░" for i in range(20 - math.floor(percentage / 5))]),
                                            round(percentage, 2))
        tmp = progress + "{0}/{1}\n{2}/s {3}/{4}\n".format(SizeFormatter(b=current * 8),
                                                           SizeFormatter(
                                                               b=total * 8),
                                                           SizeFormatter(
                                                               b=speed * 8),
                                                           elapsed_time if elapsed_time != '' else "0 s",
                                                           estimated_total_time if estimated_total_time != '' else "0 s")

        msg.edit(text=text + tmp)


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
    <code>!todo {text}</code>: Sends {text} to yourself.
    <code>!mevardump [{reply}]</code>: Sends vardump of reply or actual message.
    <code>!merawinfo [{id}|{username}|{reply}]</code>: Sends chosen object if possible.
    <code>!meinfo [{id}|{username}|{reply}]</code>: Sends chosen object formatted properly if possible.""",
              parse_mode=pyrogram.ParseMode.HTML)


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="todo", prefix=["/", "!", "#", "."]))
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


@app.on_message(pyrogram.Filters.user("me") & pyrogram.Filters.command(command="mevardump", prefix=["/", "!", "#", "."]))
def CmdVardump(client: pyrogram.Client,
               msg: pyrogram.Message):
    print(print_string.format(datetime.datetime.now().time(),
                              msg.chat.first_name,
                              msg.chat.username,
                              msg.chat.id,
                              msg.text))
    obj: pyrogram.Message = None
    try:
        if msg.reply_to_message:
            obj = app.get_messages(chat_id=msg.chat.id,
                                   message_ids=msg.reply_to_message.message_id)
        else:
            obj = msg
        if hasattr(obj.from_user, "phone_number"):
            obj.from_user.phone_number = "CENSORED"
        if hasattr(obj.chat, "phone_number"):
            obj.chat.phone_number = "CENSORED"
        if obj.reply_to_message:
            if hasattr(obj.reply_to_message.from_user, "phone_number"):
                obj.reply_to_message.from_user.phone_number = "CENSORED"
            if hasattr(obj.reply_to_message.chat, "phone_number"):
                obj.reply_to_message.chat.phone_number = "CENSORED"
    except Exception as e:
        obj = e
    if len(str(obj)) > 4096:
        file_name = "message_too_long_{0}.txt".format(str(time.time()))
        with open(file_name, "w") as f:
            f.write(str(obj))
        app.send_document(chat_id=msg.chat.id,
                          document=file_name)
        os.remove(file_name)
    else:
        msg.reply(text="VARDUMP\n" + str(obj))


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
            obj = app.get_chat(chat_id=msg.command[1])
        elif msg.reply_to_message:
            obj = app.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = app.get_chat(chat_id=msg.chat.id)
        if hasattr(obj, "phone_number"):
            obj.phone_number = "CENSORED"
    except Exception as e:
        obj = e
    msg.reply(text="INFO\n" + str(obj))


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
            obj = app.get_chat(chat_id=msg.command[1])
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


app.start()
user = app.get_me()
print(user)
app.idle()
