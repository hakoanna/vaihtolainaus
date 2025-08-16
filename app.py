import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash 
import config
import db
import asks

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    info = asks.get_asks_info()
    return render_template("index.html", info=info)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = asks.search_asks(query)
    else:
        query = ""
        results = ""
    return render_template("search.html", query=query, results=results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/trade")
def trade():
    all_asks = asks.get_asks()
    return render_template("trade.html", asks=all_asks)

@app.route("/ask/<int:ask_id>")
def show_ask(ask_id):
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(404)
    return render_template("show_ask.html", ask=ask)

@app.route("/create_ask", methods=["POST"])
def create_ask():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    content = request.form["content"]
    if not content or len(content) > 1000:
        abort(403)
    user_id = session["user_id"]

    asks.add_ask(title, content, user_id)

    return redirect("/")

@app.route("/edit_ask/<int:ask_id>", methods=["GET", "POST"])
def edit_ask(ask_id):
    require_login()
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(404)
    if ask["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_ask.html", ask=ask)

    if request.method == "POST":
        require_login()
        ask_id = request.form["ask_id"]
        ask = asks.get_ask(ask_id)
        if not ask:
            abort(404)
        if ask["user_id"] != session["user_id"]:
            abort(403)
        title = request.form["title"]
        content = request.form["content"]
        asks.update_ask(ask_id, title, content)
        return redirect("/ask/" + str(ask_id))

@app.route("/remove_ask/<int:ask_id>", methods=["GET", "POST"])
def remove_ask(ask_id):
    require_login()
    ask = asks.get_ask(ask_id)
    if not ask:
            abort(404)
    if ask["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_ask.html", ask=ask)

    if request.method == "POST":
        require_login()
        ask_id = request.form["ask_id"]
        ask = asks.get_ask(ask_id)
        if ask["user_id"] != session["user_id"]:
            abort(403)
        if "continue" in request.form:
            asks.remove_ask(ask_id)
        return redirect("/trade")


@app.route("/borrow")
def borrow():
    return render_template("borrow.html")