# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:52:40 2018

@author: Prashant Kumar
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os



from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pandas as pd
import datetime


# set up the SMTP server

class gmailMailler():
    me = ""
    password = ""

    server = ""

    def __init__(self, mail, password):
        self.me = mail
        self.password = password

    def open(self):
        self.server = smtplib.SMTP('smtp.gmail.com:587')
        self.server.starttls()
        self.server.login(self.me, self.password)
        
    def close(self):
        self.server.quit()
    
    def send(self, to, sub, html, attach=0):
        msg = MIMEMultipart()
        body = MIMEText(html, 'html')
        msg.attach(body)
        if(attach != 0):
            img_data = open(attach, 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename(attach))
            msg.attach(image)
            
        msg['Subject'] = sub
        msg['From'] = self.me
        msg['To'] = to
        self.server.sendmail(self.me, to, msg.as_string())



html = '\
<html>\
  <head></head>\
  <body>\
    <p>Hi!<br> \
       How are you?<br> \
       Here is the <a href="https://www.python.org">link</a> you wanted.\
    </p>\
  </body>\
</html>'
sub = "Test : Certificate of Participation of PINK (Rotaract club of RCCIIT)"

initTime = datetime.datetime.now()
no = 0
names = pd.read_csv("pink.csv")
#print(len(names))

for i in range(0 , len(names)):
    img = Image.open("certificate.png")
    width, height = img.size
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("a.ttf", 150)
    # draw.text((x, y),"Sample Text",(r,g,b))
    location = width/2 - 45*len(names.loc[i]['name'])
    draw.text((location, 1300),names.loc[i]['name'].upper(),(0,0,0),font=font)
    img.save('Generated/'+names.loc[i]['mail'].lower()+'.png')

    mailler = gmailMailler("<mail-id>", "<password>")
    mailler.open()
    TODO: Change it to names.loc[i]['mail'].lower()
    mailler.send("<mail-id>", sub, html, "Generated/"+names.loc[i]['mail'].lower()+".png")
    mailler.close()
    no = i
    print("Mailled to \t" + names.loc[i]['name'].upper() +"\t\t"+ names.loc[i]['mail'].lower());
    

finalTime = datetime.datetime.now()
t = finalTime-initTime
print(str(no+1)+" Certificate Generated and mailled in "+str(t)+ " Sec.")

