# Python Certificate Mailer (c)
###### Created on Tue Feb 20 19:52:40 2018
###### Author: Prashant Kumar

```
certi = Editor("certificate.png")
certi.setFont("a.ttf", 150)
certi.setLocation(0, 0)
certi.writeName('YOUR NAME')
certi.save('example@example.com')

mailler = Mailler('user', 'password')
mailler.login()
mailler.send('example@example.com', "Generated/example@example.com.png")
mailler.logout()
print("Mailled to \tNAME\t\texample@example.com");
```
