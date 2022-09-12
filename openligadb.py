from game import Match, Matches


def get_openligadb_data(api_parameter: list[str]):
    """Returns Response Object"""

    prm = "/".join(api_parameter)
    response = get(f"https://www.openligadb.de/api/{prm}")

    if response.status_code == 200:
        return response

    raise OpenLigaDbError(
        f"Did not reach OpenLigaDB. Status Code: {response.status_code}",
        f"Returned Response:\n{response.text}",
    )


def get_matches_all() -> list[dict]:

    mbl1 = get_openligadb_data(["getmatchdata", "bl1", "2022"])
    mbl2 = get_openligadb_data(["getmatchdata", "bl2", "2022"])
    mbl3 = get_openligadb_data(["getmatchdata", "bl3", "2022"])

    return [*mbl1.json(), *mbl2.json(), *mbl3.json()]
