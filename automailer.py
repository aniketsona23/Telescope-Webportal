import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sqlite3
conn = sqlite3.connect('databasemailer.db')
cursor = conn.cursor()


def send_email(recipient_email, subject, body_html):
    message = MIMEMultipart("alternative")
    message['From'] = "bitscopegoa@outlook.com"
    message['To'] = recipient_email
    message['Subject'] = subject
    message['Content-Type'] = 'text/html'
    message.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login("bitscopegoa@outlook.com", "BItscope2024")
        server.send_message(message)

    print("Email sent successfully")

cursor.execute("SELECT id, name, obj, email FROM data WHERE id=?", (5,))
rows  = cursor.fetchall()
for row in rows:
    id, name, obj, email = row
    print (name)
    print(obj)
    print(email) 
    print(id)

recipient_email = email
subject = f"Test Email| Order ID:{id}"
body_html = f"""\
<html>
  <body>
    <p>Hey {name},</p>
    <p>Please find attached the image of {obj} which you requested</p>
    <p>Your order ID is {id}<p>
    <p>Brought to you by BITScope the BITS GOA Web Observatory</p>
  </body>
</html>
"""

send_email(recipient_email, subject, body_html)