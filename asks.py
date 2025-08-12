import db

def add_ask(title, content, user_id):
    sql = """INSERT INTO asks (title, content, user_id)
            VALUES (?, ?, ?)"""
    db.execute(sql, [title, content, user_id])