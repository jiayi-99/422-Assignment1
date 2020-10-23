from flask import Flask, request, render_template
import urllib
import urllib.request
import json

app = Flask(__name__)


@app.route('/', methods=["POST"])
def get_data_dict():
    data_dict = {}
    source_lat, source_long = get_source_coords()
    destination_lat, destination_long = get_destination_coords()

    json_response = access_api(source_lat, source_long, destination_lat, destination_long)
    data_dict["error_message"] = ''
    data_dict["instructions"] = []

    if json_response:
        json_as_dict = json.loads(json_response)
        data_dict["json_info"] = json_as_dict
        route_segments = json_as_dict["routes"][0]["segments"][0]["steps"]
        for segment in route_segments:
            if "instruction" in segment:
                data_dict["instructions"].append(segment["instruction"])
            if "distance" in segment:
                data_dict["distances"].append(segment["distance"])
    else:
        data_dict["error_message"] = 'Invalid coordinates. Please try again.'
    return render_template('map.html', data_dict=data_dict,
                           error_message=data_dict["error_message"],
                           directions=data_dict["instructions"],
                           source_cor=[source_lat, source_long],
                           destination_cor=[destination_lat, destination_long],
                           distances=data_dict["distances"]
                           )


@app.route('/', methods=["GET"])
def initial_load():
    return render_template('map.html')


@app.route("/map")
def map():
    return render_template('map.html')


# helper methods
def get_source_coords():
    source_lat = request.form['source_lat']
    source_long = request.form['source_long']
    return source_lat, source_long


def get_destination_coords():
    destination_lat = request.form['destination_lat']
    destination_long = request.form['destination_long']
    return destination_lat, destination_long


def access_api(source_lat, source_long, destination_lat, destination_long):
    req = urllib.request.Request('https://api.openrouteservice.org/v2/directions/driving-car')
    req.add_header('Authorization', '5b3ce3597851110001cf624875b0189d61b04abeaa6e33d3b58aabc6')
    req.add_header('Content-Type', 'application/json')

    values = {"coordinates": [[source_long, source_lat], [destination_long, destination_lat]]}

    try:
        response = urllib.request.urlopen(req, json.dumps(values).encode('utf-8'))
        json_response = response.read()
        return_str = json_response.decode('utf-8')
    except:
        return_str = None
    return return_str

if __name__ == '__main__':
    app.run()
