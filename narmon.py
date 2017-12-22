#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import smbus
import fnmatch
import os

# MAC адрес устройства. Заменить на свой!
DEVICE_MAC = 'B8:27:EB:DC:B2:26'

#Имена датчиков
SENSOR_ID_1 = 'T1'
SENSOR_ID_2 = 'T2'
SENSOR_ID_3 = 'P1'

#Читаем значения датчиков
temperature = []
IDs = []
for filename in os.listdir("/sys/bus/w1/devices"):
  if fnmatch.fnmatch(filename, '28-0317621d49ff'):
    with open("/sys/bus/w1/devices/" + filename + "/w1_slave") as fileobj:
        lines = fileobj.readlines()
    if lines[0].find("YES"):
        pok = lines[1].find('=')
        temperature.append(float(lines[1][pok+1:pok+7])/1000)
        IDs.append(filename)
    else:
          logger.error("Error reading sensor with ID: %s" % (filename))

bus = smbus.SMBus(1)
bus.write_byte_data(0x5c, 0x20, 0b10000100)
bus.write_byte_data(0x5c,0x21, 0b1)
Temp_LSB = bus.read_byte_data(0x5c, 0x2b)
Temp_MSB = bus.read_byte_data(0x5c, 0x2c)
count = (Temp_MSB << 8) | Temp_LSB
comp = count - (1 << 16)
Temp = 42.5 + (comp/480.0)
Pressure_LSB = bus.read_byte_data(0x5c, 0x29)
Pressure_MSB = bus.read_byte_data(0x5c, 0x2a)
Pressure_XLB = bus.read_byte_data(0x5c, 0x28)
count = (Pressure_MSB << 16) | ( Pressure_LSB << 8 ) | Pressure_XLB
Pressure = ((count/4096.0)/1000)*750.064

sock = socket.socket()

#Подключаемся
try:
    sock.connect(('narodmon.ru', 8283))
#Создаём маску, заносим в неё данные и передаём их
    sock.send("#{}\n#{}#{}\n#{}#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, str(temperature)[1:-1], SENSOR_ID_2, str(Temp)[0:-1], SENSOR_ID_3, str(Pressure)[0:5]))

#Получаем ответ
    d_recv=sock.recv(1024)
    sock.close()
    print d_recv
except socket.error, e:
    print('ERROR! Exception {}'.format(e))

print str(temperature)[1:-1]
print str(Temp)[0:-1]
print str(Pressure)[0:5]
