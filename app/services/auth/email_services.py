import random
from flask_mail import Message
from app.extensions import mail

def generate_verification_code():
    return str(random.randint(100000, 999999))
    
def send_verification_email(email, username, code):
    subject = "MindCare Emai Verificationl"
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background:#f5f5f5; padding:30px;">

            <div style="
                max-width:600px;
                margin:auto;
                background:white;
                border-radius:10px;
                padding:40px;
                box-shadow:0 0 10px rgba(0,0,0,.1);
            ">

                <h2 style="color:#2E8B57;">
                    Welcome to MindCare!
                </h2>

                <p>Hello <strong>{username}</strong>,</p>

                <p>
                    Thank you for creating a MindCare account.
                </p>

                <p>
                    Please use the verification code below to verify your email address.
                </p>

                <h1 style="
                    text-align:center;
                    letter-spacing:8px;
                    color:#2E8B57;
                ">
                    {code}
                </h1>

                <p>
                    This verification code will expire in
                    <strong>10 minutes</strong>.
                </p>

                <hr>

                <small style="color:gray;">
                    If you did not create a MindCare account,
                    you can safely ignore this email.
                </small>

            </div>

        </body>
    </html>
    """
    message = Message(
        subject = subject,
        recipients=[email],
        html=html
    )
    
    mail.send(message)