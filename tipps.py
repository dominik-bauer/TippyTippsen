import enum
import difflib


# had to migrate from openligadb to
# scraping sportschau.de
# for the enum the ids of openliga db
# have been kept
@enum.unique
class TEAMS(enum.Enum):
    LEVERKUSEN = 6
    DORTMUND = 7
    SCHALKE = 9
    STUTTGART = 16
    PADERBORN = 31
    OSNABRÜCK = 36
    BAYERN_MÜNCHEN = 40
    HERTHA_BSC = 54
    HANNOVER_96 = 55
    KÖLN = 65
    ERZGEBIRGE_AUE = 66
    BRAUNSCHWEIG = 74
    KAISERSLAUTERN = 76
    MAGDEBURG = 78
    NÜRNBERG = 79
    UNION_BERLIN = 80
    MAINZ = 81
    BIELEFELD = 83
    MÖNCHENGLADBACH = 87
    FRANKFURT = 91
    AUGSBURG = 95
    ST_PAULI = 98
    HAMBURG = 100
    ROSTOCK = 102
    HOLSTEIN_KIEL = 104
    KARLSRUHE = 105
    DUISBURG = 107
    ESSEN = 109
    FREIBURG = 112
    SC_VERL = 114
    GREUTHER_FÜRTH = 115
    DARMSTADT = 118
    SANDHAUSEN = 119
    _1860_MÜNCHEN = 125
    BOCHUM = 129
    WOLFSBURG = 131
    BREMEN = 134
    INGOLSTADT = 171
    WIESBADEN = 174
    HOFFENHEIM = 175
    DRESDEN = 177
    REGENSBURG = 181
    DÜSSELDORF = 185
    DORTMUND_II = 187
    ELVERSBERG = 198
    HEIDENHEIM = 199
    HALLE = 208
    SAARBRÜCKEN = 417
    MANNHEIM = 553
    MEPPEN = 599
    OLDENBURG = 600
    LEIPZIG = 1635
    ZWICKAU = 1979
    VIKTORIA_KÖLN = 2199
    FREIBURG_II = 2397
    BAYREUTH = 2953


