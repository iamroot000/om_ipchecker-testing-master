import smtplib, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE


def sendemail(mail_subject, mail_content, mail_file=None, mail_file2=None, email_rcv=False):
    if not email_rcv:
        # email_receiver = ['kong@ebet.com', 'omgroup@m1om.me']
#        email_receiver = ['carlv@ebet.com', 'yroll.macalino@m1om.me']
        email_receiver = ['nikko.aratan@m1om.me']

    else:
        # email_receiver = ['omgroup@m1om.me']
#        email_receiver = ['carlv@ebet.com', 'yroll.macalino@m1om.me']
        email_receiver = ['nikko.aratan@m1om.me']
    try:
        #The mail addresses and password
        sender_address = "noreply@m1om.me"
        sender_pass = "bananaballs123!"
        receiver_address = email_receiver
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = COMMASPACE.join(receiver_address)
        message['Subject'] = '{} {}'. format(mail_subject, datetime.datetime.today().date())
        #The subject line
        #The body and the attachments for the mail
        # message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = str(mail_file)
        if email_rcv:
            attach_file_name2 = str(mail_file2)
            message.attach(MIMEText('<b>%s</b><br><img src="cid:%s"><br><br><img src="cid:%s"><br>' % (mail_content, attach_file_name, attach_file_name2), 'html'))
            attach_file2 = open(attach_file_name2, 'rb')  # Open the file as binary mode
            payload2 = MIMEImage(attach_file2.read())
            attach_file2.close()
            payload2.add_header('Content-ID', '<{}>'.format(attach_file2))
            message.attach(payload2)
        else:
            message.attach(MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % (mail_content, attach_file_name), 'html'))
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        #payload = MIMEBase('application', 'octate-stream')
        payload = MIMEImage(attach_file.read())
        # payload.set_payload((attach_file).read())
        # encoders.encode_base64(payload) #encode the attachment
        attach_file.close()
        #add payload header with filename
        payload.add_header('Content-ID', '<{}>'.format(attach_file))
        message.attach(payload)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        return 'Mail Sent'
    except Exception as e:
        return e

