# -*- coding: utf-8 -*-
"""bttn webhook handler."""
import json
import hipchat
import flask

app = flask.Flask(__name__)


@app.route('/bttn', methods=['POST'])
def bttn_pressed():
    print flask.request
    post = flask.request.json
    sender = post['user']
    return hipchat.send_room_message('Laboratory (testing)', "%s pressed the Big Red" % sender)
