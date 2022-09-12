from multiprocessing.sharedctypes import Value
from pprint import pprint
import os
from datetime import datetime, timedelta
from typing import Deque
from collections import deque
import pandas as pd
import dotenv
from requests import Response, get
from exceptions import OpenLigaDbError
from renderer import df_to_png
from constants import TIPPS, TEAMS, BL
from openligadb import get_openligadb_data

dotenv.load_dotenv()

from dataclasses import dataclass, field


@dataclass
class LeagueState:

    bl1: Response = field(init=False)
    bl2: Response = field(init=False)
    bl3: Response = field(init=False)
    date: datetime = field(init=False)
    places: dict[int, int] = field(init=False)

    def __post_init__(self):
        # get the data from all three leagues
        self.bl1 = get_openligadb_data(["getbltable", "bl1", "2022"])
        self.bl2 = get_openligadb_data(["getbltable", "bl2", "2022"])
        self.bl3 = get_openligadb_data(["getbltable", "bl3", "2022"])

        # concatenate all three lists
        # each item represents a row in the
        # bundesliga rankings and is of type dictionary
        bl123 = [*self.bl1.json(), *self.bl2.json(), *self.bl3.json()]

        # build places dictionary
        self.places = {row["TeamId"]: place for place, row in enumerate(bl123)}
        self.date = datetime.now()


@dataclass
class Player:
    name: str
    threema_id: str
    threema_public_key: str
    tipps: tuple

    points: tuple[int] = field(init=False)
    points_date: datetime = field(init=False)

    def update_points(self, state: LeagueState):

        points = list()
        for p_place, p_teamid in enumerate(self.tipps):
            r_place = state.places[p_teamid]
            diff = abs(p_place - r_place)
            points.append(diff2points(diff))

        self.points = tuple(points)
        self.points_date = state.date


class Match:
    """
    Holds data of a single past, current or future match of openliga db.
    The class must be initialized by one of the following two:
     - directly by defining raw_json (dict) as received from openliga db or
     - the game id (int) from openliga db, in which case the class will
       send a request to the openligadb for the raw_json.
    """

    raw_json: dict = {}
    id: int = 0

    # id: int = field(init=False)
    start: datetime = field(init=False)
    day: datetime.date = field(init=False)
    is_finished: bool = field(init=False)
    end_estimated: datetime = field(init=False)

    def __post_init__(self):
        # handle two forbidden initializations
        if not self.id or not self.raw_json:
            raise ValueError("No attribute specified. Specify eiter id or raw_json")
        if self.id and self.raw_json:
            raise ValueError("Both attributes specified. Specify eiter id or raw_json")

        # handle the two allowed initializations
        # initialized with id (raw json must be retrieved)
        if self.id:
            self.__update_raw_json()

        # up to here the data is available
        self.__update_attributes()

    def __update_raw_json(self):
        self.raw_json = get_openligadb_data(["getmatchdata", str(self.id)])

    def __update_attributes(self):
        self.id = self.raw_json["MatchID"]
        self.start = datetime.fromisoformat(self.raw_json["MatchDateTime"])
        self.day = self.start.date
        self.is_finished = self.raw_json["MatchIsFinished"]
        self.end_estimated = self.start + timedelta(minutes=90 + 15 + 5)

    def update(self):
        self.__update_raw_json()
        self.__update_attributes()


@dataclass
class Matches:
    """
    Container for any number of matches as received from OpenLigaDb
    """

    matches: list[Match] = []

    def add_match(self, m: Match):
        self.matches.append(m)

    def test(self):
        # only if a target date is set
        if type(self.target_date) is datetime.date:

            # prepare for loop by swapping variables
            matches_old, self.matches = self.matches, []

            # keep only those matches that take place on target date
            for m in matches_old:
                if m.day == self.target_date:
                    self.matches.append(m)

    def take_place_on(self, target_date: datetime.date) -> list[Match]:
        return [m for m in self.matches if m.day == target_date]

    def __update(matches: list[Match]):
        for m in matches:
            m.update()

    def __get_finished(self):
        return [m for m in self.matches if m.is_finished]

    def __get_unfinished(self):
        return [m for m in self.matches if not m.is_finished]

    def update_all(self):
        self.__update(self.matches)

    def update_unfinished(self):
        self.__update(self.__get_unfinished())

    def update_finished(self):
        self.__update(self.__get_finished())

    @property
    def are_all_finished(self):
        return all([m.is_finished for m in self.matches])

    @property
    def end_estimated(self):
        end_times = [m.end_estimated for m in self.matches]
        return max(end_times)


def build_players() -> list[Player]:

    players: list[Player] = []

    for i in range(1, 6):
        players.append(
            Player(
                os.environ[f"P{i}_NAME"],
                os.environ[f"P{i}_ID"],
                os.environ[f"P{i}_PKEY"],
                TIPPS[f"P{i}"],
            ),
        )
    return players


def split_back(l: list) -> tuple[list, list, list]:
    return l[:18], l[18:36], l[36:]


def diff2points(diff: int) -> int:
    # fmt: off
    if diff == 0:  return 3
    if diff == 1:  return 2
    if diff == 2:  return 1
    return 0
    # fmt: on


def generate_ranking(players: list[Player]) -> list[str]:
    columns = [
        "Platzierung",
        "Name",
        "Total",
        "1. Bundesliga",
        "2. Bundesliga",
        "3. Bundesliga",
    ]

    rows = []

    for player in players:

        bl1, bl2, bl3 = split_back(player.points)
        p1, p2, p3 = sum(bl1), sum(bl2), sum(bl3)
        pt = p1 + p2 + p3
        row = ["", player.name, pt, p1, p2, p3]
        rows.append(pd.DataFrame(data=[row], columns=columns))

    df = pd.concat(rows)
    df.sort_values(
        by=["Total", "1. Bundesliga", "2. Bundesliga", "3. Bundesliga"],
        ascending=False,
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)
    df.index += 1

    return df


@dataclass
class GameRunner:

    players: list[Player] = field(init=False)
    game_states: deque[LeagueState] = field(init=False)

    def __post_init__(self):
        self.players = build_players()
        self.game_states = deque(maxlen=20)

    def update_players(self):
        ls = self.game_states[-1]
        for player in self.players:
            player.update_points(ls)

    def get_player_ranking(self, ls: LeagueState) -> list:

        ranks = []
        for player in self.players:
            player.update_points(ls)
            # todo

    def send_ranking(self, ls: LeagueState):
        raise NotImplementedError

    def start(self):

        # get & add newest data
        self.game_states.append(LeagueState())

        self.update_players()

        self.update_ranking()

        sleep(20)


def get_threema_public_key(threema_id: str) -> str:
    x = get(f"https://api.threema.ch/identity/{threema_id}", verify=False)

    if x.status_code == 200:
        return x.json()["publicKey"]
    return None


# TODO: timeit list concat
def main():

    # build players first
    players = build_players()

    state_current = LeagueState()

    for player in players:
        player.update_points(state_current)
        print(f"{player.name} has {sum(player.points)} points.")
    print(f"As of {state_current.date:%Y-%m-%d %H:%M}")

    table_ranking = generate_ranking(players)
    print(table_ranking.values.tolist())

    # df_to_png(table_ranking, "test1.png")


if __name__ == "__main__":
    main()
