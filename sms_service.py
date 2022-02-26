from twilio.rest import Client
import keys
from datetime import timezone
from flask import Flask

app = Flask(__name__)
# Pulls API information from Keys file

@app.route('/')
def start_up():
  return "Waiting for message to sms....."

# request to send sms with given message and phone number
@app.route('/send', methods=['POST'])
def send_sms(message_body,phone_number):
  account_sid = keys.account_sid
  auth_key = keys.auth_token

  client = Client(account_sid, auth_key)

  # Check if phone number includes county code (will only work in US)
  if phone_number < 10:
    return "Invalid phone number format. Please send 10 digit phone number with area code"
  if len(phone_number) == 10 and phone_number[:1] != '+1':
    phone_number = "+1" + phone_number

  message = client.messages.create(
    body = message_body,
    from_ = '+14698333968',  
    to= phone_number
  )

  return message.sid

# send a status request for sms with message sid
@app.route('/status', methods=['GET'])
def get_status(message_sid):
  account_sid = keys.account_sid
  auth_key = keys.auth_token

  client = Client(account_sid, auth_key)

  status = client.messages(message_sid).fetch()

  UTC_datetime = status.date_sent

  def utc_to_local(utc_dt):
      return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
  
  local_time_sent = utc_to_local(UTC_datetime).strftime("%c")

  return [status.sid, local_time_sent]


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=125)