import math
import time

import pyrogram


def CensorPhone(obj: object) -> object:
    if hasattr(obj, "phone_number"):
        obj.phone_number = "CENSORED"
    if hasattr(obj, "from_user"):
        if hasattr(obj.from_user, "phone_number"):
            obj.from_user.phone_number = "CENSORED"
    if hasattr(obj, "reply_to_message"):
        if hasattr(obj, "from_user"):
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
