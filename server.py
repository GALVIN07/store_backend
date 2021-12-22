"""
Desc: ackend for the online store
AUthor: Gary Galvin
"""

from flask import Flask, abort, request, render_template 
from mock_data import catalog
import json
from config import db, json_parse
from bson import ObjectId
from bson.errors import InvalidId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

about_me = {
    "name": "Gary",
    "last": "Galvin",
    "age": 33,
    "hobbies": [],
    "address": {
        "street": "2717 thisway",
        "city": "Springfield"
    }
}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


"""

API ENDPOINTS

"""

@app.route("/api/catalog", methods=["get"])
def retrieve_catalog():
    cursor = db.products.find({})
    list = []
    for  prod in cursor:
        list.append(prod)

    return json_parse(list) 


@app.route("/api/catalog", methods=["post"])
def save_catalog():
    product = request.get_json()

    db.products.insert_one(product)


    return json_parse(product)


@app.route("/api/product/<id>")
def get_product(id):
    try:
        objectId_instance = ObjectId(id)
        prod = db.products.find_one({"_id": objectId_instance})
        if prod is not None:
            return json_parse(prod)
        return abort(404)

    except InvalidId:
        print("Error: Invalid Object ID", id)
        return abort(400)

@app.route("/api/catalog/<category>")
def get_product_by_category(category):
    cursor = db.products.find({"category": category})
    
    list = []

    for prod in cursor:
        list.append(prod)

    return json.dumps(list)


@app.route("/api/products/cheapest")
def get_cheapest_product():

    cursor = db.products.find({})

    cheapest_prod = cursor[0]

    for prod in cursor:
        if(prod["price"] < cheapest_prod["price"]):
            cheapest_prod = prod
    return json_parse(cheapest_prod)


@app.route("/api/products/categories")
def get_unique_categories(): 
    categories = []

    cursor = db.products.find({})
    for prod in cursor:
        cat = prod["category"]
        if cat not in categories:
            categories.append(cat)
    return json_parse(categories)


@app.route("/api/total")
def report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
        total += prod["price"]
        

    return json_parse(total)


@app.route("/api/order", methods=["POST"])
def save_order():
    order = request.get_json()
    total = 0
    for prod in order["products"]:
        db_prod = db.products.find_one({"_id": ObjectId(prod["_id"])})
        price = db_prod["price"]
        quantity = prod["quantity"]
        total += price * quantity

    if total <= 0:
        return abort(400)

    order["total"] = total 
    db.orders.insert_one(order)
    return json_parse(order)




@app.route("/test/onetime/filldb")

def fill_db():
    for prod in catalog:
        prod.pop("_id")

        db.products.insert_one(prod)

    return "Done!"


    

# REMOVE BEFORE DEPLOYING
app.run(debug=True)