from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get("/restaurants")
def get_restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurants.append(restaurant.to_dict(only=("address", "id", "name")))

    return make_response(jsonify(restaurants), 200)

@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant:
        return make_response(jsonify(restaurant.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Restaurant not found"}), 404)

@app.get("/pizzas")
def get_pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizzas.append(pizza.to_dict(only=("id", "ingredients", "name")))
    
    return make_response(jsonify(pizzas), 200)

@app.post("/restaurant_pizzas")
def create_restaurant_pizza():
    data = request.get_json()
    try:
        price = data.get('price')
        restaurant_id = data.get('restaurant_id')
        pizza_id = data.get('pizza_id')

        restaurant_pizza = RestaurantPizza(
            price=price,
            restaurant_id=restaurant_id,
            pizza_id=pizza_id
        )

        db.session.add(restaurant_pizza)
        db.session.commit()

        return make_response(jsonify(restaurant_pizza.to_dict()), 201)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 400)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)
