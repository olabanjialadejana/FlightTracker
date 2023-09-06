import smtplib


class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self, to_email, subject, content):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=to_email,
                msg=f"Subject:{subject}\n\n{content}"
            )
