console.log("NOTIFICATION.JS LOADED");

const notificationSocket = io();

const notificationButton = document.getElementById("notification-button");
const notificationDropdown = document.getElementById("notification-dropdown");
let notificationBadge = document.querySelector(".notification-badge");

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
        )

        if (existingNotification){
            return;
        }

        const notificationItem = document.createElement("div");

        notificationItem.classList.add("notification-item");
        
        notificationItem.dataset.notificationId = data.notification_id;

        const title = document.createElement("strong");

        title.textContent = data.title;

        const message = document.createElement("p");

        message.textContent = data.message;

        notificationItem.appendChild(title);
        notificationItem.appendChild(message);

        if(data.notification_type == "ChatRequestAccepted"){
            const conversationLink = document.createElement("a");

            conversationLink.href = "/notification/chat/" + data.notification_id;

            conversationLink.textContent = "Enter Conversation";

            notificationItem.appendChild(conversationLink);
        }

        const heading = notificationDropdown.querySelector("h3");

        if(heading){
            heading.insertAdjacentElement(
                "afterend",
                notificationItem
            );
        }else{
            notificationDropdown.prepend(notificationItem);
        }

        if(notificationBadge){
            let count = parseInt(notificationBadge.textContent) || 0;

            count++;

            notificationBadge.textContent = count;
        }
        else {
            notificationBadge = document.createElement("span");

            notificationBadge.classList.add("notification-badge");

            notificationBadge.textContent = "1";

            notificationButton.appendChild(notificationBadge);
        }
    }    
);


if (notificationButton && notificationDropdown){
    notificationButton.addEventListener(
        "click",
        function(){
            notificationDropdown.hidden = !notificationDropdown.hidden;
        }
    )
}