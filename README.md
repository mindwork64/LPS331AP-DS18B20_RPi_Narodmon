### Настройка I2C на Raspberry Pi
[Настройка I2C](http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi)

Поиск адреса датчика
`sudo i2cdetect -y 0` или `sudo i2cdetect -y 1`

Адрес устройства скорее всего будет **5d** или  **5c**  
Далее, полный адрес вида **0x5d** необходимо указать в начале скрипта
