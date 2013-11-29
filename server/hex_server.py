from hex_driver import HexDriver, FrameError
from flask import Flask, request
import time

hexDriver = HexDriver()
app = Flask(__name__)
@app.route('/update')
def updateLights():
    params = {}    
    for k, v in request.args.iteritems():
        params[k] = int(v)
    try:
        return hexDriver.send_frame(params)
    except FrameError:
        return "INVALID PARAMS"

@app.route('/')
def page():
    with open('hex_index.html') as index:
        return index.read()
    
#app.run(debug=True)
app.run('0.0.0.0', port=80)
