from flask import Flask, render_template, redirect, request
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import os
# import requests
app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/Testing'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba358'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        first_name = request.form.get("username")
        return redirect(url_for('application', name=first_name))
    return render_template('login.html', title='Login')


@app.route("/application", methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return "UPLOAD SUCESSFULL"
    name = request.args['name']
    return render_template('application.html', name=name)

# @app.route("/verification", methods=['GET', 'POST'])
# def verification():
#     if request.method == "POST":

# @app.route("/correct", methods=['GET', 'POST'])
# def correct():
#     if request.method == "POST":

# @app.route("/sync" , methods=['GET', 'POST'])
# def sync():

# @app.route("/exit" , methods=['GET','POST'])
# def exit():

# url = "http://localhost/average"

# files = [
#     ('model', ('model.pt', open('model.pt', 'rb'), 'application/octet-stream'))
# ]
# response = requests.request("POST", url, files=files)
# print("Response received")
# open('model1.pt', 'wb').write(response.content)


if __name__ == '__main__':
    app.run(debug=True)
