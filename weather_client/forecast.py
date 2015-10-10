from flask import Flask
import googlemaps, urllib, json, datetime, configparser

app = Flask(__name__)

# retrieve the day of the week as a string from a given unix time stamp
def get_day(unix_time, i):
    if i == 0:
        return 'Today'
    if i == 1:
        return 'Tomorrow'
    return datetime.date.fromtimestamp(unix_time).strftime('%a')

def to_string(output):
    s = ""
    for day in output:
        s += day['day'] + ': ' + '\n'
        s += day['summary'] + '\n'
        s += "High: " + str(day['max temp']) + '\n'
        s += "Low: " + str(day['min temp']) + '\n'
        s += '\n'
    return s


@app.route('/forecast/<location>')
def directions(location):

    config = configparser.RawConfigParser()
    config.read('weather.cfg')

    weather_APIKEY = config.get('API Keys', 'weather_api')
    google_APIKEY = config.get('API Keys', 'google_api')


    # get latitude and longitude from given location
    gmaps = googlemaps.Client(key=google_APIKEY)
    geocode_result = gmaps.geocode(location)[0]['geometry']['location']
    lat = geocode_result['lat']
    lon = geocode_result['lng']

    # retrieve 10 day forecast from weather data
    httpro = urllib.request.urlopen('https://api.forecast.io/forecast/{0}/{1},{2}'.format(weather_APIKEY, lat, lon))
    forecast = json.loads(httpro.read().decode("utf-8"))
    forecast = forecast['daily']['data']
    output = []
    
    # only retrieve the name of the day, summary, max temp, and min temp
    i = 0
    for day in forecast:
        d = dict()
        d['day'] = get_day(day['time'], i)
        d['summary'] = day['summary']
        d['max temp'] = day['temperatureMax']
        d['min temp'] = day['temperatureMin']
        output.append(d)
        i += 1

    #format of output is a list of dictionaries where each list entry is the forecast for that day
    return to_string(output)

if __name__ == "__main__":
    app.run(debug = True)