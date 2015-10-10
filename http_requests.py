import requests

from parsing import interpret_request, validate_grammar
from connector import DatabaseConnector
from send_sms import send_message

from rq import Queue, Connection
from redis import Redis
from consts import RQ_HOST, RQ_PORT

service_to_gram = {'google':['{str:"maps"},{str:},{str:}']}
gram_to_endpoint = {'{str:"maps"},{str:},{str:}':'http://127.0.0.1:5000/directions/{1}/{2}'}
#service_to_gram = {}
#gram_to_endpoint = {}


with Connection(Redis(RQ_HOST, RQ_PORT)):
    queue = Queue()

def process_request(id_num, phone, body):
    service = body.split(' ')[0]
    if service not in list(service_to_gram.keys()):
        return "ERROR - no such service"
    grammars = service_to_gram[service]
    for g in grammars:
        params = interpret_request(body, g)
        if type(params) != str:
            print(params)
            endpoint = gram_to_endpoint[g]
            i = 0
            while i < len(endpoint):
                if endpoint[i] == '{':
                    endpoint = endpoint[:i] + params[int(endpoint[i+1])] + endpoint[i+3:]
                i += 1
            queue.enqueue(send_message, phone, http_request(endpoint, params))
            # return http_request(endpoint, params)


def http_request(url, body):
    print("Connecting to url %s" % url)
    payload = {'body': body}
    return requests.get(url, data=payload).text

#conn = DatabaseConnector()

def load_grammars():
    db = conn.query_endpoints()
    for row in db:
        if row.service not in list(service_to_gram.keys()):
            service_to_gram[row.service] = [row.grammar]
            gram_to_endpoint[row.grammar] = row.endpoint
        else:
            service_to_gram[row.service].append(row.grammar)
            gram_to_endpoint[row.grammar] = row.endpoint

def add_or_update_grammar(service, grammar, endpoint):
    # remove all spaces not in strings
    string = False
    i = 0
    while i < len(grammar):
        if grammar[i] == '"':
            string = not string
        if grammar[i] == ' ' and not string:
            grammar = grammar[:i] + grammar[i+1:]
        i+=1

    if validate_grammar(grammar):
        conn.add_endpoint(service=service, grammar=grammar, endpoint=endpoint)
        load_grammars()


if __name__ == "__main__":
    print(process_request("TESTING123", "310-362-347",
                          "google maps Manhattan Beach, Berkeley"))
