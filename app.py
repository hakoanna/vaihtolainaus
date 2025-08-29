from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import secrets, sqlite3
import config
import db
import asks
import users
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    trade_info = asks.get_trade_asks_info()
    borrow_info = asks.get_borrow_asks_info()
    return render_template("index.html", trade_info=trade_info, borrow_info=borrow_info)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    asks = users.get_asks(user_id)
    data = users.get_user_data(user_id)
    return render_template("show_user.html", user=user, asks=asks, data=data)

@app.route("/add_profile_image", methods=["GET", "POST"])
def add_profile_image():
    require_login()

    if request.method == "GET":
        return render_template("add_profile_image.html")

    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
            return redirect("/add_profile_image")

        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
            return redirect("/add_profile_image")

        user_id = session["user_id"]
        users.update_image(user_id, image)
        flash("Kuvan lisääminen onnistui")
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_user_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = asks.search_asks(query)
    else:
        query = ""
        results = ""
    return render_template("search.html", query=query, results=results)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/trade")
def trade():
    all_asks = asks.get_trade_asks()
    classes = asks.get_all_classes()
    return render_template("trade.html", asks=all_asks, classes=classes)

@app.route("/ask/<int:ask_id>")
def show_ask(ask_id):
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(404)
    classes = asks.get_classes(ask_id)
    replies = asks.get_replies(ask_id)
    return render_template("show_ask.html", ask=ask, classes=classes, replies=replies)

@app.route("/create_ask", methods=["POST"])
def create_ask():
    check_csrf()
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    content = request.form["content"]
    if not content or len(content) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = asks.get_all_classes()

    classes = []
    type = request.form["type"]
    if type:
        class_title, class_value = type.split(":")
        if class_title not in all_classes:
            abort(403)
        if class_value not in all_classes[class_title]:
            abort(403)
        classes.append((class_title, class_value))
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    if request.form["ask_type"] == "trade":
        asks.add_trade_ask(title, content, user_id, classes)
    if request.form["ask_type"] == "borrow":
        asks.add_borrow_ask(title, content, user_id, classes)

    return redirect("/")

@app.route("/edit_ask/<int:ask_id>", methods=["GET", "POST"])
def edit_ask(ask_id):
    require_login()
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(404)
    if ask["user_id"] != session["user_id"]:
        abort(403)
    all_classes = asks.get_all_classes()

    if request.method == "GET":
        classes = {}
        for my_class in all_classes:
            classes[my_class] = ""
        for entry in asks.get_classes(ask_id):
            classes[entry["title"]] = entry["value"]

        return render_template("edit_ask.html", ask=ask, all_classes=all_classes,
        classes=classes)

    if request.method == "POST":
        check_csrf()
        require_login()
        ask_id = request.form["ask_id"]
        ask = asks.get_ask(ask_id)
        if not ask:
            abort(404)
        if ask["user_id"] != session["user_id"]:
            abort(403)
        title = request.form["title"]
        if not title or len(title) > 50:
            abort(403)
        content = request.form["content"]
        if not content or len(content) > 1000:
            abort(403)

        classes = []
        for entry in request.form.getlist("classes"):
            if entry:
                class_title, class_value = entry.split(":")
                if class_title not in all_classes:
                    abort(403)
                if class_value not in all_classes[class_title]:
                    abort(403)
                classes.append((class_title, class_value))

        asks.update_ask(ask_id, title, content, classes)
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
        check_csrf()
        require_login()
        ask_id = request.form["ask_id"]
        ask = asks.get_ask(ask_id)
        if ask["user_id"] != session["user_id"]:
            abort(403)
        if "continue" in request.form:
            asks.remove_ask(ask_id)
        return redirect("/")

@app.route("/close_ask/<int:ask_id>", methods=["POST"])
def close_ask(ask_id):
    check_csrf()
    require_login()
    ask_id = request.form["ask_id"]
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(404)
    if ask["user_id"] != session["user_id"]:
        abort(403)
    asks.close_ask(ask_id)
    return redirect("/ask/" + str(ask_id))

@app.route("/create_reply", methods=["POST"])
def create_reply():
    check_csrf()
    require_login()
    content = request.form["content"]
    if not content or len(content) > 1000:
        abort(403)
    ask_id = request.form["ask_id"]
    ask = asks.get_ask(ask_id)
    if not ask:
        abort(403)
    user_id = session["user_id"]

    asks.add_reply(ask_id, user_id, content)

    return redirect("/ask/" + str(ask_id))

@app.route("/remove_reply/<int:reply_id>", methods=["POST"])
def remove_reply(reply_id):
    check_csrf()
    require_login()
    ask_id = request.form["ask_id"]
    reply = asks.get_reply(reply_id)
    if not reply:
        abort(404)
    if session["user_id"] != reply["user_id"]:
        abort(403)
    asks.remove_reply(reply_id)
    return redirect("/ask/" + str(ask_id))

@app.route("/borrow")
def borrow():
    all_asks = asks.get_borrow_asks()
    classes = asks.get_all_classes()
    return render_template("borrow.html", asks=all_asks, classes=classes)
