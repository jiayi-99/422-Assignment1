from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
# from map_service import get_map_data
from pprint import pprint
import urllib
import urllib.request
import json
from main import get_data_dict
# initialize flask app
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/map")
def map():
    return render_template('map.html')


@app.route('/get_data_dict', methods=["POST"])
def get_data_dict():   
    data_dict = {}
    source_lat = request.form.get('source_lat')
    source_lon = request.form.get('source_lon')
    destination_lat = request.form.get('destination_lat')
    destination_lon = request.form.get('destination_lon')
   
    json_response = access_api(source_lat, source_lon, destination_lat, destination_lon)
    data_dict["error_message"] = ''
    data_dict["instructions"] = []

    # return "Hello, cross-origin-world!"
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
    return jsonify(data_dict=data_dict,
                           error_message=data_dict["error_message"],
                           directions=data_dict["instructions"],
                           source_cor=[source_lat, source_lon],
                           destination_cor=[destination_lat, destination_lon]
                           )

@app.route("/map_data", methods=['POST'])
def map_data():
    
    print('Inside map_data fn')
    # take the input from the form in web page
    source_lat = request.form.get('source_lat')
    source_lon = request.form.get('source_lon')
    destination_lat = request.form.get('destination_lat')
    destination_lon = request.form.get('destination_lon')
    
    # get the geo-json from openrouteservice for given co-ordinates
    geo_json = get_map_data(
        source_cor=[source_lat, source_lon],
        destination_cor=[destination_lat, destination_lon]
    )
    print('GEO json: ')
    pprint(geo_json)
     
    return jsonify(geo_json)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
