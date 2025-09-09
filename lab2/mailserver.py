import smtplib

sender = "tiru1582@gmail.com"
receiver = "rahulsm6940@gmail.com"
password = "Tiru1582@tiru"   # Google App Password

message = """\
Subject: Test Email

Hello, this is a test email sent from Python!
"""

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
    print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
finally:
    server.quit()
