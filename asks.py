import db

def add_ask(title, content, user_id):
    sql = """INSERT INTO asks (title, content, sent_at, user_id)
            VALUES (?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, content, user_id])

def get_asks():
    sql = """SELECT asks.id,
                asks.title,
                asks.user_id,
                asks.sent_at,
                users.username
            FROM asks, users
            WHERE asks.user_id = users.id
            ORDER BY asks.id DESC"""
    return db.query(sql)

def get_ask(ask_id):
    sql = """SELECT asks.title, 
                    asks.content,
                    asks.sent_at,
                    users.username
                FROM asks, users
                WHERE asks.user_id = users.id AND
                    asks.id = ?"""
    return db.query(sql, [ask_id])[0]