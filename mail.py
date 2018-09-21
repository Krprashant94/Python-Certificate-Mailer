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

class Editor:
    """docstring for Editor"""
    def __init__(self, tamplate_file):
        """
        Template location
        """
        self.tamplate_file = tamplate_file
        self.img = Image.open(tamplate_file)
        self.width, self.height = self.img.size
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype('a.ttf', 150)
        self.location = (0,0)
    def setFont(self, font_name, size):
        """
        Set font style and font size
        """
        self.font = ImageFont.truetype(font_name, size)
    def setLocation(self, x, y):
        """
        Set cursor location where to write. Right alignment
        """
        self.location = (x, y)
    def writeName(self, name, color=(0,0,0)):
        """
        Write the name of certificate
        """
        self.draw.text(self.location, name, color,font=self.font)
    def save(self, file_name):
        """
        Save the edited file
        """
        self.img.save('Generated/'+file_name+'.png')


# set up the SMTP server
class Mailler():
    """
    Mailler class
    """

    def __init__(self, mail, password):
        self.html = """\
        <html>
          <head></head>
          <body>
            <p>Hi!<br> 
               How are you?<br> 
               Here is the <a href="https://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>"""
        self.sub = "Test : Certificate of Participation"
        
        self.me = ""
        self.password = ""
        self.server = ""
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


if not os.path.exists('Generated'):
    os.makedirs('Generated')

initTime = datetime.datetime.now()
no = 0
names = pd.read_csv("mailling_list.csv")
# print(names)


for index, row in names.iterrows():
    certi = Editor("certificate.png")
    certi.setFont("a.ttf", 150)
    certi.setLocation(certi.width/2 - 45*len(row['name']), 1300)
    certi.writeName(row['name'].upper())
    certi.save(row['mail'])
    
    f = open('account.config', 'r')
    info = f.read()
    f.close()
    info = info.split()
    print(info)
    continue
    mailler = gmailMailler(info[0], info[1])
    mailler.open()
    mailler.send("<mail-id>", sub, html, "Generated/"+names.loc[i]['mail'].lower()+".png")
    mailler.close()
    no = i
    print("Mailled to \t" + names.loc[i]['name'].upper() +"\t\t"+ names.loc[i]['mail'].lower());
    

finalTime = datetime.datetime.now()
t = finalTime-initTime
print(str(no+1)+" Certificate Generated and mailled in "+str(t)+ " Sec.")

