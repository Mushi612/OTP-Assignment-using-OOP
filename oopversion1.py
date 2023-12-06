import smtplib
import random
import re
from twilio.rest import Client

class CommunicationService:
    @staticmethod
    def generate_otp(length=6):
        
        return ''.join([str(random.randint(0,9))for i in range(6)])

    def send_otp(self, identifier, otp):
        raise NotImplementedError("Subclasses must implement this method.")

class OTPService(CommunicationService):
    def __init__(self, account_sid, auth_token, twilio_number):
        super().__init__()
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_number = twilio_number

    def send_email(self, email, otp):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('ommhatre2003@gmail.com', 'cjtzttnalqeaughf')
        message = f'Your One Time Password is {otp}'
        server.sendmail('ommhatre2003@gmail.com', email, message)
        server.quit()

    def send_otp_over_mobile(self, mobile_no, otp):
        client = Client(self.account_sid, self.auth_token)
        message_body = f'Your 6 digit OTP is {otp}'
        message = client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=f'+91{mobile_no}',
        )
        print(message.body)

    def send_otp_to_mobile_user(self, mobile_user):
        if mobile_user.validate():
            self.send_otp_over_mobile(mobile_user.get_identifier(), self.generate_otp())
        else:
            print("Invalid Mobile number")

    def send_otp_to_email_user(self, email_user):
        if email_user.validate():
            self.send_email(email_user.get_identifier(), self.generate_otp())
        else:
            print("Invalid Email")

class User:
    def __init__(self, identifier):
        self.identifier = identifier

class MobileUser(User):
    def validate(self):
        return len(self.identifier) == 10 and self.identifier.isdigit()

    def get_identifier(self):
        return self.identifier

class EmailUser(User):
    def validate(self):
        validating_condition = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.search(validating_condition, self.identifier))

    def get_identifier(self):
        return self.identifier

if __name__ == "__main__":
    ACCOUNT_SID = "AC83269abe6b5473c7879cfa96bd9e2d3c"
    AUTH_TOKEN = "35dccfab0fcc6644e371ec283df6b6ef"
    TWILIO_NUMBER = '+14705162775'

    OTP_SERVICE = OTPService(ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER)

    MOBILE_USER = MobileUser(input("Enter the Mobile number:"))
    EMAIL_USER = EmailUser(input("Enter the Email:"))

    OTP_SERVICE.send_otp_to_mobile_user(MOBILE_USER)
    OTP_SERVICE.send_otp_to_email_user(EMAIL_USER)