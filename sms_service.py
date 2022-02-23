from twilio.rest import Client
import keys

client = Client(keys.account_sid, keys.auth_token)

message = client.messages.create(
  body = 'test message from python',
  from_ = '+14698333968',
  to='+14698787992'
)

print('success')