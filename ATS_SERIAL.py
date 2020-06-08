import serial.tools.list_ports
import MySQLdb
import threading
import time
import os

global db_host
global usuario
global clave
global base_de_datos

global queryList
queryList = []

global mysqlDefFlag
mysqlDefFlag = []

db_host = "hmiatsd.byethost31.com"
usuario = "hmiatsdb_ats"
clave = "m3c464r0n"
base_de_datos = "hmiatsdb_ats_prueba"

def serConnect():
    print("Conectando puerto serie...")
    while True:
        try:
            ser = serial.Serial('/dev/serial/by-id/usb-FTDI_USB__-__Serial-if00-port0', baudrate=38400, bytesize=serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_EVEN, timeout=None, rtscts=0, write_timeout=5, dsrdtr=0, inter_byte_timeout=None , xonxoff=True)
#            ser = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0', baudrate=38400, bytesize=serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_EVEN, timeout=None, rtscts=0, write_timeout=5, dsrdtr=0, inter_byte_timeout=None , xonxoff=True)
            ser.flushInput()
            ser.flushOutput()
            readLoop(ser) 
            break
        except:
            None

def readLoop(ser):
    time.sleep(4)
    linea = b''
    iLinea = False
    firstLine = True
    lenLinea = 152

    lCompleta = False
    cntCRC = 0
    lenCRC = 2
    CRC = b''
    crcCalc = b''
    
    print(ser.get_settings())
    ser.flush()
    
    ser.write(b'\x01\x52')
    ser.write(b'\x05')
    while True:
        try:
            if ser.in_waiting > 0:
                dato = ser.read()
                for posBit in range (1, len(dato)+1):
                    if lCompleta == False:
                        if iLinea == False:
                            if dato[posBit-1:posBit] == b'\x02':
                                iLinea = True
                                linea = b''
                                cscCalc = b''
                        else:
                            if dato[posBit-1:posBit] == b'\x02':
                                linea = b''
                                csrCalc = b''
                            elif dato[posBit-1:posBit] != b'\x03':
                                linea += dato[posBit-1:posBit]
                                if crcCalc == b'':
                                    crcCalc = str(dato[0][posBit-1:posBit].hex()).encode('ascii')
                                else:
                                    crcCalc = xor(crcCalc, str(dato[0][posBit-1:posBit].hex()).encode('ascii'))
                            else:
                                if len(linea) == lenLinea:
                                    lCompleta = True
                    else:
                        cntCRC += 1
                        CRC += dato[0][posBit-1:posBit]
                        if cntCRC == lenCRC:
                            linea += CRC
                            if str(CRC)[2:4] == str(crcCalc.hex()[1:2].upper() + crcCalc.hex()[3:4].upper()):
                                mi_query = "(CURRENT_DATE,CURRENT_TIME, x'" + str(linea)[2:len(str(linea))-1] + "')"
                                queryList.append(mi_query)
                                if  len(mysqlDefFlag) == 0:
                                    mysqlThread = threading.Thread(target=mysqlDef, daemon = True)
                                    mysqlThread.start()
                            linea = b''
                            iLinea = False
                            lCompleta = False
                            cntCRC = 0
                            CRC = b''
                            crcCalc = b''                            
            ser.write(b'\x05')
        except:
            mi_query = "(CURRENT_DATE,CURRENT_TIME, x'FFFFFFFFFFFFFF00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')"
            queryList.append(mi_query)
            if  len(mysqlDefFlag) == 0:
                mysqlThread = threading.Thread(target=mysqlDef, daemon = True)
                mysqlThread.start()
            print ("Puerto serie desconectado")
            serConnect()


def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def mysqlDef():
    print ("\n mysqlDef: Running \n")
    mysqlDefFlag.append(1)
    while True:
        try:
            db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
            cursor = db.cursor()
            break
        except:
            None

    maxLenQuery = 10000        
    while len(queryList) > 0:        
        try:
            long = len(queryList)
            if long > maxLenQuery:
                long = maxLenQuery
            query = "INSERT INTO `datos_bats`(`dia_serv`, `hora_serv`, `cadena`) VALUES "
            smp = False
            for i in range(0, long):
                if smp == False:
                    smp = True
                    query += queryList[0]
                else:
                    query += "," + queryList[0]
                queryList.pop(0)
            cursor.execute(query)
            print (query)
        except:
            while True:
                try:
                    db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
                    cursor = db.cursor()
                    break
                except:
                    None
    try:
        db.commit()
        cursor.close()
    except:
        None
        
    mysqlDefFlag.clear()
    print ("\n mysqlDef: Closed \n")


def iAmAliveDef():
    print ("\n iAmAliveDef: Running \n")
    while True:
        try:
            db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
            cursor = db.cursor()
            #INFORMO: LINEA, NUMERO TREN, CHAPA TREN, MODELO, VERSION DE FIRMWARE, 
            query = "UPDATE `datos_tr` SET `linea` = 'PRUEBA', `num_tren` = '0', `chapa_tren` = 'M0', `modelo` = 'PRUEBA', `version_fw` = '1.2.0' WHERE 1"
            cursor.execute(query)
            break
        except:
            None
            
    salir = False
    while (salir == False):
        time.sleep(60)
        try:
            #ACTUALIZO LA HORA PARA INDICAR QUE EL MODULO ESTA VIVO
            query = "UPDATE `datos_tr` SET `hora_serv` = CURRENT_TIME, `dia_serv` = CURRENT_DATE WHERE 1"
            cursor.execute(query)
            
            #ME FIJO EL ESTADO DE COMANDO PARA VER SI DEBO EJECUTAR UN COMANDO BASH
            query = "SELECT `comando` FROM `datos_tr` WHERE 1"
            cursor.execute(query)
            result = cursor.fetchall()
            if result[0][0] == 1:
                query = "UPDATE `datos_tr` SET `comando` = 8 WHERE 1"
                cursor.execute(query)
                break
        except:
            while True:
                try:
                    db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
                    cursor = db.cursor()
                    break
                except:
                    None
    try:
        db.commit()
        cursor.close()
        print ("\n iAmAliveDef: Closed \n")
        os.system('reboot')
    except:
        None


iAmAliveThread = threading.Thread(target=iAmAliveDef, daemon = True)
iAmAliveThread.start()

serConnect()
