import os
import pytz
from sender import send_message
from datetime import datetime


def logme(msg) -> None:
    dt_ger = datetime.now(pytz.timezone("Europe/Berlin"))
    tstamp = f"{dt_ger:'%F %T.%f'}"[:-3]
    tmsg = f"{tstamp} | {msg}"
    print(tmsg)
    send_message(os.environ[f"P2_ID"], os.environ[f"P2_PKEY"], tmsg, "")
