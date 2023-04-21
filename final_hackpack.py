import serial
import time
import os
import logging

phone_comm = "/dev/rfcomm0"
sensor_comm = "/dev/rfcomm1"

data_file = "rx_sensor_data.csv"
log_file = "logfile.txt"
counter = 0

# Wait for phone to connect
# If you disconnect the phone afterwards, restart the hackpack
logging.basicConfig(filename=log_file,level=logging.DEBUG)

logging.debug("began successfully")


while True:
	try:
		phone_ser = serial.Serial(phone_comm)
	except:
		continue
	phone_ser.write('Phone Connected. Beginning operation.\n'.encode('ascii'))
	phone_ser.close()
	break

# Check if the sensor is connected. If it just started connecting
# send a confirmation to the phone
while True:
	try:
		sensor_ser = serial.Serial(sensor_comm)
	except:
		# Sensor is not connected, tell the user, try again in 5 sec
		print("No sensor")
		with serial.Serial(phone_comm) as phone_ser:
			msg = "No connection to Sensor\n".encode('ascii')
			phone_ser.write(msg)
			time.sleep(1)

		continue
	# Sensor is connected
	size = 0
	print("Sensor is connected")
	try:
		size = int(sensor_ser.read_until().decode('ascii'))
	except:
		logging.exception("failed to read from sensor")
	print("size: "+str(size))

	with serial.Serial(phone_comm) as phone_ser:
		phone_ser.timeout = None
		msg = "Connected to Sensor. Do not step too far away!\n".encode('ascii')
		phone_ser.write(msg)
		# ask if phone wants the data, TODO: add size and time
		msg = f"Sensor data is {size} bytes\n".encode('ascii')
		phone_ser.write(msg)
		duration = round(size/477,1)
		msg = f"expected time is {duration} seconds\n".encode('ascii')
		phone_ser.write(msg)
		msg = "Collect data? (Y/N)\n".encode('ascii')
		phone_ser.write(msg)
		#rsp = phone_ser.read(1).decode('ascii')
		#phone_ser.reset_input_buffer()

		while True:
		# Wait for phone response
			rsp = phone_ser.read(1).decode('ascii')
			phone_ser.reset_input_buffer()
			if rsp == 'Y':
				msg = "commencing data download, standby\n".encode('ascii')
				phone_ser.write(msg)
			#if 'Y' == 'Y':
				# Yes
				# Save the data to the hackpack
				# Print to the phone
				# After sending, declare any errors or warnings

				msg = "REQUEST_DATA\n".encode('ascii')
				counter = 0
				done = 0
				file = open(data_file,"a+")
				sensor_ser.write(msg)
	
				while (counter < int(size)):
			#while (done != 1):
					data = sensor_ser.read().decode('ascii')
				#data = sensor_ser.read_until().decode('ascii')
				#data = sensor_ser.read_until("!").decode('ascii')
				#sensor_ser.close()
					print(data)
					file.write(data)
					print(str(counter)+"/"+str(size))
				#file.write("\n")
					counter += 1
				#if (data == "stop"):
				#	print("Done!")
				#	done = 1
				#	sensor_ser.close()
				#	break
				phone_ser.write("Data finished recording\n".encode('ascii'))
			#break
				print("done receiving data")
				file.close()
				rsp = " "
				with open(data_file,"r") as file:
					lines = file.readlines()
					last_line = lines[-1].strip()
					message = f"Last line of data: {last_line}\n".encode('ascii')
					phone_ser.write(message)

				time.sleep(5)
			elif rsp.strip() == 'N':
				msg = "DO_NOT_SEND\n".encode('ascii')
				sensor_ser.write(msg)
				#sensor_ser.close()
				phone_ser.write("Data not recorded\n".encode('ascii'))
				break
			else:
				msg = "Error, please Enter Y or N\n".encode('ascii')
				phone_ser.write(msg)


			#phone_ser.write("Sleeping for 5 seconds\n".encode('ascii'))
			#time.sleep(5)

