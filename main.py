'''
Author: Matt Waddell

Use:
This script will connect to PacktPub's website and add the book to your library.

Resources:
http://www.programcreek.com/python/index/402/pycurl
https://curl.haxx.se/libcurl/c/curl_easy_setopt.html
http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/

Files:
https://curl.haxx.se/ca/cacert.pem

Python:
Version 3
'''

import pycurl
from io import BytesIO

#Script Settings
website = 'https://www.packtpub.com/packt/offers/free-learning'                 #Packtpub website address
cert = ''                                                                       #Root Certificate Path
user = ''                                                                       #Your PacktPub Login
password = ''                                                                   #Your PacktPub Password

try:
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.USERAGENT, 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 8)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
    c.setopt(c.COOKIEFILE, '')
    c.setopt(c.SSL_VERIFYPEER, 1)
    c.setopt(c.SSL_VERIFYHOST, 2)
    c.setopt(c.CAINFO, cert)
    #c.setopt(c.VERBOSE, True)

    print('\nGrabbing ' + website + ' for processing...\n')

    c.setopt(c.URL, website)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    body = buffer.getvalue().decode('iso-8859-1')
    buildStart = body.find('form_build_id') + 19
    buildEnd = buildStart + 37
    buildID = body[buildStart : buildEnd]
    post = 'email=' + user.replace('@', '%40') + '&password=' + password + '&op=Login&form_build_id=' + buildID + '&form_id=packt_user_login_form'

    print('\nLogging into website...\n')

    c.setopt(c.URL, website)
    c.setopt(c.POSTFIELDS, post)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()

    print('\nFinding free book of the day...\n')

    body = buffer.getvalue().decode('iso-8859-1')
    linkStart = body.find('/freelearning-claim/')
    linkEnd = body.find('"', linkStart)
    link = 'https://www.packtpub.com' + body[linkStart : linkEnd]
    bookStart = body.find('<h2>', body.find('dotd-title')) + 4
    bookEnd = body.find('</h2>', bookStart)
    title = body[bookStart : bookEnd].strip()

    print('\nAdding book ' + title + ' to your library...\n')

    c.setopt(c.URL, link)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

except pycurl.error as error:
    errno, errstr = error
    print('Error: ', errstr)
