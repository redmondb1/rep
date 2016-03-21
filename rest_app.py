#!flask/bin/python

""" This flask app provides the RESTful interface to a RepStore.
"""

from flask import (
    abort,
    Flask,
    jsonify,
    make_response,
    redirect,
    request,
)
from rep import Rep
from rep import RepStore

app = Flask(__name__)

store = RepStore()

@app.route('/')
def index():
    """ This is a placeholder for the root.
    """
    return "Hello, World!"

@app.route('/rep/api/v1.0/reps', methods=['GET'])
def get_reps():
    """ This outputs all the Reps as a single dict.  This will eventually need
    to be limited in some way.
    """
    return jsonify(store.as_dict())

@app.route('/rep/api/v1.0/reps/<int:key>', methods=['GET'])
def get_rep(key):
    """ Return a specific Rep referenced by its local key.
    """
    try:
        return jsonify(store[key].as_dict())
    except KeyError:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    """ Defines a custom 404 page.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/rep/api/v1.0/reps', methods=['POST'])
def create_rep():
    if not request.json:
        abort(400)
    key = store.create(Rep(title=request.json['title']))
    return redirect('/rep/api/v1.0/reps/%s' % key, code=201)

@app.route('/rep/api/v1.0/reps/<int:key>', methods=['PUT'])
def update_rep(key):
    store.update({key: Rep(title=request.json.get('title'))})
    return jsonify(store[key].as_dict())

@app.route('/rep/api/v1.0/reps/<int:key>', methods=['DELETE'])
def delete_rep(key):
    try:
        del store[key]
        return jsonify({'result': True})
    except KeyError as e:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

