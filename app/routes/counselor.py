from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime
from flask_login import login_required, current_user
from app.models.referral import Referral
from app.models.counseling_session import CounselingSession
from app.models.session_summaries import SessionSummary
from app.services.chat.conversation_services import create_counseling_conversation
from app.services.chat.message_services import get_messages
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

    session = CounselingSession(
        referral_id = referral.referral_id,
        seeker_id = referral.seeker_id,
        counselor_id = referral.counselor_id,
        session_type = referral.preferred_session_type,
        session_status = "Pending"
    )

    db.session.add(session)
    db.session.commit()

    flash("Referral accepted successfully and counseling session is created.", "success")

    return redirect(url_for("counselor.view_session", session_id = session.session_id))


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


@counselor.route("/session/<int:session_id>")
@login_required
def view_session(session_id):
    if current_user.role != "Counselor":
        flash("Unauthorize Access.", "danger")
        return redirect(url_for("lpage.home"))

    session = (
        CounselingSession.query
        .filter_by(
            session_id = session_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not session:
        flash("Counseling session not found.", "warning")
        return redirect(url_for("counselor.referrals"))

    messages = []

    if session.conversation:
        message = get_messages(
            session.conversation.conversation_id
        )

    return render_template("counselor/session.html", session = session, messages = messages)


@counselor.route("/session/<int:session_id>/start", methods=['POST'])
@login_required
def start_session(session_id):

    if current_user.role != "Counselor":
        flash("Unauthorized Access.", "danger")
        return redirect(url_for("lpage.home"))

    session = (
        CounselingSession.query
        .filter_by(
            session_id = session_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not session:
        flash("Counseling session not found.","warning")
        return redirect(url_for("counselor.referrals"))

    if session.session_status != "Pending":
        flash("This counseling sesion connot be started.", "warning")
        return redirect(url_for("counselor.view_session", session_id = session_id))

    session.session_status = "Active"
    session.started_at = datetime.utcnow()

    conversation = create_counseling_conversation(
        session.session_id
    )

    db.session.commit()

    flash("Counseling session is now starting")

    return redirect(url_for("counselor.view_session", session_id = session_id))


@counselor.route("/session/<int:session_id>/complete", methods=['POST'])
@login_required
def complete_session(session_id):
    if current_user.role != "Counselor":
        flash("Unauthorize Access.", "danger")
        return redirect(url_for("lpage.home"))

    session = (
        CounselingSession.query
        .filter_by(
            session_id = session_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not session:
        flash("Counseling session not found!.", "warning")
        return redirect(url_for("counselor.counseling_sessions"))

    if session.session_status != "Active":
        flash("This counseling session has already been processd.", "warning")
        return redirect(url_for("counselor.view_session", session_id = session_id))

    outcome = request.form.get("outcome")
    counselor_note = request.form.get("counselor_note")

    if not outcome:
        flash("Session outcome is required.", "warning")
        return redirect(url_for("counselor.view_session", session_id = session_id))

    summary = SessionSummary(
        session_id = session.session_id,
        outcome = outcome,
        counselor_note = counselor_note or None,
        completed_at = datetime.utcnow()
    )

    session.session_status = "Completed"
    session.ended_at = datetime.utcnow()

    db.session.add(summary)
    db.session.commit()

    flash("Counseling session completed successfully.","success")

    return redirect(url_for("counselor.view_session", session_id = session_id))


@counselor.route("/session/<int:session_id>/cancel", methods = ['POST'])
@login_required
def cancel_session(session_id):
    if current_user.role != "Counselor":
        flash("Unauthorized Access.", "danger")
        return redirect(url_for("lpage.home"))

    session = (
        CounselingSession.query
        .filter_by(
            session_id = session_id,
            counselor_id = current_user.user_id
        ).first()
    )

    if not session:
        flash("Counseling session not found.", "warning")
        return redirect(url_for("counselor.counseling_sessions"))

    if session.session_status != "Active":
        flash("This counseling session has already been processed.", "warning")
        return redirect(url_for("counselor.view_session", session_id = session_id))

    session.session_status = "Cancelled"
    session.ended_at = datetime.utcnow()

    db.session.commit()

    flash("Counseling session has been cancelled", "success")

    return redirect(url_for("counselor.view_session", session_id = session_id))



                        