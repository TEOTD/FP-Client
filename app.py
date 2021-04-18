from flask import Flask, render_template, redirect, request
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import os
import torch
from mosquito_net import get_model, transform_image, train_model
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/Testing'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba358'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

weightsPath = os.path.join('static', os.path.join('weights', 'model.pt'))
classes = ['infected', 'uninfected']


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        first_name = request.form.get("username")
        return redirect(url_for('application', name=first_name))
    return render_template('login.html', title='Login')


@app.route("/application", methods=['GET'])
def application():
    name = request.args['name']
    return render_template('application.html', name=name)


@app.route('/test', methods=['POST'])
def test():

    file = request.files['image']
    image = file.read()

    model = get_model()
    model.eval()

    tesnor = transform_image(image_bytes=image)

    output = model.forward(tesnor)
    predicted = torch.max(output, 1)[1][0]
    return {'result': classes[predicted]}


@app.route('/validate', methods=['POST'])
def validate():
    file = request.files['image']
    image = file.read()

    label = [int(request.form["result"])]

    loss = train_model(image, label)

    return {'loss': loss}


@app.route('/sync', methods=['GET'])
def sync():
    url = "http://localhost:8000/average"

    payload = {'name': request.args['name']}
    files = [
        ('model', ('model.pt', open(weightsPath, 'rb'), 'application/octet-stream'))
    ]

    response = requests.request("POST", url, files=files, data=payload)

    if(response.status_code == 200):
        print("Response received")
        open(weightsPath, 'wb').write(response.content)

    return ""


if __name__ == '__main__':
    app.run(debug=True)
