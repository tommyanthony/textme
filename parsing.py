import re 

def interpret_request(request_string, grammar):
	# remove all spaces not in strings
	string = False
	i = 0
	while i < len(request_string):
		if request_string[i] == '"':
			string = not string
		if request_string[i] == ' ' and not string:
			request_string = request_string[:i] + request_string[i+1:]
		i+=1

	items = request_string.split(',')
	if len(items) == 0:
		return "ERROR - no parameters"
	service = items[0]
	#if service not in list(grammars.keys()):
	#	return "ERROR - no such service"
	#grammar = grammars[service]
	grammar = grammar.split(',')
	output_params = []

	num_req = 0
	for g in grammar:
		if g[0] == '{':
			num_req+=1

	counter = 0

	for i in range(1, len(items)):		# Loop over all items in grammar
		counter+=1
		if i-1 == len(grammar):
			return "ERROR"
		cur_grammar = grammar[i-1]
		input_type = cur_grammar[1:4]

		str_case = False
		float_case = False

		if input_type == "int":
			item = int(items[i])
		elif input_type == "flt":
			item = float(items[i])
			float_case = True
		elif input_type == "str":
			item = items[i]
			str_case = True
		else:
			return "ERROR - invalid type"

		if cur_grammar[5] == '}' or cur_grammar[5] == ']':
			output_params.append(item)
			continue

		remaining_grammar = cur_grammar[5:-1]
		remaining_grammar = remaining_grammar.split(';')

		added = False
		for cur in remaining_grammar:
			if str_case:
				regex = re.compile(cur[1:-1])
				if regex.match(item):
					added = True
					output_params.append(item)
					break
			elif float_case:
				if item == float(cur):
					output_params.append(item)
					added = True
					break
			elif not str_case and not float_case:
				if item == int(cur):
					output_params.append(item)
					added = True
					break

		if not added:
			return "ERROR - did not match syntax"

	if counter < num_req:
		return "ERROR - to few parameters"
	return output_params

def validate_grammar(grammar):
	# check all [] after all {} and matching braces
	brackets = False
	braces = False

	string = False

	bracket_started = False
	for i in range(len(grammar)):
		if grammar[i] == '"':
			string = not string
		if grammar[i] == '[' and not string:
			if brackets or braces:
				return False
			if grammar[i+1:i+5] != "str:" and grammar[i+1:i+5] != "int:" and grammar[i+1:i+5] != "flt:":
				return False
			brackets = True
			bracket_started = True
		elif grammar[i] == '{' and not string:
			if bracket_started or brackets or braces:
				return False
			if grammar[i+1:i+5] != "str:" and grammar[i+1:i+5] != "int:" and grammar[i+1:i+5] != "flt:":
				return False
			braces = True
		elif grammar[i] == ']' and not string:
			if not brackets or braces:
				return False
			brackets = False
		elif grammar[i] == '}' and not string:
			if not braces or brackets:
				return False
			braces = False

	# does not check that list of possible options is valid
	return True


def add_or_update_grammar(service, grammar):
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
		grammars[service] = grammar
