import parsing
import http.client, urllib.parse

service_to_gram = {}
gram_to_endpoint = {}		

# cannot have more than 10 params!
def process_request(id_num, phone, body):
	service = body.split(',')[0]
	if service not in list(service_to_gram.keys()):
		return "ERROR - no such service"
	grammars = service_to_gram[service]
	for g in grammars:
		params = interpret_request(body)
		if type(params) != str:
			endpoint = gram_to_endpoint[g]
			i = 0
			while i < len(endpoint):
				if endpoint[i] == '{':
					endpoint = endpoint[:i] + params[int(endpoint[i+1])] + endpoint[i+3:]
				i += 1
			http_request(endpoint, params)

def http_request(url, body):
	params = urllib.parse.urlencode({'@body': body})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = http.client.HTTPConnection(url)
	conn.request("GET", "", params, headers)
	return conn.getresponse()
