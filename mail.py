# -*- coding: utf-8 -*-
"""
Python Certificate Mailer
Created on Tue Feb 20 19:52:40 2018

@author: Prashant Kumar
"""
# mailling lib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Image Editing
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import pandas as pd
import datetime
import os

class Editor:
    """Editor class is for editing the certificate. It takes tamplate_file name to initilize the class"""
    def __init__(self, tamplate_file):
        """
        initilize the class
        tamplate_file (string): file name. file must be an png|jpg|bmp image. 
        """
        self.tamplate_file = tamplate_file
        self.img = Image.open(tamplate_file)
        self.width, self.height = self.img.size
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype('a.ttf', 150)
        self.location = (0,0)
    def setFont(self, font_name, size):
        """
        Set font style and font size of pen
        font_name (string): font file name. must be an .ttf filename path.
        size (int): size of the font.
        """
        self.font = ImageFont.truetype(font_name, size)
    def setLocation(self, x, y):
        """
        Set cursor location where to write. Right alignment.
        x (int): X-cordinate in image.
        y (int): Y-cordinate in image.
        """
        self.location = (x, y)
    def writeName(self, name, color=(0,0,0)):
        """
        Write the name of certificate
        name (string): name/text to print in certificate.
        color (r,g,b): color of the text.
        """
        self.draw.text(self.location, name, color,font=self.font)
    def save(self, file_name):
        """
        Save the edited file in location "/Generated".
        file_name (string): name of the file to saved
        """
        self.img.save('Generated/'+file_name+'.png')


class Mailler():
    """
    Mailler class is for SMTL outgoing mail setup
    need to ON lesssecureapps in this link if using google mail ID: https://myaccount.google.com/u/1/lesssecureapps?pageId=none
    """

    def __init__(self, mail, password):
        """
        Initilize the mailler with mail id and password.
        mail(string): Your mail ID
        password(string): Your password
        """
        self.html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br> 
               Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>"""
        self.sub = "Test : Certificate of Participation"
        
        self.server = ""
        self.my_mail_id = mail
        self.password = password
    def setTemplate(self, sub, body):
        """
        Set the HTML mail template for sending mail.
        sub (string): subject of the mail
        body (string): HTML body of the mail
        """
        self.html = body
        self.sub = sub
    def login(self):
        """
        Login to SMTP mail server.
        """
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login(self.my_mail_id, self.password)
        
    def logout(self):
        """
        Logout SMTP mail server.
        """
        self.server.quit()
    
    def send(self, to, attach=0):
        """
        send a mail
        to (string): where to send. must be an valid mail ID.
        attach (optinal)(string): full path of attachment file.  
        """
        msg = MIMEMultipart()
        body = MIMEText(self.html, 'html')
        msg.attach(body)
        if(attach != 0):
            img_data = open(attach, 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename(attach))
            msg.attach(image)
            
        msg['Subject'] = self.sub
        msg['From'] = self.my_mail_id
        msg['To'] = to
        self.server.sendmail(self.my_mail_id, to, msg.as_string())

# Check if /Generated folder exist or not and then create.
if not os.path.exists('Generated'):
    os.makedirs('Generated')

# get the account ID and password
f = open('account.config', 'r')
info = f.read()
f.close()
info = info.split()
# Get timestanp for calculating time taken to send all mail
initTime = datetime.datetime.now()
# Counter
no = 0
# All mailling list
names = pd.read_csv("mailling_list.csv")

for index, row in names.iterrows():
    certi = Editor("certificate.png")
    certi.setFont("a.ttf", 150)
    certi.setLocation(certi.width/2 - 45*len(row['name']), 1300)
    certi.writeName(row['name'].upper())
    certi.save(row['mail'])
    
    mailler = Mailler(info[0], info[1])
    mailler.login()
    mailler.send(row['mail'], "Generated/"+row['mail'].lower()+".png")
    mailler.logout()
    no+=1
    print("Mailled to \t" + row['name'].upper() +"\t\t"+ row['mail'].lower());
    

finalTime = datetime.datetime.now()
t = finalTime-initTime
print(str(no+1)+" Certificate Generated and mailled in "+str(t)+ " Sec.")

