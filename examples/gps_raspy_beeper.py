from ublox_gps import UbloxGps
import RPi.GPIO as GPIO 
import serial
import numpy as np

from gpsspy.gps_spy import GPSSpy


NUM_SATS = 255
port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
gps = UbloxGps(port)

spy = GPSSpy(signal_len=5, num_sats=NUM_SATS)

buzzer = 13
buzzCount = 0



def run():

  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(buzzer, GPIO.OUT)
  GPIO.output(buzzer, GPIO.LOW)

  try:
    print("Listenting for UBX Messages.")
    while True:
      try:
        buzzCount += 1
        if buzzCount > 0:
            buzzCount = 0
            GPIO.output(buzzer, GPIO.HIGH)
        sats = gps.satellites()
        next_cno = np.zeros(NUM_SATS)
        sat_dat = [(s.svId, s.cno) for s in sats.RB]
        for val in sat_dat:
            next_cno[val[0]] = val[1]
        print(spy.step(next_cno))
        if(spy.jammed):
            GPIO.output(buzzer, GPIO.HIGH)
            buzzCount = -10
      except (ValueError, IOError) as err:
        print(err)

  finally:
    port.close()


if __name__ == '__main__':
  run()
