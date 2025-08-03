from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tähän tulee paikka, jossa voi sopia lainauksia ja vaihtokauppoja."