TIPPS: dict[str, tuple[TEAMS, ...]] = {
    "P4": (
        TEAMS.LEIPZIG,
        TEAMS.BAYERN_MÜNCHEN,
        TEAMS.LEVERKUSEN,
        TEAMS.DORTMUND,
        TEAMS.FRANKFURT,
        TEAMS.STUTTGART,
        TEAMS.KÖLN,
        TEAMS.MÖNCHENGLADBACH,
        TEAMS.BREMEN,
        TEAMS.HOFFENHEIM,
        TEAMS.WOLFSBURG,
        TEAMS.FREIBURG,
        TEAMS.MAINZ,
        TEAMS.UNION_BERLIN,
        TEAMS.AUGSBURG,
        TEAMS.HERTHA_BSC,
        TEAMS.SCHALKE,
        TEAMS.BOCHUM,
        TEAMS.HAMBURG,
        TEAMS.KAISERSLAUTERN,
        TEAMS.PADERBORN,
        TEAMS.NÜRNBERG,
        TEAMS.DÜSSELDORF,
        TEAMS.HOLSTEIN_KIEL,
        TEAMS.ST_PAULI,
        TEAMS.DARMSTADT,
        TEAMS.KARLSRUHE,
        TEAMS.REGENSBURG,
        TEAMS.SANDHAUSEN,
        TEAMS.BIELEFELD,
        TEAMS.ROSTOCK,
        TEAMS.MAGDEBURG,
        TEAMS.BRAUNSCHWEIG,
        TEAMS.HANNOVER_96,
        TEAMS.GREUTHER_FÜRTH,
        TEAMS.HEIDENHEIM,
        TEAMS._1860_MÜNCHEN,
        TEAMS.ERZGEBIRGE_AUE,
        TEAMS.MANNHEIM,
        TEAMS.INGOLSTADT,
        TEAMS.HALLE,
        TEAMS.OSNABRÜCK,
        TEAMS.DRESDEN,
        TEAMS.WIESBADEN,
        TEAMS.VIKTORIA_KÖLN,
        TEAMS.SAARBRÜCKEN,
        TEAMS.ESSEN,
        TEAMS.MEPPEN,
        TEAMS.ELVERSBERG,
        TEAMS.DORTMUND_II,
        TEAMS.BAYREUTH,
        TEAMS.DUISBURG,
        TEAMS.FREIBURG_II,
        TEAMS.OLDENBURG,
        TEAMS.ZWICKAU,
        TEAMS.SC_VERL,
    ),
    "P1": (
        TEAMS.BAYERN_MÜNCHEN,
        TEAMS.DORTMUND,
        TEAMS.LEIPZIG,
        TEAMS.LEVERKUSEN,
        TEAMS.FRANKFURT,
        TEAMS.WOLFSBURG,
        TEAMS.KÖLN,
        TEAMS.UNION_BERLIN,
        TEAMS.FREIBURG,
        TEAMS.MÖNCHENGLADBACH,
        TEAMS.MAINZ,
        TEAMS.HOFFENHEIM,
        TEAMS.BREMEN,
        TEAMS.HERTHA_BSC,
        TEAMS.SCHALKE,
        TEAMS.STUTTGART,
        TEAMS.AUGSBURG,
        TEAMS.BOCHUM,
        TEAMS.HAMBURG,
        TEAMS.ST_PAULI,
        TEAMS.HEIDENHEIM,
        TEAMS.DÜSSELDORF,
        TEAMS.GREUTHER_FÜRTH,
        TEAMS.BIELEFELD,
        TEAMS.PADERBORN,
        TEAMS.NÜRNBERG,
        TEAMS.DARMSTADT,
        TEAMS.MAGDEBURG,
        TEAMS.HOLSTEIN_KIEL,
        TEAMS.SANDHAUSEN,
        TEAMS.BRAUNSCHWEIG,
        TEAMS.HANNOVER_96,
        TEAMS.ROSTOCK,
        TEAMS.KARLSRUHE,
        TEAMS.KAISERSLAUTERN,
        TEAMS.REGENSBURG,
        TEAMS._1860_MÜNCHEN,
        TEAMS.MANNHEIM,
        TEAMS.OSNABRÜCK,
        TEAMS.DRESDEN,
        TEAMS.ZWICKAU,
        TEAMS.ESSEN,
        TEAMS.SAARBRÜCKEN,
        TEAMS.BAYREUTH,
        TEAMS.ERZGEBIRGE_AUE,
        TEAMS.INGOLSTADT,
        TEAMS.SC_VERL,
        TEAMS.HALLE,
        TEAMS.DUISBURG,
        TEAMS.FREIBURG_II,
        TEAMS.DORTMUND_II,
        TEAMS.MEPPEN,
        TEAMS.WIESBADEN,
        TEAMS.VIKTORIA_KÖLN,
        TEAMS.ELVERSBERG,
        TEAMS.OLDENBURG,
    ),
    "P3": (
        TEAMS.BAYERN_MÜNCHEN,
        TEAMS.LEIPZIG,
        TEAMS.DORTMUND,
        TEAMS.LEVERKUSEN,
        TEAMS.FRANKFURT,
        TEAMS.HERTHA_BSC,
        TEAMS.SCHALKE,
        TEAMS.FREIBURG,
        TEAMS.HOFFENHEIM,
        TEAMS.STUTTGART,
        TEAMS.WOLFSBURG,
        TEAMS.UNION_BERLIN,
        TEAMS.KÖLN,
        TEAMS.AUGSBURG,
        TEAMS.MAINZ,
        TEAMS.MÖNCHENGLADBACH,
        TEAMS.BOCHUM,
        TEAMS.BREMEN,
        TEAMS.HAMBURG,
        TEAMS.HANNOVER_96,
        TEAMS.DÜSSELDORF,
        TEAMS.KAISERSLAUTERN,
        TEAMS.REGENSBURG,
        TEAMS.PADERBORN,
        TEAMS.NÜRNBERG,
        TEAMS.BIELEFELD,
        TEAMS.HEIDENHEIM,
        TEAMS.ROSTOCK,
        TEAMS.DARMSTADT,
        TEAMS.KARLSRUHE,
        TEAMS.GREUTHER_FÜRTH,
        TEAMS.HOLSTEIN_KIEL,
        TEAMS.SANDHAUSEN,
        TEAMS.MAGDEBURG,
        TEAMS.BRAUNSCHWEIG,
        TEAMS.ST_PAULI,
        TEAMS.DRESDEN,
        TEAMS.INGOLSTADT,
        TEAMS._1860_MÜNCHEN,
        TEAMS.MANNHEIM,
        TEAMS.ERZGEBIRGE_AUE,
        TEAMS.DORTMUND_II,
        TEAMS.DUISBURG,
        TEAMS.OSNABRÜCK,
        TEAMS.VIKTORIA_KÖLN,
        TEAMS.MEPPEN,
        TEAMS.SAARBRÜCKEN,
        TEAMS.WIESBADEN,
        TEAMS.ZWICKAU,
        TEAMS.FREIBURG_II,
        TEAMS.HALLE,
        TEAMS.ESSEN,
        TEAMS.SC_VERL,
        TEAMS.OLDENBURG,
        TEAMS.ELVERSBERG,
        TEAMS.BAYREUTH,
    ),
    "P2": (
        TEAMS.DORTMUND,
        TEAMS.BAYERN_MÜNCHEN,
        TEAMS.LEIPZIG,
        TEAMS.FRANKFURT,
        TEAMS.HOFFENHEIM,
        TEAMS.LEVERKUSEN,
        TEAMS.FREIBURG,
        TEAMS.MÖNCHENGLADBACH,
        TEAMS.WOLFSBURG,
        TEAMS.KÖLN,
        TEAMS.UNION_BERLIN,
        TEAMS.HERTHA_BSC,
        TEAMS.STUTTGART,
        TEAMS.MAINZ,
        TEAMS.BREMEN,
        TEAMS.BOCHUM,
        TEAMS.AUGSBURG,
        TEAMS.SCHALKE,
        TEAMS.PADERBORN,
        TEAMS.HAMBURG,
        TEAMS.DÜSSELDORF,
        TEAMS.BIELEFELD,
        TEAMS.ST_PAULI,
        TEAMS.GREUTHER_FÜRTH,
        TEAMS.DARMSTADT,
        TEAMS.HANNOVER_96,
        TEAMS.HOLSTEIN_KIEL,
        TEAMS.NÜRNBERG,
        TEAMS.KARLSRUHE,
        TEAMS.HEIDENHEIM,
        TEAMS.MAGDEBURG,
        TEAMS.KAISERSLAUTERN,
        TEAMS.SANDHAUSEN,
        TEAMS.ROSTOCK,
        TEAMS.BRAUNSCHWEIG,
        TEAMS.REGENSBURG,
        TEAMS._1860_MÜNCHEN,
        TEAMS.DRESDEN,
        TEAMS.INGOLSTADT,
        TEAMS.ERZGEBIRGE_AUE,
        TEAMS.MANNHEIM,
        TEAMS.OSNABRÜCK,
        TEAMS.SAARBRÜCKEN,
        TEAMS.MEPPEN,
        TEAMS.ESSEN,
        TEAMS.WIESBADEN,
        TEAMS.DORTMUND_II,
        TEAMS.ZWICKAU,
        TEAMS.VIKTORIA_KÖLN,
        TEAMS.ELVERSBERG,
        TEAMS.FREIBURG_II,
        TEAMS.OLDENBURG,
        TEAMS.HALLE,
        TEAMS.DUISBURG,
        TEAMS.SC_VERL,
        TEAMS.BAYREUTH,
    ),
    "P5": (
        TEAMS.BAYERN_MÜNCHEN,
        TEAMS.LEVERKUSEN,
        TEAMS.DORTMUND,
        TEAMS.LEIPZIG,
        TEAMS.FRANKFURT,
        TEAMS.WOLFSBURG,
        TEAMS.MÖNCHENGLADBACH,
        TEAMS.HOFFENHEIM,
        TEAMS.FREIBURG,
        TEAMS.HERTHA_BSC,
        TEAMS.KÖLN,
        TEAMS.STUTTGART,
        TEAMS.SCHALKE,
        TEAMS.MAINZ,
        TEAMS.UNION_BERLIN,
        TEAMS.BREMEN,
        TEAMS.BOCHUM,
        TEAMS.AUGSBURG,
        TEAMS.NÜRNBERG,
        TEAMS.HAMBURG,
        TEAMS.DÜSSELDORF,
        TEAMS.HANNOVER_96,
        TEAMS.BIELEFELD,
        TEAMS.ST_PAULI,
        TEAMS.GREUTHER_FÜRTH,
        TEAMS.DARMSTADT,
        TEAMS.HOLSTEIN_KIEL,
        TEAMS.PADERBORN,
        TEAMS.HEIDENHEIM,
        TEAMS.SANDHAUSEN,
        TEAMS.KARLSRUHE,
        TEAMS.KAISERSLAUTERN,
        TEAMS.ROSTOCK,
        TEAMS.MAGDEBURG,
        TEAMS.REGENSBURG,
        TEAMS.BRAUNSCHWEIG,
        TEAMS._1860_MÜNCHEN,
        TEAMS.DRESDEN,
        TEAMS.INGOLSTADT,
        TEAMS.MANNHEIM,
        TEAMS.SAARBRÜCKEN,
        TEAMS.OSNABRÜCK,
        TEAMS.ERZGEBIRGE_AUE,
        TEAMS.WIESBADEN,
        TEAMS.DORTMUND_II,
        TEAMS.DUISBURG,
        TEAMS.ESSEN,
        TEAMS.HALLE,
        TEAMS.MEPPEN,
        TEAMS.ELVERSBERG,
        TEAMS.FREIBURG_II,
        TEAMS.VIKTORIA_KÖLN,
        TEAMS.ZWICKAU,
        TEAMS.BAYREUTH,
        TEAMS.OLDENBURG,
        TEAMS.SC_VERL,
    ),
}


def map_enum_to_list_items(
    enumeration: enum.EnumMeta, anylist: list[str]
) -> dict[str, int]:
    """
    Accepts an enum, and tries to match (1:1) every enum to one of the strings
    found in the anylist. Returns a dict
    """
    if len(enumeration) != len(anylist):
        raise ValueError(
            f"Enumeration ({len(enumeration)}) and list ({list(anylist)})"
            " must be of same length!"
        )

    skip_enums = []
    list_candidates = [x.upper() for x in anylist]
    mymap = {}

    for cutoff in [0.95, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05]:
        for en in enumeration:

            # check for assigned enums and skip those
            if en in skip_enums:
                continue

            # build comparable string
            elem = str(en.name).replace("_", " ").strip().upper()

            # get list of best match
            closest = difflib.get_close_matches(
                elem,
                list_candidates,
                n=1,
                cutoff=cutoff,
            )
            if closest:
                # reduce candidates
                list_candidates.remove(closest[0])

                # add enum as assigned
                skip_enums.append(en)

                # build mapping list
                mymap[closest[0]] = en

    return mymap
