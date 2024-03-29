import os
from exceptions import ThreemaError
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from time import sleep
import pandas as pd
import dotenv
from tipps import TEAMS, TIPPS, map_enum_to_list_items
from sender import send_message
import scraper

dotenv.load_dotenv()


@dataclass
class RankingState:
    """
    With creation it will retrieve the rankings of 1., 2. and 3. Bundesliga
    and provides a dictionary with teamnames: rank. With rank being simply
    the index of the concatenated lists of teamnames 0 through 55 (n=56)
    """

    date: datetime = field(init=False)
    ranks: dict[int, int] = field(init=False)

    def __post_init__(self):
        self.update_ranking()

    def update_ranking(self):
        """
        Updates all attributes of the object, with the newest data
        available from sportschau.de.
        """
        self.teams_ranked = scraper.scrape_sportschau_ranking()
        teams_map = map_enum_to_list_items(TEAMS, self.teams_ranked)
        self.date = datetime.now()

        self.ranks = {
            teams_map[team.upper()]: n for n, team in enumerate(self.teams_ranked)
        }


@dataclass
class Player:
    """
    Holds relevant data for each player and provides a method to
    update the players current points as well as sending the
    player a threema message
    """

    name: str
    threema_id: str
    threema_public_key: str
    tipps: tuple

    send_limit: int = 5
    send_limit_time: timedelta = timedelta(hours=2)
    send_log: list[datetime] = field(default_factory=lambda: [])

    points: list[int] = field(init=False)
    points_date: datetime = field(init=False)

    def update_points(self, state: RankingState):
        """
        Accepts a RankingState object and uses that
        to update the players current points in the
        betting game
        """

        points_tmp: list[int] = []
        rank_tipp: int
        teamname: int
        rank_ref: int
        rank_diff: int

        # loop the players tipps
        for rank_tipp, teamname in enumerate(self.tipps):
            rank_ref = state.ranks[teamname]
            rank_diff = abs(rank_tipp - rank_ref)
            points_tmp.append(get_points(rank_diff))

        self.points = points_tmp[:]
        self.points_date = state.date

    def send_threema(self, message: str, image_path: str):
        dt_limit: datetime = datetime.utcnow() - self.send_limit_time
        last_sends: list[datetime] = [dt for dt in self.send_log if dt > dt_limit]
        if len(last_sends) > self.send_limit:
            print("Message not send. Limit of messages exceeded...")
            return

        try:
            send_message(
                self.threema_id,
                self.threema_public_key,
                message,
                image_path,
            )
            self.send_log.append(datetime.utcnow())
        except ThreemaError as err:
            print(err)


@dataclass
class Players:
    """
    Contains all Player objects, in order to perform actions to all of them
    in bulk
    """

    players: list[Player]
    threema_min_delay: timedelta = timedelta(hours=12)
    threema_last: datetime = datetime(year=1, month=1, day=1)

    def update_points(self, state: RankingState):
        """Updates points of all Players"""
        for p in self.players:
            p.update_points(state)

    def threema_send(self, message, image_path):
        """Send a threema message to all Players, use %name% as placeholder."""

        for p in self.players:
            if "%name%" in message:
                msg = message.replace("%name%", p.name)
            else:
                msg = message[:]

            p.send_threema(msg, image_path)
            sleep(5)
        self.threema_last = datetime.utcnow()


@dataclass
class Match:
    """
    Holds data of any single past, current or future match.
    (Only data that is relevant for efficiently triggering
    scrapes and updates is contained)
    """

    start: datetime
    is_finished: bool
    end_estimated: datetime = field(init=False)

    def __post_init__(self):
        self.end_estimated = self.start + timedelta(minutes=90 + 15 + 5)


@dataclass
class Matches:
    """
    Container for any number of matches. It provides methods to check for games
    that happen on a specific date or if those games are finished.
    """

    matches: list[Match] = field(init=False)
    last_update: datetime = field(init=False)

    def __post_init__(self):
        self.update_matches()

    def update_matches(self):
        """Retrieves a new set of matches as available from sportschau.de"""
        tmp_matches: list[Match] = []
        for start_datetime, is_finished in scraper.scrape_matches():
            tmp_matches.append(Match(start_datetime, is_finished))
        self.last_update = datetime.utcnow()
        self.matches = tmp_matches

    def get_matches(self, target_date: datetime | None) -> list[Match]:
        """
        Returns a list of all matches. If target_date is specified it
        will do that only for the matches that happend on that day
        """
        if target_date is None:
            return self.matches
        else:
            return [m for m in self.matches if m.start.date() == target_date.date()]

    def are_scheduled(self, target_date: datetime | None = None) -> bool:
        matches_to_check = self.get_matches(target_date)
        return bool(matches_to_check)

    def are_finished(self, target_date: datetime | None = None) -> bool:
        """
        Check if all self.matches are finished. If target_date is
        specified it will do that only for the matches that happen on that day
        """
        matches_to_check = self.get_matches(target_date)
        return all([m.is_finished for m in matches_to_check])

    def end_estimated(self, target_date: datetime | None = None) -> datetime:
        """
        Returns a datetime that estimates when all self.matches are presumably
        finished. If target_date is specified it will do that only for the
        matches that happen on that day
        """
        matches_to_check = self.get_matches(target_date)
        end_times = [m.end_estimated for m in matches_to_check]
        return max(end_times)


def build_players() -> Players:
    player_list: list[Player] = []

    for i in range(1, 6):
        player_list.append(
            Player(
                os.environ[f"P{i}_NAME"],
                os.environ[f"P{i}_ID"],
                os.environ[f"P{i}_PKEY"],
                TIPPS[f"P{i}"],
            ),
        )
    return Players(player_list)


def split_bl123_table_back(input_list: list) -> list[list]:
    return [input_list[:18], input_list[18:36], input_list[36:]]


def get_points(rank_difference: int) -> int:
    if rank_difference == 0:
        return 3
    if rank_difference == 1:
        return 2
    if rank_difference == 2:
        return 1
    return 0


def generate_ranking(players: Players) -> pd.DataFrame:
    columns = [
        "Spieler",
        "Total",
        "1. Bundesliga",
        "2. Bundesliga",
        "3. Bundesliga",
    ]

    rows = []

    for player in players.players:
        bl1, bl2, bl3 = split_bl123_table_back(player.points)
        p1, p2, p3 = sum(bl1), sum(bl2), sum(bl3)
        pt = p1 + p2 + p3
        row = [player.name, pt, p1, p2, p3]
        rows.append(pd.DataFrame(data=[row], columns=columns))

    df = pd.concat(rows)
    df.sort_values(
        by=["Total", "1. Bundesliga", "2. Bundesliga", "3. Bundesliga"],
        ascending=False,
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": ""})

    return df
