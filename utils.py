import glob
import json
import math
import os
import shutil
import tarfile
import time
import typing

import pyrogram

config = None
with open(file="config.json", encoding="utf-8") as f:
    config = json.load(fp=f)


def PrintUser(user: typing.Union[pyrogram.Chat, pyrogram.User]) -> str:
    return (
        (user.first_name + (f" {user.last_name}" if user.last_name else ""))
        + " ("
        + (f"@{user.username} " if user.username else "")
        + f"#user{user.id})"
    )


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
    except Exception as ex:
        print(ex)
        return False


def Backup() -> str:
    # empty downloads folder
    for filename in os.listdir("./downloads"):
        file_path = os.path.join("./downloads", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as ex:
            print(f"Failed to delete {file_path}. Reason: {ex}")
    # remove previous backups
    for filename in glob.glob("./backupUserbot*"):
        os.remove(filename)

    backup_name = f"backupUserbot{int(time.time())}.tar.xz"
    with tarfile.open(backup_name, mode="w:xz") as f_tar_xz:
        # backup userbot
        for folder_name, subfolders, filenames in os.walk("./"):
            if not (folder_name.startswith("./.git") or "__pycache__" in folder_name):
                for filename in filenames:
                    if filename != backup_name and not (
                        filename.endswith(".session")
                        or filename.endswith(".session-journal")
                    ):
                        # exclude current backup and session files
                        file_path = os.path.join(folder_name, filename)
                        print(file_path)
                        f_tar_xz.add(file_path)
        # backup additional files and folders
        for file_dir in config["additional_backup"]:
            if os.path.isfile(file_dir):
                # if file backup file
                print(file_dir)
                f_tar_xz.add(file_dir)
            elif os.path.isdir(file_dir):
                # if folder backup whole folder
                for folder_name, subfolders, filenames in os.walk(file_dir):
                    for filename in filenames:
                        file_path = os.path.join(folder_name, filename)
                        print(file_path)
                        f_tar_xz.add(file_path)

    return backup_name


def SendBackup(client: pyrogram.Client, msg: pyrogram.Message = None):
    if msg:
        msg.edit_text(text="I am preparing the automatic backup.")
    else:
        msg = client.send_message(
            chat_id=client.ME.id,
            text="I am preparing the automatic backup.",
            disable_notification=True,
        )

    backup_name = Backup()

    client.send_document(
        chat_id=client.ME.id,
        document=backup_name,
        disable_notification=True,
        progress=DFromUToTelegramProgress,
        progress_args=(msg, "I am sending the automatic backup.", time.time()),
    )


def CensorPhone(obj: object) -> object:
    if hasattr(obj, "phone_number"):
        obj.phone_number = "CENSORED"
    if hasattr(obj, "from_user"):
        if hasattr(obj.from_user, "phone_number"):
            obj.from_user.phone_number = "CENSORED"
    if hasattr(obj, "reply_to_message"):
        if obj.reply_to_message:
            if hasattr(obj.reply_to_message, "from_user"):
                if hasattr(obj.reply_to_message.from_user, "phone_number"):
                    obj.reply_to_message.from_user.phone_number = "CENSORED"
    return obj


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
        return f"{B} B"
    elif KB <= B < MB:
        return f"{B/KB:.2f} KB"
    elif MB <= B < GB:
        return f"{B/MB:.2f} MB"
    elif GB <= B < TB:
        return f"{B/GB:.2f} GB"
    elif TB <= B:
        return f"{B/TB:.2f} TB"


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
    tmp = (
        (f"{days}d, " if days > 0 else "")
        + (f"{hours}h, " if hours > 0 else "")
        + (f"{minutes}m, " if minutes > 0 else "")
        + (f"{seconds}s, " if seconds > 0 else "")
        + (f"{milliseconds}ms, " if milliseconds > 0 else "")
    )
    return tmp[:-2]


def DFromUToTelegramProgress(
    current: int, total: int, msg: pyrogram.Message, text: str, start: float,
) -> None:
    """
    Use this method to update the progress of a download from/an upload to Telegram, this method is called every 512KB.
    Update message every ~4 seconds.

    current (``int``): Currently downloaded/uploaded bytes.

    total (``int``): File size in bytes.

    msg (:class:`Message <pyrogram.Message>`): The Message to update while downloading/uploading the file.

    text (``str``): Text to put into the update.

    start (``float``): Time when the operation started.


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
        progress = "[{0}{1}] {2}%\n".format(
            "".join(["█" for i in range(math.floor(percentage / 5))]),
            "".join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        tmp = progress + "{0}/{1}\n{2}/s {3}/{4}\n".format(
            SizeFormatter(b=current * 8),
            SizeFormatter(b=total * 8),
            SizeFormatter(b=speed * 8),
            elapsed_time if elapsed_time != "" else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )

        msg.edit_text(text=text + tmp)
