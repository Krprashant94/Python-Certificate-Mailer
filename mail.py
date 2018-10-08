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



import pandas as pd
import datetime
import os

class Mailler():
    """
    Mailler class is for SMTL outgoing mail setup
    need to ON lesssecureapps in this link if using google mail ID: https://myaccount.google.com/u/1/lesssecureapps?pageId=none
    """

    def __init__(self, mail, password, name):
        """
        Initilize the mailler with mail id and password.
        mail(string): Your mail ID
        password(string): Your password
        """
        self.html = """\
        <html>
          <head></head>
          <body>
            <p style="font-size:16px;">Dear """+name+""",<br> 
               <p style="font-size:16px;">You are getting this email because you are applied for "Six Petal Internship Program".  Please go through the <a href="https://docs.google.com/forms/d/e/1FAIpQLSe4ABFFz6h8EXTt6gKgOXcdao3Fp4MLbMbEylTxetjdjM5__Q/viewform">link for round one</a>. Please note that we have limited number of vacancy; we will select top scored person only with less time(Time calculation will start from now)  if you will qualify in this round. we will call you (via Skype or phone) for an interview cum selection round. Please note that appearing in round one means you are accepting our term and condition which was mentioned at the time of form fillup.</p>
<p style="font-size:16px;"><br/>Important Note again:<br/></p>
<ol>
<li style="font-size:16px;">You will get a letter of recommendation for your work</li>
<li style="font-size:16px;">Depending upon your CV we many shift your work to another location(only  in case of vacancy full)</li>
<li style="font-size:16px;">This is an unpaid internship however you will get accommodation(or your pocket money)  if needed </li>
</ol>

			Link : https://docs.google.com/forms/d/e/1FAIpQLSe4ABFFz6h8EXTt6gKgOXcdao3Fp4MLbMbEylTxetjdjM5__Q/viewform
<br/><br/><br/><br/><br/><br/>
			Regards<br/>
			Six Petal Developer Team
            </p>
          </body>
        </html>"""
        self.sub = "Six Petal Internship Program"
        
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
names = pd.read_csv("Internship Form.csv")

for index, row in names.iterrows():
    
    mailler = Mailler(info[0], info[1], row['name'])
    mailler.login()
    mailler.send(row['email'])
    mailler.logout()
    no+=1
    print("Mailled to \t" + row['name'].upper() +"\t\t"+ row['email'].lower());
    

finalTime = datetime.datetime.now()
t = finalTime-initTime
print(str(no)+" Mailled in "+str(t)+ " Sec.")

