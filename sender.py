"""the logic behind sending will be stored here"""
from datetime import datetime
from pprint import pprint
import dotenv
import os
import subprocess
from game import get_openligadb_data
from exceptions import ThreemaError

dotenv.load_dotenv()


def build_threema_command_str(
    threema_id: str, threema_public_key: str, msg: str, img_path: str
) -> str:

    # message only
    if msg and not img_path:
        return f"""threema send text --to {threema_id} --to.pubkey {threema_public_key} --msg "{msg}" """

    # image only
    if not msg and img_path:
        return f"""threema send image --to {threema_id} --to.pubkey {threema_public_key} --img {img_path}"""

    # image and message
    if msg and img_path:
        return f"""threema send image --to {threema_id} --to.pubkey {threema_public_key} --img {img_path} --msg "{msg}" """

    raise ValueError("Specify a message, an image or specify both.")


def send_message(threema_id: str, threema_public_key: str, msg: str, img_path: str):

    # todo add 4x data validation!
    # watch out for \n or \\n characters!
    # is unicode allowed? how to encode?
    # make data check
    # unicode alloweed?
    # how is multilines handled?
    # check if image exists

    str_cmd = build_threema_command_str(threema_id, threema_public_key, msg, img_path)

    proc = subprocess.run(str_cmd, shell=True, capture_output=True, text=True)
    outp = proc.stdout + proc.stderr
    # check for success:
    # sometimes it's in stderr, because of the "No handler
    # for connection termination" error message
    if "Message sent" not in outp:
        raise ThreemaError(f"Message not sent:\n{outp}")


def scheduler():
    def get_all_matches_data():
        pass

    def get_todays_matches():
        return []

    def wait_until_next_day(hours: int):
        pass

    def are_there_matches_today():
        pass

    while True:

        today = datetime.now()

        matches_all = get_all_matches_data()
        if are_there_matches_today(matches_all):
            wait_until_next_day(14)
            continue

        # up to here there are matches to wait for to finish
        matches_today = read_todays_matches(matches_all)
        unfinished_matches, finished_matches = update(unfinished_matches)
        while unfinished_matches:
            unfinished_matches, finished_matches = update(unfinished_matches)
            sleep("30min")
            # breakout here, if midnight: break inner while loop

        # up to here all matches are finished

        # update tables
        # render table
        # render messages
        # send to all players

    """determines when to update the data and send to players
    after every spieltag, when all games are finished"""
    spieltage_finished = dict()
    spieltage_future = dict()

    # when initialized all match data must be retrieved
    match_data_all = get_openligadb_data(["getmatchdata", "bl1", "2022"]).json()

    # initialize all
    spieltage = {m["Group"]["GroupOrderID"]: list() for m in match_data_all}

    for m in match_data_all:
        st = m["Group"]["GroupOrderID"]
        fi = m["MatchIsFinished"]
        spieltage[st].append(fi)
    for k, v in spieltage.items():
        print(k, all(v))

    pprint(spieltage)

    # loop every spieltag
    # check for all games finished true
    # if all true: send message
    # assume finding the first unfinished game, send the message for the spieltg with all finished games
    pass


if __name__ == "__main__":
    i = 2
    name = os.environ[f"P{i}_NAME"]
    tid = os.environ[f"P{i}_ID"]
    pkey = os.environ[f"P{i}_PKEY"]
    fn = "table.png"
    msg = f"Hallo {name}, das ist der aktuelle Spielstand... \U0001F60D "

    resp1 = get_openligadb_data(["getmatchdata", "bl1", "2022"])
    resp2 = get_openligadb_data(["getmatchdata", "bl2", "2022"])
    resp3 = get_openligadb_data(["getmatchdata", "bl3", "2022"])

    games_json = resp1.json() + resp2.json() + resp3.json()

    games = dict()
    for game in games_json:
        match_date = game["MatchDateTime"].split("T")[0]
        match_id = game["MatchID"]
        match_finished = game["MatchIsFinished"]

        # build key, value pair
        if match_date not in games.keys():
            games[match_date] = [[], []]

        # add finished and unfinished games
        if match_finished:
            games[match_date][1].append(match_id)
        else:
            games[match_date][0].append(match_id)

    while True:
        today_date = datetime.now().isoformat().split("T")[0]
        if today_date not in games:

            print("not found")
    for key, value in sorted(games.items(), key=lambda x: x[0]):
        print("{} : {}".format(key, value))
    # pprint(games)
