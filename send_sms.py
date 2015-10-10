# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXX"
auth_token = "YYYYYYYYYYYYYYYYYY"
FROM_NUMBER = "+15555555555"
client = TwilioRestClient(account_sid, auth_token)

def send_message(to_num, body):
    """
    Sends a message to TO_NUM with a message body of BODY
    """
    message = client.messages.create(to=to_num, from_=FROM_NUMBER, body=body)

def print_message(to_num, body):
    print("%s: %s\n\n" % (to_num, body), out=open("out.txt", 'w'))
