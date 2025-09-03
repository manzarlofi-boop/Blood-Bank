from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import re

app = Flask(__name__)
app.secret_key = "bloodbank_secret"  # flash messages ke liye

# MongoDB Connection
client = MongoClient("mongodb+srv://Blood9080:Blood9080@cluster0.xppo9z9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["blood_donation"]
donors_collection = db["donors"]

@app.route("/")
def home():
    return render_template("index.html")

# Donor Form
@app.route("/donor", methods=["GET", "POST"])
def donor():
    if request.method == "POST":
        name = request.form["name"].strip()
        dob = request.form["dob"].strip()
        age = request.form["age"].strip()
        gender = request.form["gender"].strip()
        aadhar = request.form["aadhar"].strip()
        phone = request.form["phone"].strip()
        email = request.form["email"].strip()
        blood_group = request.form["blood_group"].strip()

        # Validation
        if not all([name, dob, age, gender, aadhar, phone, email, blood_group]):
            flash("⚠️ All fields are required!", "danger")
            return redirect(url_for("donor"))

        if not age.isdigit() or int(age) < 18:
            flash("⚠️ Age must be 18 or above!", "danger")
            return redirect(url_for("donor"))

        if not re.fullmatch(r"\d{12}", aadhar):
            flash("⚠️ Aadhaar number must be 12 digits!", "danger")
            return redirect(url_for("donor"))

        if not re.fullmatch(r"\d{10}", phone):
            flash("⚠️ Phone number must be 10 digits!", "danger")
            return redirect(url_for("donor"))

        # Save donor
        donors_collection.insert_one({
            "name": name,
            "dob": dob,
            "age": int(age),
            "gender": gender,
            "aadhar": aadhar,
            "phone": phone,
            "email": email,
            "blood_group": blood_group
        })

        flash("✅ Donor Registered Successfully!", "success")
        return redirect(url_for("donor"))

    return render_template("donor.html")

# Receiver Form
@app.route("/receiver", methods=["GET", "POST"])
def receiver():
    donors = None
    if request.method == "POST":
        name = request.form["name"].strip()
        age = request.form["age"].strip()
        gender = request.form["gender"].strip()
        blood_group = request.form["blood_group"].strip()

        if not all([name, age, gender, blood_group]):
            flash("⚠️ All fields are required!", "danger")
            return redirect(url_for("receiver"))

        donors = list(donors_collection.find({"blood_group": blood_group}))

        if donors:
            flash(f"✅ Found {len(donors)} donor(s)!", "success")
        else:
            flash("❌ No donors found for this blood group.", "warning")

    return render_template("receiver.html", donors=donors)

if __name__ == "__main__":
    app.run(debug=True)
