import db

def add_ask(title, content, user_id):
    sql = """INSERT INTO asks (title, content, sent_at, user_id)
            VALUES (?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, content, user_id])

def get_asks_info():
    sql = "SELECT COUNT(a.id) total, MAX(a.sent_at) last FROM asks a"
    return db.query(sql)[0]

def get_asks():
    sql = """SELECT a.id,
                    a.title,
                    a.user_id,
                    a.sent_at,
                    u.username
            FROM asks a, users u
            WHERE a.user_id = u.id
            GROUP BY a.id
            ORDER BY a.id DESC"""
    return db.query(sql)

def get_ask(ask_id):
    sql = """SELECT a.id,
                    a.title,
                    a.content,
                    a.sent_at,
                    a.user_id,
                    u.id user_id,
                    u.username
                FROM asks a, users u
                WHERE a.user_id = u.id AND
                    a.id = ?"""
    return db.query(sql, [ask_id])[0]

def update_ask(ask_id, title, content):
    sql = """UPDATE asks SET
                            title = ?,
                            content = ?
                        WHERE id = ?"""
    db.execute(sql, [title, content, ask_id])

def remove_ask(ask_id):
    sql = "DELETE FROM asks WHERE id = ?"
    db.execute(sql, [ask_id])

def search_asks(query):
    sql = """SELECT id, title
            FROM asks
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
