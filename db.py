import sqlite3

conn = sqlite3.connect("posts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT,
    status TEXT
)
""")
conn.commit()


def add_post(user_id, text):
    cursor.execute(
        "INSERT INTO posts (user_id, text, status) VALUES (?, ?, ?)",
        (user_id, text, "pending")
    )
    conn.commit()
    return cursor.lastrowid


def get_post(post_id):
    cursor.execute("SELECT text FROM posts WHERE id=?", (post_id,))
    return cursor.fetchone()


def update_status(post_id, status):
    cursor.execute("UPDATE posts SET status=? WHERE id=?", (status, post_id))
    conn.commit()


def get_user_posts(user_id):
    cursor.execute("SELECT text, status FROM posts WHERE user_id=?", (user_id,))
    return cursor.fetchall()