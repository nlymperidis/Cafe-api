import os
import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

API_KEY = os.environ.get("API_KEY")
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE")
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=to_dict(random_cafe))


@app.route("/all")
def get_all_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[to_dict(cafe) for cafe in all_cafes])


@app.route("/search")
def get_cafe_at_location():
    # Get the 'loc' parameter from the request
    loc = request.args.get('loc')
    if loc:
        result = db.session.execute(db.select(Cafe).where(Cafe.location == loc))
        cafes = result.scalars().all()
        if cafes:
            return jsonify(cafes=[to_dict(cafe) for cafe in cafes])
        else:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})
    else:
        return jsonify({'message': 'Please provide a "loc" parameter in your request'})


# HTTP POST - Create Record
@app.route("/add", methods=["GET","POST"])
def post_new_cafe():
    api_key = request.args.get('api-key')

    if api_key == API_KEY:
        name = request.form.get("name")

        # Check if a cafe with the same name already exists in the database
        existing_cafe = Cafe.query.filter_by(name=name).first()

        if not existing_cafe:
            new_cafe = Cafe(
                name=request.form.get("name"),
                map_url=request.form.get("map_url"),
                img_url=request.form.get("img_url"),
                location=request.form.get("loc"),
                has_sockets=bool(request.form.get("sockets")),
                has_toilet=bool(request.form.get("toilet")),
                has_wifi=bool(request.form.get("wifi")),
                can_take_calls=bool(request.form.get("calls")),
                seats=request.form.get("seats"),
                coffee_price=request.form.get("coffee_price"),
            )
            db.session.add(new_cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully added the new cafe."})
        else:
            return jsonify(error={"Duplicate": "Sorry a cafe with that name was found in the database."})
    else:
        return jsonify(error=
                       {"Unauthorized": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])  # We need the GET to get the cafe_id
def patch_new_price(cafe_id):
    cafe = db.session.get(Cafe, cafe_id)
    new_price = request.args.get('new_price')
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["GET", "DELETE"])
def delete_coffee(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the Cafe."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(
            error={"Unauthorized": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
