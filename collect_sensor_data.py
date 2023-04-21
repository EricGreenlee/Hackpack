import SHT30
import os
import time
import csv
"""
os.system('echo gpio | sudo tee /sys/class/leds/led0/trigger')

while(1):
	os.system('echo 1 | sudo tee /sys/class/leds/led0/brightness')
	time.sleep(0.8)
	os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
	time.sleep(0.2)

"""
#settings
sens_name = "sens001"
fname_hack = "/home/hackpack1/sensor/hackpack_sensor_data.csv"
fname_backup = "backup_sensor_data.csv"
sleep_interval = 1 #seconds

thsen = SHT30.SHT30(powerpin=6)


while(1):
	humid, temp, crcH, crcT = thsen.fast_read_humidity_temperature_crc()
	data = [[sens_name,time.time(),temp, humid]]
	print(data)
	with open(fname_hack, "a+", newline="") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(data)
	time.sleep(sleep_interval)

