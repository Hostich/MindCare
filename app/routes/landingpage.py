from flask import Blueprint, render_template

lpage = Blueprint("lpage", __name__)


@lpage.route("/")
def home():
    return render_template("landingpage.html")