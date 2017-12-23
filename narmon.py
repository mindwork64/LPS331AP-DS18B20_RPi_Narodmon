#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import smbus
import fnmatch
import os

# MAC адрес сетевой карты устройства. Заменить на свой!
DEVICE_MAC = '00:00:00:00:00:00'
LP_ADDR = '0x5d'

# Имена датчиков. Если надо больше или меньше соотвественно добавляем или удаляем строку, не забывая изменить номер.
SENSOR_ID_1 = 'T1'
SENSOR_ID_2 = 'T2'
SENSOR_ID_3 = 'P1'

# Читаем значения датчиков

# Первым идёт DS18B20, если другой, меняем код под себя.
temperature = []
IDs = []
for filename in os.listdir("/sys/bus/w1/devices"):
  # В следующей строке меняем адрес датчика на свой который есть в /sys/bus/w1/devices/ и начинается на 28-
  if fnmatch.fnmatch(filename, '28-0317621d49ff'):
    with open("/sys/bus/w1/devices/" + filename + "/w1_slave") as fileobj:
        lines = fileobj.readlines()
    if lines[0].find("YES"):
        pok = lines[1].find('=')
        temperature.append(float(lines[1][pok+1:pok+7])/1000)
        IDs.append(filename)
    else:
          logger.error("Error reading sensor with ID: %s" % (filename))


# Включаем и работаем с показаниями датчика LPS331AP
bus = smbus.SMBus(1)
bus.write_byte_data(LP_ADDR, 0x20, 0b10000100)
bus.write_byte_data(LP_ADDR,0x21, 0b1)
Temp_LSB = bus.read_byte_data(LP_ADDR, 0x2b)
Temp_MSB = bus.read_byte_data(LP_ADDR, 0x2c)
count = (Temp_MSB << 8) | Temp_LSB
comp = count - (1 << 16)

# Расчитываем температуру по формуле из даташита.
Temp = 42.5 + (comp/480.0)

###### Давление
Pressure_LSB = bus.read_byte_data(LP_ADDR, 0x29)
Pressure_MSB = bus.read_byte_data(LP_ADDR, 0x2a)
Pressure_XLB = bus.read_byte_data(LP_ADDR, 0x28)
count = (Pressure_MSB << 16) | ( Pressure_LSB << 8 ) | Pressure_XLB

По формуле из даташита вычисляем давление в мм.рт.ст.
Pressure = ((count/4096.0)/1000)*750.064

sock = socket.socket()

# Подключаемся
try:
    sock.connect(('narodmon.ru', 8283))
# Создаём маску, заносим в неё данные и передаём их
    sock.send("#{}\n#{}#{}\n#{}#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, str(temperature)[1:-1], SENSOR_ID_2, str(Temp)[0:-1], SENSOR_ID_3, str(Pressure)[0:5]))

# Получаем ответ
    d_recv=sock.recv(1024)
    sock.close()
    print d_recv
except socket.error, e:
    print('ERROR! Exception {}'.format(e))

print str(temperature)[1:-1]
print str(Temp)[0:-1]
print str(Pressure)[0:5]
