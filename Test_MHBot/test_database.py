import sqlite3


def add_player(user_id, name):
    progress = "0_0"
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    check_prog = cur.execute(f"SELECT progress FROM players WHERE user_id={user_id}").fetchall()
    if not check_prog:
        with db:
            cur.execute(f"INSERT INTO players (user_id, name, progress, events) VALUES ({user_id}, '{name}', "
                        f"'{progress}', '')")
        db.close()
        return "0_0"
    else:
        db.close()
        return check_prog[0][0]


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


def get_events(user_id):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    with db:
        event = cur.execute(f"SELECT events FROM players WHERE user_id={user_id}").fetchall()
    db.close()
    return str(event[0][0])


def add_to_events(user_id, event):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    events = cur.execute(f"SELECT events FROM players WHERE user_id={user_id}").fetchall()
    events = events[0][0] + event + "_"
    with db:
        cur.execute(f"UPDATE players SET events='{events}' WHERE user_id={user_id}").fetchall()
    db.close()


if __name__ == "__main__":
    pass
