 # -*- coding: utf-8 -*-
import hmac
import time
import hashlib

from functools import wraps
from flask import Flask, request, make_response, jsonify

# shared secret token
DATA_VIZ_SIGNING_KEY = "YOUR_SIGNING_KEY_ASK_LUMAPPS_SUPPORT"

def is_data_viz_call(f):
    def http401(message):
        # The request has not been made by LumApps, reject it
        return make_response(jsonify({"error": message}), 401)

    @wraps(f)
    def wrap(*args, **kwargs):
        # header containing the hmac hash
        lumapps_hash = request.headers.get("X-LumApps-Hash")
        # header containing the hmac message
        lumapps_message = request.headers.get("X-LumApps-Message")

        if not lumapps_hash or not lumapps_message:
            return http401("Missing headers")

        _hash = hmac.HMAC(
            DATA_VIZ_SIGNING_KEY,
            lumapps_message,
            digestmod=hashlib.sha256,
        ).hexdigest()

        try:
            """ The message contains the user making the call and the timestamp
            It's formatted like so : user@domain.tld:12345
            """
            user_email, timestamp_str = lumapps_message.split(":")
            timestamp = int(timestamp_str)
        except Exception:
            return http401("Malformed headers")

        # The hash was not correct
        if not _hash == lumapps_hash:
            return http401("Invalid hash")

        # The request was too old
        if timestamp < time.time() - 60:
            return http401("Message too old")

        """ The hash was correct and the timestamp fresh, 
        it's a call made by LumApps, the decorated function will be executed
        """
        return f(*args, **kwargs)

    return wrap


app = Flask(__name__)

@app.route("/html")
@is_data_viz_call
def html():
    return make_response("<ul><li>Result 8</li><li>Result 1</li><ul>")

@app.route("/pie")
@is_data_viz_call
def pie():
    return make_response("January,February,March,April,May\n193,284,413,440,137")

@app.route("/table")
@is_data_viz_call
def table():
    return make_response("Store,Turnover,Sales\nParis,73127,764\nNew York,148076,521")

if __name__ == "__main__":
    app.run(threaded=True)