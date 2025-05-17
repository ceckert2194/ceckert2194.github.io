from flask import Flask, render_template, request, jsonify
from main import YEAR, TOLERANCE, find_street_alignments_in_bbox

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alignments', methods=['POST'])
def alignments():
    data = request.json
    min_lat = data['min_lat']
    min_lon = data['min_lon']
    max_lat = data['max_lat']
    max_lon = data['max_lon']
    year = data.get('year', YEAR)
    tolerance = data.get('tolerance', TOLERANCE)
    print(f"Received bbox: {min_lat}, {min_lon}, {max_lat}, {max_lon}")
    print(f"Year: {year}, Tolerance: {tolerance}")
    results = find_street_alignments_in_bbox(min_lat, min_lon, max_lat, max_lon, year, tolerance)
    print(f"Found {len(results)} alignments")
    if results:
        print(f"Sample alignment: {results[0]}")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)