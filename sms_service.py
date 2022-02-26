from twilio.rest import Client
import keys
from datetime import timezone
from flask import Flask

app = Flask(__name__)
# Pulls API information from Keys file

@app.route('/')
def start_up():
  return 'Waiting for message to sms.....'

# request to send sms with given message and phone number.
# Receives message body and phone number through URL.
# example: localhost:125/Hello, this is a message from SeeSplit./##########
@app.route('/send/<string:message_body>/<string:phone_number>')
def send_sms(message_body,phone_number):
  account_sid = keys.account_sid
  auth_key = keys.auth_token

  client = Client(account_sid, auth_key)

  # Check if phone number includes county code (will only work in US)
  if len(phone_number) < 10:
    return 'Invalid phone number format. Please send a 10 digit phone number that includes the area code with no delimeters'
  # if only 10 digit format, add in internation code
  if len(phone_number) == 10 and phone_number[:1] != '+1':
    phone_number = '+1' + phone_number

  message = client.messages.create(
    body = message_body,
    from_ = '+14698333968',  
    to= phone_number
  )

  # twilio message id for status requests
  id = message.sid

  return 'Success. Here is your message ID: ' + id

# Request status for a message previously sent with message ID
# through URL body
# example: localhost:125/
@app.route('/status/<string:message_sid>')
def get_status(message_sid):
  account_sid = keys.account_sid
  auth_key = keys.auth_token

  client = Client(account_sid, auth_key)

  status = client.messages(message_sid).fetch()

  UTC_datetime = status.date_sent

  #function to convert UTC to local timezone
  def utc_to_local(utc_dt):
      return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
  
  local_time_sent = utc_to_local(UTC_datetime).strftime('%c')

  #return status and time sent from Twilio
  return_message = status.status + ": " + local_time_sent

  return return_message

if __name__ == '__main__':
  # app.debug = True
  app.run(host='0.0.0.0', port=125)