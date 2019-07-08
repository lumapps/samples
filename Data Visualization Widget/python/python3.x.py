import time
import hmac
import hashlib
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route("/")
def main():
    """
    Sample API that checks the authentication headers passed by LumApps
    """
    lumapps_hash = request.headers["X-LumApps-Hash"]  # header containing the hmac hash
    lumapps_message = request.headers[
        "X-LumApps-Message"
    ]  # header containing the hmac message

    _hash = hmac.HMAC(
        bytes(SECRET_KEY, encoding='utf-8'),  # shared secret token
        lumapps_message.encode('utf-8'),  # the encoded message
        digestmod=hashlib.sha256,  # the algorithm used to hash the message
    ).hexdigest()

    # The message contains the user making the call and the timestamp
    # It's formatted like so : user@domain.tld:12345
    # Where user@domain.tld is the connected user email address and 12345 the timestamp of the call
    user_email, timestamp = lumapps_message.split(":")

    if (
        _hash != lumapps_hash  # check that the hash is correct
        or int(timestamp) < time.time() - 60  # check that the message is not an old one
    ):
        # /!\ The hash was not correct or the request was too old, the request has not been made by LumApps, reject it
        return make_response(
            jsonify(
                {
                    "error": "Error : the message has not been hashed properly or is too old."
                }
            ),
            401,
        )

    # The hash was correct and the timestamp fresh, it's a call made by LumApps, return the data you want to display
    return make_response(
        jsonify({"confidential": {"margin": "0.081", "target": "0.09"}})
    )


app.run()