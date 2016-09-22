# -*- coding: utf-8 -*-
"""bttn webhook handler."""
from os import getenv
import flask
import hipchat

app = flask.Flask(__name__)

# set of valid channels
CHANNELS = ('hipchat', 'sms')
# set of required form keys
FORM_KEYS = ('channel', 'recipient', 'message')

HIPCHAT_API_TOKEN = getenv('HIPCHAT_API_TOKEN')
TWILIO_ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')


@app.route('/', methods=['POST'])
def bttn_pressed():
    """Respond to a bttn press event."""
    form = flask.request.form

    for key in FORM_KEYS:
        if key not in form:
            return "Request form must include a '%s' key." % key, 400

    if form['channel'] == 'hipchat':
        return send_to_hipchat(form['recipient'], form['message'])
    elif form['channel'] == 'sms':
        return send_sms(form['recipient'], form['message'])
    else:
        return "Unknown channel: '%s'" % form['channel'], 400


def send_to_hipchat(room, message):
    """Forward the button message to HipChat."""
    if not HIPCHAT_API_TOKEN:
        return "Missing HIPCHAT_API_TOKEN environment variable.", 400
    try:
        response = hipchat.send_room_message(room, message, message_format='text')
        return "Message sent successfully", response.status_code
    except hipchat.HipChatError as ex:
        return ex.error_message, ex.status_code


def send_sms(number, message):
    """Forward the message via SMS."""
    if not TWILIO_ACCOUNT_SID:
        return "Missing TWILIO_ACCOUNT_SID environment variable.", 400
    if not TWILIO_AUTH_TOKEN:
        return "Missing TWILIO_AUTH_TOKEN environment variable.", 400
    return "Not yet implemented", 200
