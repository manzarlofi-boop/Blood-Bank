from flask import Flask, render_template, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Blood9080:Blood9080@cluster0.xppo9z9.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient(MONGO_URL)
db = client["blood_donation"]
donors = db["donors"]

@app.route("/")
def home():
    return render_template("home.html")

# Donor Registration
@app.route("/donor", methods=["GET", "POST"])
def donor():
    if request.method == "POST":
        donor_data = {
            "name": request.form["name"],
            "dob": request.form["dob"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "aadhar": request.form["aadhar"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "blood_group": request.form["blood_group"]
        }
        donors.insert_one(donor_data)
        return "✅ Donor Registered Successfully!"
    return render_template("donor_form.html")

# Receiver Form
@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    if request.method == "POST":
        blood_group = request.form["blood_group"]
        results = list(donors.find({"blood_group": blood_group}))
        return render_template("results.html", donors=results, blood_group=blood_group)
    return render_template("receiver_form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
