from ublox_gps import UbloxGps
import serial
import numpy as np

from HoverflyGPSDetector.gps_jamming_detector import GPSSpy
# Can also use SPI here - import spidev
# I2C is not supported

port = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
gps = UbloxGps(port)

spy = GPSSpy(signal_len=5, num_sats=24)


def run():
  try:
    print("Listenting for UBX Messages.")
    while True:
      try:
        sats = gps.satellites()
        next_cno = np.zeros(24)
        sat_dat = [(s.svId, s.cno) for s in sats.RB]
        for val in sat_dat:
            next_cno[val[0]] = val[1]
        spy.step(next_cno)
        print(spy.decision_variable)
      except (ValueError, IOError) as err:
        print(err)

  finally:
    port.close()


if __name__ == '__main__':
  run()
