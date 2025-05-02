"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_members():
    members = jackson_family.get_all_members()
    response_body = {"family": members}
    return jsonify(response_body), 200

@app.route('/members/<int:id>',methods=['GET'])
def handle_get_specific_member(id):
    member = jackson_family.get_member(id)
    if(member):
        response_body = member
        return jsonify(response_body), 200
    else:
        response_body = {"error":"Family member not found."}
        return jsonify(response_body), 404

@app.route('/members', methods=['POST'])
def handle_post_member():
    new_member = request.json
    added = jackson_family.add_member(new_member)
    if added:
        return handle_get_members()
    else:
        response_body = {"error":"There was an error adding the member."}
        return jsonify(response_body), 400

@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    deleted = jackson_family.delete_member(id)
    if deleted:
        return handle_get_members()
    else:
        response_body = {"error":"Couldn't find a family member with that ID."}
        return jsonify(response_body), 400


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
