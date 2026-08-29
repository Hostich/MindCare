from flask import Blueprint, render_template, redirect, url_for, flash
from datetime import datetime
from flask_login import login_required, current_user
from app.models.referral import Referral
from app.extensions import db

counselor = Blueprint("counselor", __name__, url_prefix="/counselor")

@counselor.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "Counselor":
        return redirect(url_for("lpage.home"))
    
    return render_template("counselor/dashboard.html")


@counselor.route("/referrals")
@login_required
def referrals():

    if current_user.role != "Counselor":
        return redirect(url_for("lpage.home"))

    referrals = (
        Referral.query
        .filter_by(
            counselor_id = current_user.user_id
        )
        .order_by(
            Referral.referred_at.desc()
        )
        .all()
    )

    return render_template("counselor/referrals.html", referrals = referrals)

@counselor.route("/referrals/<int:referral_id>")
@login_required
def review_referrals(referral_id):

    if current_user.role != "Counselor":
        return redirect(url_for("lpage.home"))

    referral = (
        Referral.query
        .filter_by(
            referral_id = referral_id,
            counselor_id = current_user.user_id
        )
        .first()
    )

    if not referral:
        return redirect(url_for("counselor.referrals"))

    return render_template("cousnelor/review_referral.html", referral = referral)

@counselor.route("/referral/<int:referral_id>/accept", methods=['POST'])
@login_required
def accept_referral(referral_id):

    if current_user.role != "Counselor":
        flash("Unauthorize access.")
        return redirect(url_for("lpage.home"))

    referral = (
        Referral.query
        .filter_by(
            referral_id = referral_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not referral:
        flash("Referral not foud.", "warning")

        return redirect(url_for("counselor.referrals"))

    if referral.referral_status != "Pending":

        flash("This referral has already been processed.")
        return redirect(url_for("counselor.referrals"))

    referral.referral_status = "Accepted"
    referral.responded_at = datetime.utcnow()

    db.session.commit()

    flash("Referral accepted successfully.", "success")

    return redirect(url_for("counselor.referrals"))


@counselor.route("/referral/<int:referral_id>/reject",methods=['POST'])
@login_required
def reject_referral(referral_id):

    if current_user.role != "Counselor":
        flash("Unauthorize access", "danger")
        return redirect(url_for("lpage.home"))

    referral = (
        Referral.query
        .filter_by(
            referral_id = referral_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not referral:
        flash("Rerral not found.","danger")
        return redirect(url_for("counselor.referrals"))

    if referral.referral_status != "Pending":
        flash("This referral has already been processed", "warning")
        return redirect(url_for("counselor.referrals"))

    referral.referral_status = "Rejected"
    referral.responded_at = datetime.utcnow()

    db.session.commit()

    flash("Referral rejected", "info")
    
    return redirect(url_for("counselor.referrals"))
