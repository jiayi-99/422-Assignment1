from flask import Flask, jsonify, render_template, request
from map_service import get_map_data
from pprint import pprint

# initialize flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/map")
def map():
    return render_template('map.html')

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)