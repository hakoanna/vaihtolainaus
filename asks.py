import db

def add_ask(title, content, user_id):
    sql = """INSERT INTO asks (title, content, user_id)
            VALUES (?, ?, ?)"""
    db.execute(sql, [title, content, user_id])

def get_asks():
    sql = "SELECT id, title FROM asks ORDER BY id DESC"
    return db.query(sql)

def get_ask(ask_id):
    sql = """SELECT asks.title, 
                    asks.content,
                    users.username
                FROM asks, users
                WHERE asks.user_id = users.id AND
                    asks.id = ?"""
    return db.query(sql, [ask_id])[0]