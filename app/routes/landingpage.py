from flask import Blueprint, render_template, url_for


lpage = Blueprint("lpage", __name__)


@lpage.route("/")
def home():
    return render_template("landingpage.html")