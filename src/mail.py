import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = 'protech2043@gmail.com'
    msg['To'] = 'gursewaksaggu2043@gmail.com'
    text = MIMEText("test")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    port=smtplib.SMTP_PORT
    s = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('protech2043@gmail.com', '********')
    From = msg['From']
    To = msg['To']
    s.sendmail(From, To, msg.as_string())
    s.quit()

FileName = 'ImageBase/Balveer_singh.jpeg'
SendMail(FileName)
