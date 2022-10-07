from datetime import datetime, timedelta
from pprint import pprint
from time import sleep
from game import RankingState, build_players, Match, Matches, generate_ranking
from renderer import df_to_png
from tipps import TEAMS, map_enum_to_list_items


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
        print("___STARTING NEW DAY___")
        today = datetime.utcnow()

        # get all matches for bl1/bl2/b3 for season 22/23
        matches.update_matches()

        # check if there are matches scheduled
        if not matches.are_scheduled(today):
            print("There are no matches today. Wait until next day.")
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
                print(
                    f"There are matches today. Waiting {waiting_seconds}s for them to end"
                )
                sleep(waiting_seconds)
                n = 1

            else:
                print("waiting two minutes for matches to finish")
                sleep(2 * 60)

            # after that keep scraping every few min
            matches.update_matches()

        print("There are matches today. All are finished.")
        ##############################################
        # up to here all matches of today are finished

        # wait 5 minutes so that the rankings are hopefully updated
        print("Waiting a few minutes for bundesliga tabellen to update")
        sleep(5 * 60)

        # get fresh bundesliga tables
        print("Update ranking state")
        todays_rankingstate = RankingState()

        # update the points of each player with new bundesliga tables
        print("Update points")
        players.update_points(todays_rankingstate)

        # build point overview dataframe
        print("building dataframe")
        df = generate_ranking(players)

        # render dataframe into png
        print("rendering png")
        fn = f"points_overview_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        df_to_png(df, fn)

        # send png to all players
        print("sending messages")
        players.threema_send(
            "Hallo und guten Abend. Ich bin Tippy Tippsen und ich schicke dir testweise die Punkteübersicht für das Bundesliga Tippspiel zu. Also du weißt schon das wo du die Bundesliga Tabellen getippt hast..."
        )
        players.threema_send("", fn)

        print("__END FOR TODAY___")


if __name__ == "__main__":

    players = build_players()
    state = RankingState()

    # update the points of each player with new bundesliga tables
    print("Update points")
    players.update_points(state)

    # build point overview dataframe
    print("building dataframe")
    df = generate_ranking(players)

    # render dataframe into png
    print("rendering png")
    fn = f"points_overview_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
    df_to_png(df, fn)

    # send png to all players
    print("sending messages")
    players.threema_send("", fn)


# run()
