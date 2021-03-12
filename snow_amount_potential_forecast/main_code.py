#!/usr/bin/env python
# coding: utf-8


#################################################################################################
#                                  Sym HEX							#
#												#
#	Coded by Eduardo O. Rodrigues								#
#     												#
#	the currently code download a website image time-by-time(defined by user)		#
#	after, it sends the image via e-mail protocol to your selected "TARGET_EMAIL"		#
#	via SENDER_EMAIL									#
#												#
#     Technology used: Python 3.6+								#
#												#
#												#
#################################################################################################




#SOME DEFINITIONS
TIME_SLEEPING = 120                             #IN SECONDS
SENDER_EMAIL = ''                               #TYPE THE EMAIL THAT WILL SEND THE FORECAST (EMAIL THAT WAS CREATED THE APP PASSWORD IN STEPS THAT I SENT)
TARGET_EMAIL = ''                               #EMAIL THAT YOU RECEIVE THE SNOW AMOUNT FORECAST
GOOGLE_APP_PASSWORD = ''                        #SAME FROM THE STEPS THAT I SENT TO YOU TO FOLLOW TO CREATE A PASSWORD APP

import sys
import subprocess


try:
    print('Trying to install all needed packages. Wait a minute')
    # implement pip as a subprocess:
######### importing requests
    try:
        print('trying to import requests: ')
        import requests
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
            'requests'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)
######### importing requests_html
##    try:
##        print('trying to import requests_html: ')
##        from requests_html import HTMLSession
##        print('success')
##    except:
##        print('Not possible, trying to install')
##        try:
##            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
##    'requests_html'])
##            print('Packages installed sucessfully...')
##        except Exception as e2:
##            print(e2)

######### importing pillow

    try:
        print('trying to import pillow: ')
        from PIL import Image
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'Pillow'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)
            
######### importing bs4
    try:
        print('trying to import bs4: ')
        from bs4 import BeautifulSoup
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'bs4'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)
    
######### importing smtplib
    try:
        print('trying to import smtplib: ')
        import smtplib
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'smtplib'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)    
    
######### importing email.message
    try:
        print('trying to import EmailMessage: ')
        from email.message import EmailMessage
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'email.message'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)

######### importing mimetype
    try:
        print('trying to import mimetypes: ')
        import mimetypes
        print('success')
    except:
        print('Not possible, trying to install')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
    'mimetypes'])
            print('Packages installed sucessfully...')
        except Exception as e2:
            print(e2)   
    


######### all imports finished to lets pass
    print('Starting forecast getter')
except Exception as e:
    print("Failed to install the packages")
    print(e)

import requests
#from requests_html import HTMLSession
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
#time module
import time
#email modules
import time
import smtplib
from email.message import EmailMessage
import mimetypes


# In[100]:


#email appp password
google_app_password = GOOGLE_APP_PASSWORD
sender_email = SENDER_EMAIL
target_email = TARGET_EMAIL

img1_bytes = None
img2_bytes = None

weblink='https://www.weather.gov/okx/winter#tab-2'

while(True):

    r = requests.get(weblink)
    parse = BeautifulSoup(r.text, 'html.parser')

    img_link = parse.find_all(id='stsImg')[0].attrs['src']
    new_img_link = 'https://www.weather.gov'+img_link
	new_img_link
    img_req = requests.get(new_img_link)
    img1_bytes = img_req.content
    try:
        img2_bytes = open(r'.old_forecast', 'rb')
        img2_bytes = img2_bytes.read()
        
    except:
        d = open(r'.old_forecast', 'wb')
        d.close()
    #first it verify if the old img/pdf is equal to new one
    #if not he pass
    if(img1_bytes == img2_bytes):
        print('Forecast not changed')
        pass
    else:
        img_saved = Image.open(BytesIO(img_req.content))
        img2 = img_saved.convert('RGB')
        file_name_forecast = r'forecast_img.pdf'
        img2.save(file_name_forecast)
        try:
            #sending e-mail
            server = smtplib.SMTP('smtp.gmail.com:587')
            body_message = 'There is the new updated forecast for the region.<br> Snow Amount Potential Update'
            msg = EmailMessage()
            msg['From'] = sender_email
            msg['To'] = target_email
            msg['Subject'] = 'Snow Amount Potential wheater forecast'
            password = google_app_password
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(body_message)
            #msg.preamble = body_message
            #loading pdf to attach and add to email body
            path = file_name_forecast
            # Guess the content type based on the file's extension.
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as fp:
                msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, 
                                   filename=file_name_forecast)
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print("email sent")
        except Exception as e:
            print('Error ocurred: ', e)
        #resetting some infos and setting another
        img2_bytes = img1_bytes
        saved_img = open(r'.old_forecast', 'wb')
        saved_img.write(img2_bytes)
        saved_img.close()
    print(f'TIME>> {time.localtime().tm_mon}/{time.localtime().tm_mday}/{time.localtime().tm_year} - {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}')    
    time.sleep(TIME_SLEEPING)



