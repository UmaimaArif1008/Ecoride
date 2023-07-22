
import smtplib

gmail_user = 'umaima.5593@gmail.com'
gmail_password = 'jpcqjkfrghxemidl'

subject = 'OTP for password reset.'
email_text = "OTP for reset password is "
def sendEmail(email, otp):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, email, email_text+otp)
        server.close()
        print ('Email sent!')
        return True
    except Exception as e:
        print(e)
        print ('Something went wrong...')
        return False