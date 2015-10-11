import json
from flask import Flask
import googlemaps

app = Flask(__name__)
with open("key.txt") as input_key:
    key = next(input_key).strip("\n")

def remove_tags(text):
    output = text.replace("<b>", "")
    output = output.replace("</b>", "")
    output = output.replace("<div>", "")
    output = output.replace("</div>", "")
    return output

@app.route('/directions/<origin>/<destination>')
def directions(origin, destination):
    gmaps = googlemaps.Client(key=key)
    directions_result = gmaps.directions(origin, destination)
    output = dict() # output is a dictionary, keyed by routes, of lists of dictionaries of steps and total data
    i = 1
    for dr in directions_result: # for directions for each possible route
        sub_output = []
        leg = dr['legs'][0] # assumes that user does not input waypoints or additional endpoints
        for step in leg['steps']:
            s = dict()
            s['direction'] = remove_tags(step['html_instructions'])
            s['distance'] = step['distance']['text']
            s['duration'] = step['duration']['text']
            sub_output.append(s)
        totals = dict()
        totals['total distance'] = leg['distance']['text'] # output at end of each route
        totals['total time'] = leg['duration']['text']
        sub_output.append(totals)
        output['Route {0}:'.format(i)] = sub_output
        i += 1
    #convert into list of dictionaries where each category is key
    #jsond = json.dumps(output)
    route = output["Route 1:"]
    build_string = ""
    for line in route:
        if "total time" in line.keys():
            build_string += line["total time"] + " " + line["total distance"]
            break
        print(line)
        build_string+= line["direction"]
        build_string+= " ("
        build_string+= line["duration"] + ", "
        build_string+= line["distance"] + ")\n"
    return build_string

if __name__ == "__main__":
    app.run(debug=True)
