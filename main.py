from datetime import datetime, timedelta
from time import sleep
from game import RankingState, build_players, Matches, generate_ranking
from renderer import write_points_table_to_png
from logger import logme
import traceback
import humanize


def sleepc(seconds: int):
    logme(f"I will now wait for {humanize.precisedelta(seconds, format='%0.0f')}.")
    sleep(float(seconds))


def wait_days_until_time(days: int, hh: int, mm: int):
    """
    Will wait <days> and stops waiting up to the time specified via <hh:mm>
    local time!
    """

    time_now = datetime.now()
    time_target = datetime(
        time_now.year, time_now.month, time_now.day, hh, mm, 0
    ) + timedelta(days=days)

    # avoid negative deltas, also makes no sense to wait then
    if time_target < time_now:
        return

    timediff = time_target - time_now

    sleepc(int(timediff.total_seconds()))


def run():

    # build players
    players = build_players()

    matches = Matches()

    # start the loop for tracking games
    # times from sportschau are all UTC
    # all times are utc!
    while True:
        logme("Starting a new day!")
        today = datetime.utcnow()

        # get all matches for bl1/bl2/b3 for season 22/23
        logme("Scraping sportschau.de for todays or upcoming matches.")
        matches.update_matches()

        # check if there are matches scheduled
        if not matches.are_scheduled(today):
            logme("There are no matches scheduled for today.")
            # players.send(witz)
            wait_days_until_time(days=1, hh=12, mm=0)  # utc
            continue  # start over

        # up to here there are matches happening today
        # loop and update until all matches are finished
        logme("Found matches scheduled for today!")
        n = 0
        while not matches.are_finished(today):

            # in the first loop try to wait until the last game is finished
            if n == 0:
                dt_diff = matches.end_estimated(today) - datetime.utcnow()
                waiting_seconds = dt_diff.total_seconds()

                str_time_finish = matches.end_estimated(today).strftime("%H:%M")
                logme(
                    f"I'm estimating that all matches are finished around: {str_time_finish}"
                )

                sleepc(int(waiting_seconds))
                n = 1

            else:
                # after that keep scraping every few min
                logme("Todays matches are almost finished.")
                sleepc(30)

            matches.update_matches()

        logme("Todays matches are all finished.")
        ##############################################
        # up to here all matches of today are finished

        logme("Waiting a few seconds to be sure that sportschau.de is up-to-date.")
        sleepc(60)

        logme("Fetching data and sending the overview to all players.")
        # get fresh bundesliga tables
        todays_rankingstate = RankingState()

        # update the points of each player with new bundesliga tables
        players.update_points(todays_rankingstate)

        # build point overview dataframe
        df = generate_ranking(players)

        # render dataframe into png
        fn = f"points_overview_{datetime.now():%Y%m%d-%H%M%S}.png"
        header = ["", "", "Total", "1. Bundesliga", "2. Bundesliga", "3. Bundesliga"]
        write_points_table_to_png(df, fn, header)

        # send png to all players
        players.threema_send(
            "Hallo %name%! Ich bin zurück! Wuff Wuff was macht der Punktestand?", ""
        )
        players.threema_send(
            f"sportschau.de, {todays_rankingstate.date:%d.%m.%Y %H:%M}", fn
        )

        logme("Alle Übersichten wurden versendet.")
        wait_days_until_time(days=1, hh=12, mm=0)  # utc


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logme(str(e))
        logme(traceback.format_exc())
        logme("Tippy Tippsen will now stop working. Bye...")
        raise
