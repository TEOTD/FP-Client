from flask import Flask, render_template, redirect, request
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import os
import torch
from torchvision import transforms
from mosquito_net import get_model
from io import BytesIO
from PIL import Image
# import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/Testing'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba358'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

classes = ['infected', 'uninfected']

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((120, 120)),
        transforms.ColorJitter(0.05),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(20),
        transforms.ToTensor(), 
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    image = Image.open(BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


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
    #print(output)
    predicted = torch.max(output, 1)[1][0]
    #print(predicted)
    return {'result': classes[predicted]}

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
