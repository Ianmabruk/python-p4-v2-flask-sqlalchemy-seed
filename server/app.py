# server/app.py

import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# --------------------------
# Routes
# --------------------------
@app.route("/")
def index():
    return "<h1>Zoo API</h1>"

# GET all animals
@app.route("/animals", methods=["GET"])
def get_animals():
    animals = Animal.query.all()
    return jsonify([a.to_dict() for a in animals])

# POST create animal
@app.route("/animals", methods=["POST"])
def create_animal():
    data = request.get_json() or {}
    name = data.get("name")
    species = data.get("species")
    zookeeper_id = data.get("zookeeper_id")
    enclosure_id = data.get("enclosure_id")

    if not all([name, species, zookeeper_id, enclosure_id]):
        return jsonify({"errors": ["Missing required fields"]}), 400

    animal = Animal(
        name=name,
        species=species,
        zookeeper_id=zookeeper_id,
        enclosure_id=enclosure_id
    )
    db.session.add(animal)
    db.session.commit()
    return jsonify(animal.to_dict()), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
