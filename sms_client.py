from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)


@app.route("/twilio", methods=['GET', 'POST'])
def recieve_sms():
    """
    Recieves SMS text messages from Twilio, and inserts them into the MySQL
    database for Celery to pick up and execute on. Logs a warning if there is
    none of From, MessageSid, or Body in the request's parameters.
    """

    from_number = param('From')
    unique_id = param('MessageSid')
    body = param('Body')
    if from_number and unique_id and body:
        # insert into DB for Celery to pick up
        pass
    else:
        # error?
        resp = twilio.twiml.Response()
        resp.message("Hello, Mobile Monkey")
        return str(resp)


def param(name):
    return request.values.get(name, None)

if __name__ == "__main__":
    app.run(debug=True)
