import re 

grammars = {}

def interpret_request(request_string):
	request_string = request_string.replace(', ', ',')
	items = request_string.split(',')
	if len(items) == 0:
		return "ERROR - no parameters"
	service = request_string[0]
	grammar = grammars[service]
	grammar = grammar.split(',')
	output_params = []

	num_req = 0
	for g in grammar:
		if g[0] == '{':
			num_req++
			
	counter = 0

	for i in range(1, len(items)):		# Loop over all items in grammar
		counter++
		if i-1 == len(grammar):
			return "ERROR"
		cur_grammar = grammar[i-1]
		input_type = cur_grammar[1:4]

		str_case = False
		float_case = False

		if input_type == "int":
			item = int(items[i])
		else if input_type == "flt":
			item = float(items[i])
			float_case = True
		else if input_type == "str":
			item = items[i]
			str_case = True
		else:
			return "ERROR - invalid type"

		if cur_grammar[5] == '}' || cur_grammar[5] == ']':
			output_params.append(item)
			continue

		remaining_grammar = cur_grammar[5:-1]
		remaining_grammar = remaining_grammar.split(';')

		added = False
		for cur in remaining_grammar:
			if str_case:
				regex = re.compile(cur[1:-1])
				if re.match(item):
					added = True
					output_params.append(item)
					break
				param = ""
			else if float_case:
				if item == float(cur):
					output_params.append(item)
					added = True
					break
			else:
				if item == int(cur):
					output_params.append(item)
					added = True
					break

		if not added:
			return "ERROR - did not match syntax"

	if counter < num_req:
		return "ERROR - to few parameters"
	return output_params