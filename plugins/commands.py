import datetime
import os
import sys
import time
import urllib

import pyrogram
import utils


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command(
        "megetip",
        prefixes=["/", "!", "#", "."],
    )
)
def CmdGetIP(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    ip = urllib.request.urlopen("https://ipecho.net/plain").read().decode("utf8")
    msg.reply_text(text=ip)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("mebackup", prefixes=["/", "!", "#", "."])
)
def CmdBackup(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    utils.SendBackup(client=client, msg=msg)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("meexec", prefixes=["/", "!", "#", "."])
)
def CmdExec(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    expression = msg.text[len(msg.command[0]) + 2 :]

    if expression:
        text = None
        try:
            text = exec(expression, dict(client=client, msg=msg))
        except Exception as ex:
            text = str(ex)

        if text:
            text = str(text)
            if len(text) > 4096:
                file_name = f"./downloads/message_too_long_{time.time()}.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(text)
                msg.reply_document(document=file_name)
                os.remove(file_name)
            else:
                msg.reply_text(text=text)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("meeval", prefixes=["/", "!", "#", "."])
)
def CmdEval(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    expression = msg.text[len(msg.command[0]) + 2 :]

    if expression:
        text = None
        try:
            text = str(eval(expression, dict(client=client, msg=msg)))
        except Exception as ex:
            text = str(ex)

        if len(text) > 4096:
            file_name = f"./downloads/message_too_long_{time.time()}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(text)
            msg.reply_document(document=file_name)
            os.remove(file_name)
        else:
            print("TEXT IS => " + text)
            msg.reply_text(text=text)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("mehelp", prefixes=["/", "!", "#", "."])
)
def CmdHelp(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    msg.edit_text(
        text="""HELP
<code>!mehelp</code>: Sends this message.
<code>!megetip</code>: Get IP of the server.
<code>!mebackup</code>: Execute the backup of the userbot and of the files and folders specified in the config.
<code>!mereboot</code>: Reboot the userbot.
<code>!meping</code>: Ping the userbot.
<code>!metodo {text}</code>: Sends {text} to yourself.
<code>!meto {media_type} {reply}</code>: Sends media|text in reply as the specified {media_type} that can be <code>animation|audio|document|photo|sticker|video|video_note|voice</code>.
<code>!mevardump [{reply}]</code>: Sends vardump of reply or actual message.
<code>!merawinfo [{id}|{username}|{reply}]</code>: Sends chosen object if possible.
<code>!meinfo [{id}|{username}|{reply}]</code>: Sends chosen object formatted properly if possible.
<code>!meeval {one_line_of_code}</code>: Returns the result of {one_line_of_code}.
<code>!meexec {code}</code>: Executes {code}.""",
        parse_mode=pyrogram.enums.parse_mode.ParseMode.HTML,
    )


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("meto", prefixes=["/", "!", "#", "."])
)
def CmdTo(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    if len(msg.command) > 1 and msg.reply_to_message:
        try:
            path = None
            if msg.reply_to_message.media:
                path = msg.reply_to_message.download()
            else:
                path = f"text_{msg.reply_to_message.id}_{time.time()}.txt"
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(msg.reply_to_message))
            if msg.command[1] == "animation":
                msg.reply_animation(animation=path)
            elif msg.command[1] == "audio":
                msg.reply_audio(audio=path)
            elif msg.command[1] == "document":
                msg.reply_document(document=path)
            elif msg.command[1] == "photo":
                msg.reply_photo(photo=path)
            elif msg.command[1] == "sticker":
                msg.reply_sticker(sticker=path)
            elif msg.command[1] == "video":
                msg.reply_video(video=path)
            elif msg.command[1] == "video_note":
                msg.reply_video_note(video_note=path)
            elif msg.command[1] == "voice":
                msg.reply_voice(voice=path)
            os.remove(path=path)
            msg.delete()
        except Exception as ex:
            msg.edit_text(text=ex)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("metodo", prefixes=["/", "!", "#", "."])
)
def CmdTodo(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    # remove the actual command
    msg.command.remove(msg.command[0])

    message = ""
    if len(msg.command) > 0:
        # reconstruct the path in case there are spaces (pyrogram.filters.command uses spaces as default separator)
        message += " ".join(msg.command)
    client.send_message(chat_id="me", text="#TODO " + message)
    if msg.reply_to_message:
        msg.reply_to_message.forward(chat_id="me")
    msg.delete()


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("mevardump", prefixes=["/", "!", "#", "."])
)
def CmdVardump(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
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


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("merawinfo", prefixes=["/", "!", "#", "."])
)
def CmdRawInfo(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    obj: pyrogram.types.User = None
    try:
        if len(msg.command) > 1:
            obj = str(
                client.get_chat(
                    chat_id=msg.command[1]
                    if not utils.IsInt(msg.command[1])
                    else int(msg.command[1])
                )
            )
        elif msg.reply_to_message:
            obj = str(client.get_chat(chat_id=msg.reply_to_message.user.id))
        else:
            obj = str(client.get_chat(chat_id=msg.chat.id))
    except Exception as ex:
        obj = ex
    msg.edit_text(text=f"INFO\n{obj}")


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("meinfo", prefixes=["/", "!", "#", "."])
)
def CmdInfo(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    # TODO ADD GROUPDATA FOR USERS
    obj: pyrogram.types.User = None
    try:
        if len(msg.command) > 1:
            obj = client.get_chat(
                chat_id=msg.command[1]
                if not utils.IsInt(msg.command[1])
                else int(msg.command[1])
            )
        elif msg.reply_to_message:
            obj = client.get_chat(chat_id=msg.reply_to_message.user.id)
        else:
            obj = client.get_chat(chat_id=msg.chat.id)

        text = f"INFO\nID: {obj.id}\nType: {obj.type}\nUsername: {obj.username}\nName: {obj.first_name}\nSurname: {obj.last_name if obj.last_name else ''}\nDescription: {obj.description}\nDate: {datetime.datetime.now().time()}"
    except Exception as ex:
        text = f"INFO\n{ex}"
    msg.edit_text(text=text)


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("meping", prefixes=["/", "!", "#", "."])
)
def CmdPing(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    # adapted from https://git.colinshark.de/PyroBot/PyroBot/src/branch/develop/pyrobot/modules/www.py
    start = datetime.datetime.utcnow()
    msg.edit_text(text="pong!")
    end = datetime.datetime.utcnow()
    msg.edit_text(
        text=f"pong!\n{utils.TimeFormatter((end - start).microseconds / 1000)}"
    )


@pyrogram.Client.on_message(
    pyrogram.filters.user("me")
    & pyrogram.filters.command("mereboot", prefixes=["/", "!", "#", "."])
)
def CmdReboot(client: pyrogram.Client, msg: pyrogram.types.Message):
    print(
        "\n[ UTC {0} ] ".format(
            datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        )
        + (
            msg.chat.title
            if msg.chat.title
            else (
                msg.chat.first_name
                + (f" {msg.chat.last_name}" if msg.chat.last_name else "")
            )
        )
        + " ("
        + (f"@{msg.chat.username} " if msg.chat.username else " ")
        + f"#chat{msg.chat.id}): "
        + msg.text
    )
    msg.delete()
    python = sys.executable
    os.execl(python, python, *sys.argv)
