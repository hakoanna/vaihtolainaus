import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(ask_id):
    sql = "SELECT title, value FROM ask_classes WHERE ask_id = ?"
    return db.query(sql, [ask_id])

def add_ask(title, content, user_id, classes):
    sql = """INSERT INTO asks (title, content, sent_at, user_id, status)
            VALUES (?, ?, datetime('now'), ?, 1)"""
    db.execute(sql, [title, content, user_id])

    ask_id = db.last_insert_id()

    sql = "INSERT INTO ask_classes (ask_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [ask_id, title, value])

def get_asks_info():
    sql = "SELECT COUNT(a.id) total, MAX(a.sent_at) last FROM asks a WHERE a.status=1"
    return db.query(sql)[0]

def get_asks():
    sql = """SELECT a.id,
                    a.title,
                    a.user_id,
                    a.sent_at,
                    u.username,
                    a.status
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
                    a.status,
                    u.id user_id,
                    u.username
                FROM asks a, users u
                WHERE a.user_id = u.id AND
                    a.id = ?"""
    result = db.query(sql, [ask_id])
    return result[0] if result else None

def update_ask(ask_id, title, content, classes):
    sql = """UPDATE asks SET
                            title = ?,
                            content = ?
                        WHERE id = ?"""

    sql = "DELETE FROM ask_classes WHERE ask_id = ?"
    db.execute(sql, [ask_id])

    sql = "INSERT INTO ask_classes (ask_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [ask_id, title, value])

def remove_ask(ask_id):
    sql = "DELETE FROM ask_classes WHERE ask_id = ?"
    db.execute(sql, [ask_id])
    sql = "DELETE FROM replies WHERE ask_id = ?"
    db.execute(sql, [ask_id])
    sql = "DELETE FROM asks WHERE id = ?"
    db.execute(sql, [ask_id])

def search_asks(query):
    sql = """SELECT id, title
            FROM asks
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def close_ask(ask_id):
    sql = "UPDATE asks SET status = 0 WHERE id = ?"
    db.execute(sql, [ask_id])

def add_reply(ask_id, user_id, content):
    sql = """INSERT INTO replies (ask_id, user_id, content, sent_at)
            VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [ask_id, user_id, content])

    ask_id = db.last_insert_id()

def get_replies(ask_id):
    sql = """SELECT r.id, r.content, u.id user_id, u.username
            FROM replies r, users u
            WHERE r.ask_id = ? AND r.user_id = u.id
            ORDER BY r.id"""
    return db.query(sql, [ask_id])

def get_reply(reply_id):
    sql = """SELECT r.id,
                    r.content,
                    r.sent_at,
                    r.user_id,
                    u.id user_id,
                    u.username
                FROM replies r, users u
                WHERE r.user_id = u.id AND
                    r.id = ?"""
    result = db.query(sql, [reply_id])
    return result[0] if result else None

def remove_reply(reply_id):
    sql = "DELETE FROM replies WHERE id = ?"
    db.execute(sql, [reply_id])