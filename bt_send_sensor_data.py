import serial
import os
import time
import subprocess
import csv

data_file = "/home/hackpack1/startup/sensor_data.csv"
#data_file = "/home/hackpack1/bt/ex_sensor_data.csv"
hackpack_comm = "/dev/rfcomm0"

if __name__ == "__main__":
	while True:
		# Connect to the hackpack
		while True:
			try:
				hackpack_ser = serial.Serial(hackpack_comm)
			except:
				continue
			breaka
		print("Hackpack Connected")
		# Send the file size
		if os.path.isfile(data_file):
			with open(data_file, "r") as file:
				file_contents = file.read()
			file_size = len(file_contents)
			#file_size = int(os.stat(data_file).st_size)-313
			print(f"File size: {file_size}")
		else:
			file_size = 0
		hackpack_ser.write(f"{file_size}\n".encode('ascii'))

		# Wait for hackpack to request data
		print("Waiting for hackpack response")
		msg = hackpack_ser.read_until().decode('ascii')
		print(msg)
		
		if msg.strip() == "REQUEST_DATA":
			# Read the csv then delete it
			# Send the data to the hackpack
			if file_size > 0:
				with open(data_file, "r") as f:
					for i in range(file_size):
						#contents = f.read(1).decode('ascii')
						contents = f"{f.read(1)}".encode('ascii')
						hackpack_ser.write(contents)
			#with open(data_file) as csv_file:
				#csv_reader = csv.reader(csv_file)
				#count = 0
				#data_chunks = []
				#for row in csv_reader:
				#	data_chunks.append(row)
				#	count += 1
				#	if count <10:
				#		data_bytes=str(data_chunks).encode('ascii')
				#		print(data_bytes)
				#		hackpack_ser.write(data_bytes)
				#		#count = 0
				#		data_chunks = []
				#		time.sleep(0.1)
				#	if count == 10:
				#		data_bytes="stop".encode('ascii')
				#		hackpack_ser.write(data_bytes)
				#contents = f"{f.read(100)}".encode('ascii')
				#contents = "Hello world!".encode('ascii')
				#print(contents)
				#hackpack_ser.write(contents)
				os.remove(data_file)
			print("done sending data")
		# Close the serial comm and sleep
		print("sleeping")
		hackpack_ser.close()
		time.sleep(5)
