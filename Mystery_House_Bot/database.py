import sqlite3


def add_player(user_id, name):
    progress = "S_0"
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    if not cur.execute(f"SELECT * FROM players WHERE user_id={user_id}").fetchall():
        with db:
            cur.execute(f"INSERT INTO players (user_id, name, progress) VALUES ({user_id}, '{name}', '{progress}')")
    db.close()


def get_img(user_id):
    db = sqlite3.connect("players.db")
    cur = db.cursor()
    with db:
        img_name = cur.execute(f"SELECT progress FROM players WHERE user_id={user_id}").fetchall()
    return str(img_name[0][0])


if __name__ == "__main__":
    pass
