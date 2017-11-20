from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from os.path import join

from send_image import send_images_to_server

app = Flask(__name__)

CLIENT = MongoClient()
DB = CLIENT['iot']
USERS = DB['users']
UPLOAD_FOLDER = "./static/uploads"

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form['login_username']    
    password = request.form['login_password']
    user = USERS.find({"username":username})[0]
    if user['password'] != password:
        return "Invalid password"
    return render_template("home.html", user = user)

@app.route("/signup",methods=["POST"])
def signup():
    data = dict()
    data["username"] = request.form['username']
    data["email"] = request.form['email']
    data["password"] = request.form['password']
    USERS.insert_one(data)   
    return render_template("register.html")

@app.route("/send_images",methods=["POST"])
def send_images():
    username = request.form["username"]
    email_id = USERS.find_one({"username":username})["email"]
    image_1 = request.files["pic_1"]
    image_2 = request.files["pic_2"]
    image_3 = request.files["pic_3"]
    image_4 = request.files["pic_4"]
    image_5 = request.files["pic_5"]
    image_1.save(join(UPLOAD_FOLDER, secure_filename(image_1.filename)))
    image_2.save(join(UPLOAD_FOLDER, secure_filename(image_2.filename)))
    image_3.save(join(UPLOAD_FOLDER, secure_filename(image_3.filename)))
    image_4.save(join(UPLOAD_FOLDER, secure_filename(image_4.filename)))
    image_5.save(join(UPLOAD_FOLDER, secure_filename(image_5.filename)))
    send_images_to_server(str(email_id),str(username))
    return str(email_id)

if __name__ == "__main__":
    app.run(debug=True, port=2000)
