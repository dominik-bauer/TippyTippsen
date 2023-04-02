""" Contains the logic behind sending threema messages"""
import os
import sys
import dotenv
import requests
import time
from subprocess import run, CompletedProcess
from exceptions import ThreemaError

dotenv.load_dotenv()

if sys.platform.startswith("win"):
    THREEMA_EXECUTABLE = "threema_windows.exe"
elif sys.platform.startswith("linux"):
    THREEMA_EXECUTABLE = "./threema_linux"
else:
    raise OSError(f"Platform not supported: {sys.platform}")


def build_threema_command_str(
    threema_id: str, threema_public_key: str, msg: str, img_path: str
) -> str:

    # message only
    if msg and not img_path:
        return (
            f"{THREEMA_EXECUTABLE} send text"
            + f" --to {threema_id}"
            + f" --to.pubkey {threema_public_key}"
            + f' --msg "{msg}" '
        )

    # image only
    if not msg and img_path:
        return (
            f"{THREEMA_EXECUTABLE} send image"
            + f" --to {threema_id}"
            + f" --to.pubkey {threema_public_key}"
            + f" --img {img_path}"
        )

    # image and message
    if msg and img_path:
        return (
            f"{THREEMA_EXECUTABLE} send image"
            + f" --to {threema_id}"
            + f" --to.pubkey {threema_public_key}"
            + f' --img {img_path} --msg "{msg}" '
        )

    raise ThreemaError("Specify a message, an image or specify both.")


def send_message(
    threema_id: str,
    threema_public_key: str,
    msg: str = "",
    img_path: str = "",
    retrys: int = 5,
    retry_after_seconds: int = 15,
):

    # todo add 4x data validation!
    # watch out for \n or \\n characters!
    # is unicode allowed? how to encode?
    # make data check
    # unicode alloweed?
    # how is multilines handled?
    # check if image exists

    # either message or image must be present
    if not msg and not img_path:
        raise ThreemaError("Specify message or image or both")

    # check for threema executable
    if not is_threema_executable_available():
        raise ThreemaError("Did not find threema executable")

    # check image path
    if img_path:
        if not os.path.exists(img_path):
            raise ThreemaError(f"Did not find specified image: '{img_path}'")

    str_cmd: str = build_threema_command_str(
        threema_id, threema_public_key, msg, img_path
    )

    i = 0
    outp = ""
    # retry five times
    for i in range(retrys):
        proc: CompletedProcess = run(
            str_cmd, shell=True, capture_output=True, text=True
        )
        outp: str = proc.stdout + proc.stderr
        # check for success:
        # sometimes it's in stderr, because of the "No handler
        # for connection termination" error message
        if "Message sent" in outp:
            return
        time.sleep(retry_after_seconds)

    raise ThreemaError(f"After {i} retrys the message could not be sent:\n{outp}")


def is_threema_executable_available():
    """
    Returns true if the threema executable is found
    otherwise false
    """
    proc = run(
        THREEMA_EXECUTABLE,
        shell=True,
        capture_output=True,
        text=True,
    )

    if proc.returncode == 0:
        return True

    return False


def get_threema_public_key(threema_id: str) -> str | None:
    """
    Retrieves public key for any threema user id
    """
    x = requests.get(f"https://api.threema.ch/identity/{threema_id}", verify=False)

    if x.status_code == 200:
        return x.json()["publicKey"]

    return None
