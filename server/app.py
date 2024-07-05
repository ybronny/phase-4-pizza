#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


@app.get("/restaurants")
def get_restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurants.append(restaurant.to_dict(only=("address", "id", "name",)))

    body = restaurants

    return make_response(body, 200)

@app.get("/restaurants/<int:id>")
def get_restaurant(id):
    restaurant = Restaurant.query.filter_by(id = id).first()

    if restaurant:
        body = restaurant.to_dict()
        status = 200
    else:
        body = {"error": "Restaurant not found"}
        status = 404
    
    return make_response(body, status)

@app.delete("/restaurants/<int:id>")
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id = id).first()

    if restaurant:
        body = {}
        status = 204
        db.session.delete(restaurant)
        db.session.commit() 
    else:
        body = {"error": "Restaurant not found"}
        status = 404
    
    return make_response(body, status)

@app.get("/pizzas")
def get_pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizzas.append(pizza.to_dict(only=("id", "ingredients", "name", )))
    
    body = pizzas

    return make_response(body, 200)



@app.post("/restaurant_pizzas")
def create():
    data = request.get_json()
    
    if "price" not in data or "pizza_id" not in data or "restaurant_id" not in data:
        body = {"error": "Missing required fields"}
        status = 400
    else:
        try:
            restaurant_pizza = RestaurantPizza(price=data["price"], pizza_id=data["pizza_id"], restaurant_id=data["restaurant_id"])
            db.session.add(restaurant_pizza)
            db.session.commit()
            
            body = restaurant_pizza.to_dict()
            status = 201
        except:
            body = {"errors": ["validation errors"]}
            status = 400
    
    return make_response(body, status)


    
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)