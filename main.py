from datetime import datetime, timedelta
import pause
from game import build_players, Match, Matches
from openligadb import get_matches_all


def wait_days_until_time(days: int, hh: int, mm: int):
    """
    Will wait <days> and stops waiting up to the time specified via <hh:mm>
    """

    time_now = datetime.now()
    time_target = datetime(
        time_now.year, time_now.month, time_now.day, hh, mm, 0
    ) + timedelta(days=days)
    pause.until(time_target)


def wait_until(time_target: datetime):
    time_now = datetime.now()
    time_diff = time_target - time_now

    """
    Will wait <days> and stops waiting up to the time specified via <hh:mm>
    """

    time_now = datetime.now()
    time_target = datetime(
        time_now.year, time_now.month, time_now.day + days, hh, mm, 0
    )
    time_diff = time_target - time_now


def run():

    # build players
    players = build_players()

    # start the loop for tracking games
    while True:

        today = datetime.now().date

        # get all matches for bl1/bl2/b3 for season 22/23
        matches = Matches()
        for raw_json in get_matches_all():
            matches.add_match(Match(raw_json))

        # check for matches that take place this day
        matches_list = matches.take_place_on(today)
        if not matches_list:
            wait_days_until_time(1, 14, 0)
            continue  # start over

        # up to here there are matches today
        matches_today = Matches(matches_list)

        # wait until all matches are finished
        while not matches_today.are_all_finished:
            # TODO: add breakout and send
            matches_today.update_unfinished()
            sleep(30 * 60)  # sleep 30 minutes

        # up to here all matches are finished

        # update tables
        # render table
        # render messages
        # send to all players


if __name__ == "__main__":
    run()
