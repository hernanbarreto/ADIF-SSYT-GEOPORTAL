from ftplib import FTP
import os

print ('Conectando al FTP')
while True:
    try:
        ftp = FTP('185.2.168.124')
        ftp.login(user='ats@ats-tr.tk', passwd='m3c464r0n')
        break
    except:
        None

print('Descargando ATS_SERIAL.py')
with open('/home/pi/Desktop/ATS_SERIAL.py', 'wb') as fp:
    ftp.retrbinary('RETR ATS_SERIAL.py', fp.write)
    fp.close()
ftp.quit()
print ('Descarga de ATS_SERIAL.py finalizada')

print('Ejecutando ATS_SERIAL.py')
os.system('sudo chmod 755 /home/pi/Desktop/ATS_SERIAL.py')
os.system('sudo /usr/bin/python3 /home/pi/Desktop/ATS_SERIAL.py')
