from ublox_gps import UbloxGps
import RPi.GPIO as GPIO 
import serial
import numpy as np
import time

from gpsspy.gps_spy import GPSSpy


NUM_SATS = 255
port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
gps = UbloxGps(port)

spy = GPSSpy(signal_len=5, num_sats=NUM_SATS)


timestr = time.strftime("%Y%m%d-%H%M%S")



def run():
    jamming_known = False
    buzzer = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(buzzer, GPIO.LOW)
    buzzDrive = GPIO.PWM(buzzer, 2000)
    # with open("/home/pi/hti/logging/gps_jamming/"+timestr+".csv", 'w') as logFile:
    # logFile.write("Time,CNO,Jammed\n")
    try:
        print("Listening for UBX Messages.")
        buzzDrive.start(70)
        time.sleep(1)
        buzzDrive.stop()
        time.sleep(1)
        buzzDrive.start(70)
        time.sleep(1)
        buzzDrive.stop()
        while True:
            try:
                sats = gps.satellites()
                next_cno = np.zeros(NUM_SATS)
                sat_dat = [(s.svId, s.cno) for s in sats.RB]
                for val in sat_dat:
                    next_cno[val[0]] = val[1]
                val = spy.step(next_cno)
                print(val, spy.jammed, jamming_known)
                # logFile.write("{},{},{}\n".format(time.time(), val, spy.jammed))
                if spy.jammed and not jamming_known:
                    jamming_known = True
                    buzzDrive.start(70)
                elif not spy.jammed and jamming_known:
                    jamming_known = False
                    buzzDrive.stop()
            except (ValueError, IOError, IndexError) as err:
                print(err)

    finally:
        port.close()
        GPIO.cleanup()


if __name__ == '__main__':
  run()
