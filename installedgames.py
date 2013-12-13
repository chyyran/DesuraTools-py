import sqlite3
import os
from desuragame import InstalledGame

games_db = None


def init_db():
    global games_db
    games_db = sqlite3.connect(get_item_info_path()[0])


def get_item_info_path():
        desurapath = os.path.join("C:/", "ProgramData", "Desura", "DesuraApp")
        if os.path.exists(os.path.join(desurapath,"iteminfo_d.sqlite")):
            return os.path.join(desurapath, "iteminfo_d.sqlite"), True
        else:
            return os.path.join(desurapath, "iteminfo_c.sqlite"), False


def _get_games_d():
        games = []
        # 2097164
        cur = games_db.cursor().execute(
            "SELECT * FROM iteminfo "
            "WHERE statusflags = 16777246 OR statusflags = 30 OR statusflags = 26 OR statusflags = 16777242"
        )
        for result in cur.fetchall():
            name = result[6]
            shortname = result[7]
            icon = result[10]
            exe = games_db.cursor().execute("SELECT exe FROM exe WHERE itemid = '{0}' AND name = 'Play'"
                                            .format(result[0])).fetchone()[0]
            games.append(InstalledGame(shortname, name, exe, icon))
        return games


def _get_games_c():
        games = []
        # 2097164
        cur = games_db.cursor().execute("SELECT * FROM iteminfo "
                                        "WHERE statusflags = 16777246 "
                                        "OR statusflags = 30 "
                                        "OR statusflags = 26 "
                                        "OR statusflags = 16777242")
        for result in cur.fetchall():
            name = result[6]
            shortname = result[7]
            icon = result[10]
            exe = result[15]
            games.append(InstalledGame(shortname, name, exe, icon))
        return games


def get_games():
    if get_item_info_path()[1]:
        games = _get_games_d()
    else:
        games = _get_games_c()
    return games
