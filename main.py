from datetime import datetime, timedelta
from time import sleep
from game import RankingState, build_players, Matches, generate_ranking
from renderer import write_points_table_to_png
from logger import logme


def wait_days_until_time(days: int, hh: int, mm: int):
    """
    Will wait <days> and stops waiting up to the time specified via <hh:mm>
    local time!
    """

    time_now = datetime.now()
    time_target = datetime(
        time_now.year, time_now.month, time_now.day, hh, mm, 0
    ) + timedelta(days=days)
    timediff = time_target - time_now
    sleep(timediff.total_seconds())


def run():

    # build players
    players = build_players()

    matches = Matches()

    # start the loop for tracking games
    # times from sportschau are all UTC
    # all times are utc!
    while True:
        logme("___STARTING NEW DAY___")
        today = datetime.utcnow()

        # get all matches for bl1/bl2/b3 for season 22/23
        matches.update_matches()

        # check if there are matches scheduled
        if not matches.are_scheduled(today):
            logme("There are no matches today. Wait until next day.")
            # players.send(witz)
            wait_days_until_time(days=1, hh=12, mm=0)  # utc
            continue  # start over

        # up to here there are matches happening today
        # loop and update until all matches are finished
        n = 0
        while not matches.are_finished(today):

            # in the first loop try to wait until the last game is finished
            if n == 0:
                dt_diff = matches.end_estimated(today) - datetime.utcnow()
                waiting_seconds = dt_diff.total_seconds()
                logme(
                    f"There are matches today. Waiting {waiting_seconds}s for them to end"
                )
                sleep(waiting_seconds)
                n = 1

            else:
                logme("waiting two minutes for matches to finish")
                sleep(2 * 60)

            # after that keep scraping every few min
            matches.update_matches()

        logme("There are matches today. All are finished.")
        ##############################################
        # up to here all matches of today are finished

        # wait 5 minutes so that the rankings are hopefully updated
        logme("Waiting a few minutes for bundesliga tabellen to update")
        sleep(1 * 60)

        logme("Fetching data and sending overview to all")
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
            "Hallo %name%! Ich hoffe dein Tag war so gut wie der neue Punktestand:", ""
        )
        players.threema_send(
            f"sportschau.de, {todays_rankingstate.date:%d.%m.%Y %H:%M}", fn
        )

        logme("End for Today. Wait until next day...")
        wait_days_until_time(days=1, hh=12, mm=0)  # utc


if __name__ == "__main__":

    run()
