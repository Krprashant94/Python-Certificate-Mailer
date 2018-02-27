# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:52:40 2018

@author: Prashant Kumar
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pandas as pd
import datetime


a = datetime.datetime.now()
no = 0
names = pd.read_csv("pink.csv")
#print(len(names))
for i in range(0 , len(names)):
    print(names.loc[i]['name'].title());
    img = Image.open("certificate.png")
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("a.ttf", 50)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((200, 600),names.loc[i]['name'].title(),(0,0,0),font=font)
    img.save('Generated/'+names.loc[i]['mail'].lower()+'.png')
    no = i
b = datetime.datetime.now()
t = b-a
print(str(no)+" Certificate Generated in "+str(t)+ " Sec.")