import smtplib
from email.mime.text import MIMEText

def send_email(message,subject,toaddrs):

    fromaddr = 'intruders.iot@gmail.com'
    username = 'intruders.iot@gmail.com'
    password = 'rajupal8'     
    msg = MIMEText(message, 'html')    
    msg['Subject']  = subject    
    msg['From']=fromaddr    
    msg['Reply-to'] = 'no-reply'    
    msg['To'] = toaddrs  
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()    
    server.starttls()
    server.ehlo()    
    server.login(username,password)    
    server.sendmail(fromaddr, [toaddrs], msg.as_string())
    server.quit()
   
"""
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()

"""


"""subject = raw_input("Enter subject\n")
message = raw_input("Enter message\n")
toaddrs = raw_input("Enter receiver email address\n")
send_email(str(message),str(subject),str(toaddrs))"""



#https://myaccount.google.com/lesssecureapps