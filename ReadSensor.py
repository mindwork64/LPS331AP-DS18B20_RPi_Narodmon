import smbus

# Sensor address, detected by using 'sudo i2cdetect -y 0' or 'sudo i2cdetect -y 1' accordingly
SENSOR_ADDRESS = "0x5d"

# init bus
bus = smbus.SMBus(1)

# Power up LPS331AP pressure sensor & set BDU bit
bus.write_byte_data(SENSOR_ADDRESS, 0x20, 0b10000100)

# Write value 0b1 to register 0x21 on device at address SENSOR_ADDRESS
bus.write_byte_data(SENSOR_ADDRESS,0x21, 0b1)

Temp_LSB = bus.read_byte_data(SENSOR_ADDRESS, 0x2b)
Temp_MSB = bus.read_byte_data(SENSOR_ADDRESS, 0x2c)

# Combine LSB & MSB
count = (Temp_MSB << 8) | Temp_LSB

# As value is negative convert 2's complement to decimal
comp = count - (1 << 16)

# Calc temp according to data sheet
Temp = 42.5 + (comp/480.0)

print "Temperature: %.2f" % Temp

Pressure_LSB = bus.read_byte_data(SENSOR_ADDRESS, 0x29)
Pressure_MSB = bus.read_byte_data(SENSOR_ADDRESS, 0x2a)
Pressure_XLB = bus.read_byte_data(SENSOR_ADDRESS, 0x28)

count = (Pressure_MSB << 16) | ( Pressure_LSB << 8 ) | Pressure_XLB
#comp = count - (1 << 24)
# Pressure value is positive so just use value as decimal 

# Getting pressure value in mbars
Pressure = count/4096.0
# Comment line above and uncomment one below to get value in mm.Hg
#Pressure = ((count/4096.0)/1000)*750.064

print "Pressure: %.2f" % Pressure


