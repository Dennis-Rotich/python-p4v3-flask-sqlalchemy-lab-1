# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    response_body = {
        'id': earthquake.id,
        'magnitude':earthquake.magnitude,
        'location': earthquake.location,
        'year':earthquake.year
    }
    status_code = 200
    headers = {}
    return make_response(jsonify(response_body), status_code, headers)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def search_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if not earthquakes:
        return jsonify({'count':0, 'quakes': []}), 200
    quakes = []
    count = 0
    for earthquake in earthquakes:
        count += 1
        quakes.append({
            'id': earthquake.id,
            'magnitude':earthquake.magnitude,
            'location':earthquake.location,
            'year':earthquake.year
        })
    response_body = {'count': count, 'quakes': quakes}
    status_code = 200
    headers = {}
    return make_response(response_body, status_code, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
