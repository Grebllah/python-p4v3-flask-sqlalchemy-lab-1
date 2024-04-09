# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def min_magnitude(magnitude):
    earthquakes = []  # array to store a dictionary for each eathquake
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquakes.append(earthquake.to_dict())
    body = {'count': len(earthquakes),
            'quakes': earthquakes
            }
    return make_response(body, 200)
# Task #4: Add view to get earthquakes matching a minimum magnitude value
# Edit app.py to add a view that takes one parameter, a float that represents an magnitude. The route should have the form /earthquakes/magnitude/<float:magnitude>.
# The view should query the database to get all earthquakes having a magnitude greater than or equal to the parameter value, and return a JSON response containing the count of matching rows along with a list containing the data for each row.
# For example, the URL http://127.0.0.1:5555/earthquakes/magnitude/9.0
# Links to an external site. should result in a response with a 200 status and a body containing JSON formatted text as shown:

if __name__ == '__main__':
    app.run(port=5555, debug=True)
