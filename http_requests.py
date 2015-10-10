from parsing import interpret_request
import requests

service_to_gram = {'google':['{str:"maps"},{str:},{str:}']}
gram_to_endpoint = {'{str:"maps"},{str:},{str:}':'http://127.0.0.1:5000/directions/{1}/{2}'}


def process_request(id_num, phone, body):
    service = body.split(',')[0]
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
            return http_request(endpoint, params)


def http_request(url, body):
    print("Connecting to url %s" % url)
    payload = {'body': body}
    return requests.get(url, data=payload).text

if __name__ == "__main__":
    print(process_request("TESTING123", "310-362-347",
                          "google, maps, Manhattan Beach, Berkeley"))
