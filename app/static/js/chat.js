console.log("CHAT.JS LOADED");


/* =========================================
   CREATE SOCKET CONNECTION
========================================= */

const socket = io();





/* =========================================
   SOCKET CONNECTED
========================================= */

socket.on("connect", function () {

    console.log(
        "Connected:",
        socket.id
    );

     /*
        Join the user's notification room.

        This allows this socket connection to
        receive new chat request notifications.
    */

    if (typeof currentUserId !== "undefined") {

        socket.emit(
            "join_notification_room",
            {
                user_id: currentUserId
            }
        );

        console.log(
            "Joined notification room:",
            currentUserId
        );

    }

    /*
        Only join a room when a conversation
        is currently selected.
    */

    if (typeof conversationId !== "undefined") {

        socket.emit("join_room", {

            conversation_id:
                conversationId

        });

        console.log(
            "Joined conversation:",
            conversationId
        );

    }

});


/* =========================================
   GET CHAT ELEMENTS
========================================= */

const form =
    document.getElementById("chat-form");

const messageInput =
    document.getElementById("message-input");

const chatBox =
    document.getElementById("chat-box");


/* =========================================
   SEND MESSAGE
========================================= */

if (form) {

    form.addEventListener(
        "submit",
        function (e) {

            /*
                VERY IMPORTANT:
                Stop the browser from submitting
                the form normally.
            */

            e.preventDefault();


            const message =
                messageInput.value.trim();


            if (message === "") {
                return;
            }


            console.log(
                "Sending message:",
                message
            );


            socket.emit(
                "send_message",
                {

                    conversation_id:
                        conversationId,

                    sender_id:
                        currentUserId,

                    message:
                        message

                }
            );


            /*
                Clear input after sending.
            */

            messageInput.value = "";

        }
    );

}


/* =========================================
   RECEIVE MESSAGE
========================================= */

socket.on(
    "receive_message",
    function (data) {

        const currentChatBox = document.getElementById("chat-box");

        if (!currentChatBox) {
            return;
        }

        if (typeof conversationId !== "undefined" && data.conversation != conversationId){
            return;
        }


        const div =
            document.createElement("div");

        
        const isMine = data.sender_id == currentUserId;

        div.classList.add("message");

        if(isMine){
            div.classList.add("message-mine");
        }else{
            div.classList.add("message-theirs");
        }



        const sender =
            data.sender_id == currentUserId
                ? "You"
                : otherUserLabel;

        div.innerHTML = `

            <strong>
                ${sender}
            </strong>

            <p>
                ${data.message}
            </p>

            <small>
                Just now
            </small>
            <hr>

        `;


        chatBox.appendChild(div);


        /*
            Scroll to newest message.
        */

        currentChatBox.scrollTop =
            currentChatBox.scrollHeight;

    }
);


/* =========================================
   CONVERSATION ENDED
========================================= */

socket.on(
    "conversation_ended",
    function (data) {

        console.log(
            "Conversation ended:",
            data
        );


        alert(
            "The conversation has ended."
        );


        /*
            Return to the chat page.
            This removes the conversation_id
            from the URL.
        */

        if (
            typeof chatRedirectUrl !==
            "undefined"
        ) {

            window.location.href =
                chatRedirectUrl;

        }

    }
);
/* =========================================
   COUNSELING SESSION STARTED
========================================= */
socket.on(
    "counseling_session_started",
    function (data) {

        console.log(
            "Counseling session started:",
            data
        );

        if (
            typeof counselingSessionId !== "undefined" &&
            data.session_id == counselingSessionId
        ) {

            console.log(
                "This counseling session has started."
            );

            window.location.reload();

        }

    }
);

/* =========================================
   CHAT TABS FOR SEEKER
========================================= */

const allVolunteersBtn = document.getElementById("all-volunteers-btn");
const privateChatBtn = document.getElementById("private-chat-btn");
const volunteerList = document.getElementById("volunteer-list");
const privateChatList = document.getElementById("private-chat-list");

if(allVolunteersBtn && privateChatBtn && volunteerList && privateChatList){
    allVolunteersBtn.addEventListener(
        "click",
        function(){
            volunteerList.hidden = false;
            privateChatList.hidden = true;
            allVolunteersBtn.classList.add("active");
            privateChatBtn.classList.remove("active");
        }
    );

    privateChatBtn.addEventListener(
        "click",
        function(){
            volunteerList.hidden = true;
            privateChatList.hidden = false;
            privateChatBtn.classList.add("active");
            allVolunteersBtn.classList.remove("active");
        }
    );
}

/* =========================================
   VOLUNTEER NOTIFICATION CHAT REQUEST
========================================= */
socket.on("new_notification", function(data){

    console.log("CHAT PAGE RECEIVED NOTIFICATION:", data);

    if(data.notification_type !== "ChatRequestCreated"){
        return;
    }

    const pendingList = document.getElementById("pending-list");

    if(!pendingList){
        console.log("PENDING LIST NOT FOUND");
        return;
    }

    // Prevent duplicate request cards
    const existingRequest = pendingList.querySelector(
        `[data-request-id="${data.request_id}"]`
    );

    if(existingRequest){
        return;
    }

    // Create request card
    const requestCard = document.createElement("div");
    requestCard.classList.add("request-card");
    requestCard.dataset.requestId = data.request_id;

    // Request information
    const requestInfo = document.createElement("div");
    requestInfo.classList.add("request-info");

    const seekerName = document.createElement("strong");
    seekerName.textContent = "Anonymous Seeker";

    const requestMessage = document.createElement("p");
    requestMessage.textContent = "Wants to start a conversation";

    requestInfo.appendChild(seekerName);
    requestInfo.appendChild(requestMessage);

    // Accept button
    const acceptButton = document.createElement("a");
    acceptButton.href = acceptRequestUrl.replace(
        /0$/,
        data.request_id
    );
    acceptButton.textContent = "Accept";

    // Reject form
    const rejectForm = document.createElement("form");
    rejectForm.method = "POST";
    rejectForm.action = rejectRequestUrl.replace(
        /0$/,
        data.request_id
    );

    const rejectButton = document.createElement("button");
    rejectButton.type = "submit";
    rejectButton.textContent = "Reject";

    rejectForm.appendChild(rejectButton);

    // Add everything to request card
    requestCard.appendChild(requestInfo);
    requestCard.appendChild(acceptButton);
    requestCard.appendChild(rejectForm);

    // Add the request before the "No pending..." message
    const noRequestsMessage = pendingList.querySelector("p");

    if(
        noRequestsMessage &&
        noRequestsMessage.textContent.includes(
            "No pending chat requests"
        )
    ){
        noRequestsMessage.remove();
    }

    pendingList.appendChild(requestCard);
});