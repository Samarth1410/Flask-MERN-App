# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import json

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SIP"]   #DB represents database named SIP
collection = db["investments"]      #collection reprents table named investments

@app.route("/calculate", methods=["POST"])
def calculate():
    print("start loading data")
    data = json.loads(request.data)
    print(data)
    
    name = data["name"]
    years = int(data["years"])
    amount = float(data["amount"])*12
    rate = float(data["rate"])
    print(rate)
    # Calculate Future amount
    i = (rate / 100) / 12
    res =  amount * (((1 + i)**years - 1) / i) * (1 + i)
    
    # Store data in MongoDB
    investment_data = {
        "name": name,
        "years": years,
        "investment": amount,
        "interestRate": rate,
        "SIP": res
    }
    collection.insert_one(investment_data)
    
    return jsonify({"Final": res})

if __name__ == "__main__":
    app.run(debug=True)
