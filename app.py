"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/api/cupcakes")
def list_all_cupcake():
    """Return JSON {cupcakes: [{id, flavor, size, rating, image}...]} """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def show_single_cupcake_detail(cupcake_id):
    """ Return JSON with detail about a single cupcake
        example: {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """ Creates cupcake and returns the JSON of new cupcake 
        example: {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json.get("flavor")
    size = request.json.get("size")
    rating = request.json.get("rating")
    image = request.json.get("image")

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake_details(cupcake_id):
    """ Takes JSON like {cupcake: {flavor: Test}} 
        and returns a JSON {cupcake: {flavor: Vanilla Test}} 
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # breakpoint()
    flavor = request.json["cupcake"].get("flavor")
    size = request.json["cupcake"].get("size")
    rating = request.json["cupcake"].get("rating")
    image = request.json["cupcake"].get("image")

    cupcake.flavor = flavor if flavor else cupcake.flavor
    cupcake.size = size if size else cupcake.size
    cupcake.rating = rating if rating else cupcake.rating
    cupcake.image = image if image else cupcake.image

    db.session.commit()
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """ Takes JSON like object and returns JSON 
        Example: {"deleted": [cupcake_id]} 
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    # return jsonify(f'{"deleted": [cupcake_id]}')

    return jsonify(deleted=cupcake_id)

# @app.get("/")
# def
