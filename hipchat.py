# -*- coding: utf-8 -*-
"""Wrapper around the HipChat v2 API.

This module contains a couple of generic functions for sending messages
to rooms and users within HipChat.

>>> hipchat.send_room_message('Lounge', 'This is a message')
>>> hipchat.send_user_message('hugo', 'Hello, Hugo')

Requires HIPCHAT_API_TOKEN to be set.

"""
import json
import os

import requests

API_V2_ROOT = 'https://api.hipchat.com/v2/'
VALID_COLORS = ('yellow', 'green', 'red', 'purple', 'gray', 'random')
VALID_FORMATS = ('text', 'html')


class HipChatError(Exception):

    """Custom error raised when communicating with HipChat API."""

    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

    def __unicode__(self):
        message = json.loads(self.error_message).get('error', {}).get('message')
        return u'Status code %s: %s' % (self.status_code, message)

    def __str__(self):
        return unicode(self).decode('utf-8')


def get_auth_headers(auth_token=None):
    """Return authentication headers for API requests.

    Kwargs:
        auth_token: if passed in this is used as the API token. If
            this is None, look in the os.environ for a value for
            'HIPCHAT_API_TOKEN'.

    Returns a dict that can be passed into requests.post as the
        'headers' dict.

    """
    token = auth_token or os.getenv('HIPCHAT_API_TOKEN')
    assert token is not None, (u"No valid HipChat authentication token found.")
    return {
        'Authorization': 'Bearer %s' % token,
        'Host': 'api.hipchat.com',
        'Content-Type': 'application/json'
    }


def _call_api(url, message, auth_token=None, color='yellow', sender=None,
              notify=False, message_format='html'):
    """Send message to user or room via API.

    Args:
        url: API endpoint
        message: string, The message body, 1-10000 chars.

    Kwargs:
        auth_token: string, the API auth token to use, defaults to the os.environ
            value for 'HIPCHAT_API_TOKEN'.
        color: string, message background, defaults to 'yellow', can be
            any value in VALID_COLORS
        sender: string, the name that appears as the sender of the message.
            defaults to the name of the owner of the auth token.
        notify: bool, defaults to False, if True then 'ping' recipients.
        message_format: string, one of VALID_FORMATS - the format of the
            message. If 'html' it can contains links etc., but if 'text' it can
                be used for fixed-width-appropriate messages - e.g. code / quotes.

    Raises HipChatError if for any reason the request fails.

    """
    assert message is not None, u"Missing message param"
    assert len(message) >= 1, u"Message too short, must be 1-10,000 chars."
    assert len(message) <= 10000, u"Message too long, must be 1-10,000 chars."
    assert color in VALID_COLORS, u"Invalid color value: %s" % color
    assert message_format in VALID_FORMATS, u"Invalid format: %s" % message_format

    headers = get_auth_headers(auth_token=auth_token)
    data = {
        'message': message,
        'color': color,
        'notify': notify,
        'message_format': message_format
    }
    if sender is not None:
        data['from'] = sender

    resp = requests.post(url, data=json.dumps(data), headers=headers)
    if str(resp.status_code)[:1] != '2':
        raise HipChatError(resp.status_code, resp.text)
    else:
        return resp


def send_room_message(room_id_or_name, message, auth_token=None, color='yellow',
                      sender=None, notify=False, message_format='html'):
    """Send a message to room."""
    assert room_id_or_name not in (None, ''), u"Missing room_id_or_name"
    url = "%sroom/%s/notification" % (API_V2_ROOT, room_id_or_name)
    return _call_api(
        url,
        message,
        auth_token=auth_token,
        color=color,
        sender=sender,
        notify=notify,
        message_format=message_format
    )


def send_user_message(user_id_or_email, message, auth_token=None,
                      notify=False, message_format='html'):
    """Send a message to room."""
    assert user_id_or_email not in (None, ''), u"Missing user_id_or_email"
    url = "%suser/%s/message" % (API_V2_ROOT, user_id_or_email)
    return _call_api(
        url,
        message,
        auth_token=auth_token,
        notify=notify,
        message_format=message_format
    )
