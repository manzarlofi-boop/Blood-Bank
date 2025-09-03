from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Blood9080:Blood9080@cluster0.xppo9z9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["bloodbank"]
donors = db["donors"]

@app.route("/")
def home():
    return render_template("donor_form.html")

@app.route("/register_donor", methods=["POST"])
def register_donor():
    donor = {
        "name": request.form["name"],
        "dob": request.form["dob"],
        "age": request.form["age"],
        "gender": request.form["gender"],
        "blood_group": request.form["blood_group"],
        "aadhar": request.form["aadhar"],
        "phone": request.form["phone"]
    }
    donors.insert_one(donor)
    return "✅ Donor Registered Successfully! <a href='/'>Go Back</a>"

@app.route("/receiver")
def receiver_form():
    return render_template("receiver_form.html")

@app.route("/search_donor", methods=["POST"])
def search_donor():
    blood_group = request.form["blood_group"]
    results = donors.find({"blood_group": blood_group})
    return render_template("donors_list.html", donors=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
