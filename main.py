import os
from datetime import datetime
from time import sleep
from typing import Deque
from collections import deque

import dotenv
from requests import Response, get
import requests

from constants import TIPPS, TEAMS, BL

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
        self.bl1 = get_openligadb_data(["getavailableteams", "bl1", "2022"])
        self.bl2 = get_openligadb_data(["getavailableteams", "bl2", "2022"])
        self.bl3 = get_openligadb_data(["getavailableteams", "bl3", "2022"])

        # concatenate all three lists and loop each item
        # each item represents a row in the bundesliga
        # tables and is of type dictionary
        bl123 = [*self.bl1.json(), *self.bl2.json(), *self.bl3.json()]

        # build places dictionary
        self.places = {row["TeamId"]: place for place, row in enumerate(bl123)}
        self.date = datetime.utcnow()


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


def get_openligadb_data(api_parameter: list[str]):
    """Returns Response Object"""

    prm = "/".join(api_parameter)
    response = get(f"https://www.openligadb.de/api/{prm}")

    if response.status_code == 200:
        return response

    print(
        f"Did not reach OpenLigaDB. Status Code: {response.status_code}",
        f"Returned Response:\n{response.text}",
    )
    return None


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


def diff2points(diff: int) -> int:
    # fmt: off
    if diff == 0:  return 3
    if diff == 1:  return 2
    if diff == 2:  return 1
    return 0
    # fmt: on


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

    print("This are the players: ")
    for p in players:
        print(p.name, p.threema_id, p.threema_public_key, p.tipps)

    state_current = LeagueState()

    for player in players:
        player.update_points(state_current)
        print(
            f"{player.name} has {sum(player.points)} points. Based on data from: {player.points_date}"
        )


if __name__ == "__main__":
    main()
    # https://github.com/dominik-bauer/TippyTippsen.git
