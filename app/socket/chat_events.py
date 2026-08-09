from flask_socketio import join_room, leave_room
from flask import request
from app.extensions import socketio
from app.services.chat.message_services import send_message

@socketio.on("join_room")
def handle_join_room(data):
    room = f"conversation_{data['conversation_id']}"
    join_room(room)
    print(f"{request.sid} Joined {room}")

@socketio.on("leave_room")
def handle_leave_room(data):
    room = f"conversation_{data['conversation_id']}"
    leave_room(room)
    print(f"{request.sid} Left {room}")

@socketio.on("send_message")
def handle_send_message(data):

    room = f"conversation_{data['conversation_id']}"

    send_message(
        data["conversation_id"],
        data["sender_id"],
        data["message"]
    )

    print(data)

    socketio.emit(
        "receive_message",
        {
            "sender_id": data["sender_id"],
            "message": data["message"]
        },
        to=room
    )