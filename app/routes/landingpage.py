from flask import Blueprint

lpage = Blueprint("lpage", __name__)

@lpage.route("/")
def home():
    return "<h2>WELCOME TO MINDCARE!</h2>"
    