import sqlite3


def add_player(user_id, name):
    progress = "0_0"
    inv = "test"
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    if not cur.execute(f"SELECT * FROM players WHERE user_id={user_id}").fetchall():
        with db:
            cur.execute(f"INSERT INTO players (user_id, name, progress, invent) VALUES ({user_id}, '{name}', "
                        f"'{progress}', '')")
    db.close()


def get_progress(user_id):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    with db:
        img_name = cur.execute(f"SELECT progress FROM players WHERE user_id={user_id}").fetchall()
    db.close()
    return str(img_name[0][0])


def update_progress(user_id, p):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    with db:
        cur.execute(f"UPDATE players SET progress='{p}' WHERE user_id={user_id}").fetchall()
    db.close()


def get_inv(user_id):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    with db:
        tool = cur.execute(f"SELECT invent FROM players WHERE user_id={user_id}").fetchall()
    db.close()
    return str(tool[0][0])


def add_to_inv(user_id, tool):
    inv = get_inv(user_id)
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    inv += tool + "_"
    with db:
        cur.execute(f"UPDATE players SET invent='{inv}' WHERE user_id={user_id}").fetchall()
    db.close()


if __name__ == "__main__":
    pass
