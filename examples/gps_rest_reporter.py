from ublox_gps import UbloxGps
import numpy as np
import threading
import flask
from flask import request, jsonify

from hoverfly_gps_spy.gps_spy import GPSSpy
from hoverfly_pgs_spy.serial_socket import SerialSocket


NUM_SATS = 71
PORT_NUM = 15566
SIG_LEN = 5
THRESH = 40000

port = SerialSocket(PORT_NUM)
gps = UbloxGps(port)

spy = GPSSpy(signal_len=SIG_LEN, num_sats=NUM_SATS, threshold=THRESH)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/jammed', methods=['GET'])
def isJammed():
    return jsonify(jammed=spy.jammed)

def background():
  try:
    print("Listenting for UBX Messages.")
    while True:
      try:
        sats = gps.satellites()
        next_cno = np.zeros(NUM_SATS)
        sat_dat = [(s.svId, s.cno) for s in sats.RB]
        for val in sat_dat:
            next_cno[val[0]] = val[1]
      except (ValueError, IOError):
          pass

  finally:
    port.close()


if __name__ == '__main__':
    threading.Thread(target=background).start()
    app.run()
