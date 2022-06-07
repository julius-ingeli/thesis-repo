#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2020/10/16
########################################################################
import RPi.GPIO as GPIO
import time
from datetime import datetime
import csv
import Freenove_DHT as DHT
import mysql.connector as sqlc


#SQL SETUP
mydb = sqlc.connect(
host = "192.168.100.101",
user = "pi",
password = "123",
database='mydb',
auth_plugin='mysql_native_password')
print("connection complete.")
mycursor = mydb.cursor()


DHTPin = 11     #define the pin of DHT11
redLEDPin = 18  #define red LED pin
grnLEDPin = 16  #define green LED pin

#setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redLEDPin,GPIO.OUT)
GPIO.output(redLEDPin,GPIO.LOW)
GPIO.setup(grnLEDPin,GPIO.OUT)
GPIO.output(grnLEDPin,GPIO.LOW)

#CSV header
header = ["Number",'Timestamp','Status','Temperature','Humidity'] 


def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    counts = 0 # Measurement counts
    while(True):
        counts += 1
        print("Measurement counts: ", counts)
        for i in range(0,15):            
            chk = dht.readDHT11()     
            if (chk is dht.DHTLIB_OK):      
                status = "DHT11,OK!"
                GPIO.output(grnLEDPin,GPIO.HIGH)
                print(status)
                break
            else:
                status = "DHT11,NOT OK!"
                GPIO.output(redLEDPin,GPIO.HIGH)
                print(status)
                break    
            time.sleep(0.1)
            
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))

        #timestamp
        timestamp = datetime.now() 
        timestamp_sql = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        print(timestamp_sql)
        
        #writing to csv file
        csvdata = [counts,timestamp,status,dht.temperature, dht.humidity]
        writer.writerow(csvdata)

        #sending data to sql
        sql = "INSERT INTO temps (Number, Timestamp, Status, Temperature, Humidity) VALUES (%s,%s,%s,%s,%s)"
        val = (counts,timestamp_sql,status,dht.temperature,dht.humidity)
        mycursor.execute(sql,val)
        mydb.commit()
        print("record sent to database")
        time.sleep(2)
        #shut down LED
        GPIO.output(redLEDPin,GPIO.LOW)
        GPIO.output(grnLEDPin, GPIO.LOW)      
        
if __name__ == '__main__':
    print ('Program is starting ... ')
    f = open('temps.csv', 'w', newline = '', encoding="UTF8")
    writer = csv.writer(f)
    print("file open.")
    writer.writerow(header)
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        f.close()
        exit()  

