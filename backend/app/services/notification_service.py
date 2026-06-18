"""
LandScope AI — Notification Service (Mock SMTP)
"""

def send_alert_email(email: str, subject: str, message: str):
    """
    Mock email sender that just prints to the console for development.
    In production, this would use smtplib or SendGrid.
    """
    print(f"==================================================")
    print(f"📧 EMAIL ALERT TO: {email}")
    print(f"📝 SUBJECT: {subject}")
    print(f"💬 MESSAGE:\n{message}")
    print(f"==================================================")
