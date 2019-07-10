import hmac
import time
import hashlib

from functools import wraps
from flask import request, make_response, jsonify, g

DATA_VIZ_SIGNING_KEY = "YOUR_SIGNING_KEY_ASK_LUMAPPS_SUPPORT"

def is_data_viz_call(f):
    def http401(message):
        print(message)
        return make_response(jsonify({"error": message}), 401)

    @wraps(f)
    def wrap(*args, **kwargs):
        lumapps_hash = request.headers.get("X-LumApps-Hash")
        lumapps_message = request.headers.get("X-LumApps-Message")

        if not lumapps_hash or not lumapps_message:
            return http401("Missing headers")

        _hash = hmac.HMAC(
            bytes(DATA_VIZ_SIGNING_KEY, encoding="utf-8"),
            lumapps_message.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        try:
            user_email, timestamp_str = lumapps_message.split(":")
            timestamp = int(timestamp_str)
        except Exception:
            return http401("Malformed headers")

        if not _hash == lumapps_hash:
            return http401("Invalid hash")

        if timestamp < time.time() - 60:
            return http401("Message too old")

        g.email = user_email
        return f(*args, **kwargs)

    return wrap


from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route("/")
@is_data_viz_call
def main():
    return make_response(
        jsonify({"confidential": {"margin": "0.081", "target": "0.09"}})
    )
