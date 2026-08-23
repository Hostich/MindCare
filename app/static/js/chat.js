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

        /*
            If there is no chat box,
            don't try to add anything.
        */

        const currentChatBox = document.getElementById("chat-box");

        if (!currentChatBox) {
            return;
        }

        if (
            typeof conversationId !== "undefined" && data.conversation != conversationId
        ){
            return;
        }


        const div =
            document.createElement("div");


        const sender =
            data.sender_id == currentUserId
                ? "You"
                : otherUserLabel;


        div.classList.add("message");


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