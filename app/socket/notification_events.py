from flask import request
from flask_socketio import join_room

from app.extensions import socketio

@socketio.on("join_notification_room")
def handle_join_notification_room(data):
    user_id = data["user_id"]

    room = f"user_{user_id}"

    join_room(room)

    print(f"{request.sid} join notification room {room}")