from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture)
    return jsonify(message="Picture not found"), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()
    id_to_check = picture_data['id']
    for picture in data:
        if picture['id'] == id_to_check:
            return jsonify({"Message": f"picture with id {id_to_check} already present"}), 302

    data.append(picture_data)
    return jsonify(picture_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    picture_data = request.get_json()

    # Search for the picture by ID
    picture_to_update = None
    for picture in data:
        if picture['id'] == id:
            picture_to_update = picture
            break

    # If the picture exists, update it; otherwise, return a 404 response
    if picture_to_update:
        # Update the picture with the incoming request data
        picture_to_update.update(picture_data)
        return jsonify(picture_to_update), 200
    else:
        abort(404, {"message": "picture not found"})

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Search for the picture by ID
    picture_to_delete = None
    for picture in data:
        if picture['id'] == id:
            picture_to_delete = picture
            break

    # If the picture exists, delete it; otherwise, return a 404 response
    if picture_to_delete:
        data.remove(picture_to_delete)
        return '', 204
    else:
        abort(404, {"message": "picture not found"})