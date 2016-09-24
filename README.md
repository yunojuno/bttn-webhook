# bttn-webhook

Hackable Flask app that can be used as a webhook for bt.tn events

## What is bt.tn

Describing itself as "The simplest user interface in the world", [bt.tn](https://bt.tn/) is literally a button. A big, red, button. That you can press.

What happens when you press the button is largely up to you. The bt.tn itself
will send a press event to bt.tn HQ, and from there an IFTTT-style set of actions can be configured. You can send an email, or SMS, poke an IFTTT recipe.

## What is this project

If you are a developer, the most useful thing that can happen is that it calls an HTTP endpoint with a payload including the following details:

```
<DATE> Expands to date when bttn was pressed<br>
<TIME> Expands to time of day when bttn was pressed<br>
<NAME> Expands to bttn's name<br>
<USER> Expands to user's name<br>
<LOCATION> Expands to bttn's location<br>
<EMAILADDRESS> Expands to bttn's email address<br>
<LANGUAGE> Expands to bttn's language<br>
<ID> Expands to bttn's short ID<br>
<DEVICEID> Expands to bttn's device ID<br>
<URL> Expands to bttn's URL<br>
<EID> Expands to a unique numeric button press event identifier<br>
<ETYPE> Expands to bttn press event type<br>
<COUNTER> Expands to number of times the bttn has been pressed<br>
<CALLBACKURL> Expands to http callback URL<br>
```

This project provides a simple template / starter for creating and deploying
a webhook handler. The sample integration is with HipChat. It requires that
you set up the button action to POST to the endpoint (the Heroku app URL) with
the following data as form encoded variables:

```
"channel" - must be "hipchat" for the default sample
"recipient" - the room name / id for HipChat, channel for Slack, phone number for Twilio
"message" - the message to send, which can include the expansion tags above
```

You will need to set up a Heroku environment setting - `HIPCHAT_API_TOKEN`.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
