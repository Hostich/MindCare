console.log("NOTIFICATION.JS LOADED");

const notificationSocket = io();

const notificationButton = document.getElementById("notification-button");
const notificationDropdown = document.getElementById("notification-dropdown");
let notificationBadge = document.querySelector(".notification-badge");

// CLICK EXISTING NOTIFICATIONS
if(notificationDropdown){
    notificationDropdown.addEventListener("click", function(e){
        const notificationItem = e.target.closest(".notification-item");

        if(!notificationItem){
            return;
        }
        const notificationId = notificationItem.dataset.notificationId;

        if(!notificationId){
            return;
        }
        console.log("NOTIFICATION CLICKED:", notificationId);

        notificationItem.classList.remove("notification-unread");
        fetch("/notification/read/"+ notificationId)
            .then(function(){
                if(notificationBadge){
                    let count = parseInt(notificationBadge.textContent) || 0;
                    count--;
                    if(count <= 0){
                        notificationBadge.remove();
                        notificationBadge = null;
                    }else{
                        notificationBadge.textContent = count;
                    }
                }
            });
        });
    }

//join notification room
notificationSocket.on(
    "connect",
    function(){
        console.log(
            "Notification socket connected:",
            notificationSocket.id
        );

        if(
            typeof currentUserId !== "undefined"
        ){
            notificationSocket.emit(
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
    }
);

//new notification
notificationSocket.on(
    "new_notification",
    function(data){
        console.log(
            "New notification received:",
            data
        );

        if(!notificationDropdown){
            return;
        }

        const existingNotification = notificationDropdown.querySelector(
            `[data-notification-id = "${data.notification_id}"]`
        );

        if (existingNotification){
            return;
        }

        const notificationItem = document.createElement("div");

        notificationItem.classList.add("notification-item");
        notificationItem.classList.add("notification-unread");
        
        notificationItem.dataset.notificationId =
            data.notification_id;

        notificationItem.addEventListener("click", function()
        {
            console.log("NOTIFICATION CLICKED:", data.notification_id);
            fetch("/notification/read/" + data.notification_id)
            .then(function (){
                if(notificationBadge){
                    let count = parseInt(notificationBadge.textContent) || 0;
                    count--;

                    if(count <= 0){
                        notificationBadge.remove();
                        notificationBadge = null;
                    }else{
                        notificationBadge.textContent = count;
                    }
                }
            });
        });

        const title = document.createElement("strong");

        title.textContent = data.title;

        const message = document.createElement("p");

        message.textContent = data.message;

        notificationItem.appendChild(title);
        notificationItem.appendChild(message);


        // NEW CHAT REQUEST
        if(data.notification_type == "ChatRequestCreated"){

            // Accept button
            const acceptButton =
                document.createElement("a");

            acceptButton.href =
                acceptRequestUrl.replace(
                    /0$/,
                    data.request_id
                );

            acceptButton.textContent =
                "Accept";

            // Reject button
            const rejectForm =
                document.createElement("form");

            rejectForm.method = "POST";

            rejectForm.action =
                rejectRequestUrl.replace(
                    /0$/,
                    data.request_id
                );

            const rejectButton =
                document.createElement("button");

            rejectButton.type = "submit";

            rejectButton.textContent =
                "Reject";

            rejectForm.appendChild(
                rejectButton
            );

            notificationItem.appendChild(
                acceptButton
            );

            notificationItem.appendChild(
                rejectForm
            );
        }

        // CHAT REQUEST ACCEPTED
        else if(data.notification_type == "ChatRequestAccepted"){

            const conversationLink =
                document.createElement("a");

            conversationLink.href =
                "/notification/chat/" +
                data.notification_id;

            conversationLink.textContent =
                "Enter Conversation";

            notificationItem.appendChild(
                conversationLink
            );

        }

        // COUNSELING SESSION CREATED
        else if(data.notification_type == "CounselingSessionCreated"){

            const counselingLink =
                document.createElement("a");

            counselingLink.href =
                "/notification/counseling/" +
                data.notification_id;

            counselingLink.textContent =
                "View Counseling Session";

            counselingLink.addEventListener(
                "click",
                function(){

                    if(notificationBadge){

                        let count =
                            parseInt(
                                notificationBadge.textContent
                            ) || 0;

                        count--;

                        if(count <= 0){

                            notificationBadge.remove();

                            notificationBadge = null;

                        }
                        else{

                            notificationBadge.textContent =
                                count;

                        }

                    }

                }
            );

            notificationItem.appendChild(
                counselingLink
            );
        }
        else if(data.notification_type == "ReferralCreated"){
            const referralLink = document.createElement("a");
            referralLink.href = "/counselor/referrals";

            referralLink.textContent = "View Referral";

            notificationItem.appendChild(referralLink);
        }


        const heading =
            notificationDropdown.querySelector("h3");

        if(heading){

            heading.insertAdjacentElement(
                "afterend",
                notificationItem
            );

        }
        else{

            notificationDropdown.prepend(
                notificationItem
            );

        }


        // UPDATE NOTIFICATION BADGE
        if(notificationBadge){

            let count =
                parseInt(
                    notificationBadge.textContent
                ) || 0;

            count++;

            notificationBadge.textContent =
                count;

        }
        else {

            notificationBadge =
                document.createElement("span");

            notificationBadge.classList.add(
                "notification-badge"
            );

            notificationBadge.textContent =
                "1";

            notificationButton.appendChild(
                notificationBadge
            );

        }
    }    
);


// CONVERSATION ENDED
notificationSocket.on(
    "conversation_ended",
    function(data){

        console.log(
            "Conversation ended notification:",
            data
        );

        if(!notificationDropdown){
            return;
        }

        const notificationItems =
            notificationDropdown.querySelectorAll(
                ".notification-item"
            );

        notificationItems.forEach(
            function(notificationItem){

                const notificationLink =
                    notificationItem.querySelector("a");

                if(!notificationLink){
                    return;
                }

                // Check if this notification belongs
                // to the ended conversation
                if(
                    notificationLink.href.includes(
                        "/notification/chat/"
                    )
                ){

                    notificationItem.innerHTML = `
                        <strong>
                            Chat Request Accepted
                        </strong>

                        <p>
                            The volunteer has ended the conversation.
                        </p>

                        <p>
                            Conversation Ended
                        </p>
                    `;

                    // Remove one unread notification
                    if(notificationBadge){

                        let count =
                            parseInt(
                                notificationBadge.textContent
                            ) || 0;

                        count--;

                        if(count <= 0){

                            notificationBadge.remove();

                            notificationBadge = null;

                        }
                        else{

                            notificationBadge.textContent =
                                count;

                        }

                    }

                }

            }
        );

    }
);


// COUNSELING SESSION STARTED
notificationSocket.on(
    "counseling_session_started",
    function(data){

        console.log(
            "Counseling session started:",
            data
        );

        if(
            typeof counselingSessionId !== "undefined" &&
            data.session_id == counselingSessionId
        ){

            console.log(
                "Refreshing counseling session page..."
            );

            window.location.reload();

        }

    }
);


// COUNSELING SESSION COMPLETED
notificationSocket.on(
    "counseling_session_completed",
    function(data){

        console.log(
            "Counseling session completed:",
            data
        );

        if(
            typeof counselingSessionId !== "undefined" &&
            data.session_id == counselingSessionId
        ){

            console.log(
                "Refreshing counseling session page..."
            );

            window.location.reload();

        }

    }
);


// NOTIFICATION DROPDOWN
if (
    notificationButton &&
    notificationDropdown
){

    notificationButton.addEventListener(
        "click",
        function(){

            notificationDropdown.hidden =
                !notificationDropdown.hidden;

        }
    );

}