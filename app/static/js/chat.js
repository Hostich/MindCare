const socket = io();

socket.on("connect", function () {

    console.log("Connected:", socket.id);

    socket.emit("join_room", {
        conversation_id: conversationId
    });

});

const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", function (e) {

    e.preventDefault();

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    socket.emit("send_message", {
        conversation_id: conversationId,
        sender_id: currentUserId,
        message: message
    });

    messageInput.value = "";

});

socket.on("receive_message", function (data) {

    const div = document.createElement("div");

    const sender =
        data.sender_id == currentUserId
            ? "You"
            : otherUserLabel;

    div.innerHTML = `
        <strong>${sender}</strong>
        <p>${data.message}</p>
        <hr>
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

});

socket.on("conversation_ended", function(data) {
   
    alert("The conversation has ended.");
   
    window.location.href = chatRedirectUrl;
});

window.addEventListener("beforeunload", function () {

    socket.emit("leave_room", {
        conversation_id: conversationId
    });

});