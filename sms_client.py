from flask import Flask, request
from redis import Redis
from rq import Queue
from consts import RQ_HOST, RQ_PORT


from connector import DatabaseConnector
from http_requests import process_request

app = Flask(__name__)
#db = DatabaseConnector()
queue = Queue(connection=Redis(RQ_HOST, RQ_PORT))


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
        # Add to RQ in addition
        #db.add_received_sms(from_num=from_number, body=body, id=unique_id)
        queue.enqueue(process_request, unique_id, from_number, body)
        return "Queued"
    else:
        # error?
        raise Exception("One of from, unique_id, and body is null!")


def param(name):
    return request.values.get(name, None)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
