""" Contains the logic behind sending threema messages"""
import os
import sys
import dotenv
import requests
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
        return f"""{THREEMA_EXECUTABLE} send text --to {threema_id} --to.pubkey {threema_public_key} --msg "{msg}" """

    # image only
    if not msg and img_path:
        return f"""{THREEMA_EXECUTABLE} send image --to {threema_id} --to.pubkey {threema_public_key} --img {img_path}"""

    # image and message
    if msg and img_path:
        return f"""{THREEMA_EXECUTABLE} send image --to {threema_id} --to.pubkey {threema_public_key} --img {img_path} --msg "{msg}" """

    raise ThreemaError("Specify a message, an image or specify both.")


def send_message(
    threema_id: str,
    threema_public_key: str,
    msg: str = "",
    img_path: str = "",
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
            raise ThreemaError("Did not find specified image: '{img_path}'")

    str_cmd: str = build_threema_command_str(
        threema_id, threema_public_key, msg, img_path
    )

    print(str_cmd)
    proc: CompletedProcess = run(str_cmd, shell=True, capture_output=True, text=True)
    outp: str = proc.stdout + proc.stderr
    # check for success:
    # sometimes it's in stderr, because of the "No handler
    # for connection termination" error message
    if "Message sent" not in outp:
        raise ThreemaError(f"Message not sent:\n{outp}")


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


def get_threema_public_key(threema_id: str) -> str:
    """
    Retrieves public key for any threema user id
    """
    x = requests.get(f"https://api.threema.ch/identity/{threema_id}", verify=False)

    if x.status_code == 200:
        return x.json()["publicKey"]
    return None
