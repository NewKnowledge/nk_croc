#!/usr/bin/python3

from flask import Flask, request, render_template
from json import dumps

from keras.applications.inception_v3 import InceptionV3
from nk_croc import Croc

# Initialize flask
listener = Croc()
listener.model = InceptionV3(weights='imagenet')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/demo-fileupload", methods=['POST'])
def demo_analyze_uploaded_image():
    ''' Listen for an image url being POSTed on root.
    '''
    request.get_data()

    image_path = request.form['image_path']

    result = listener.predict(input_path=image_path)

    return render_template(
        'display.html', image_path=image_path,
        table=result['objects'].ix[:, ['label', 'confidence']].to_html(),
        chars=result['chars'], tree=result['object_trees'])


@app.route("/fileupload", methods=['POST'])
def analyze_uploaded_image():
    ''' Listen for an image url being POSTed on root.
    '''
    request.get_data()

    image_path = request.form["image_path"]

    result = listener.predict(input_path=image_path)

    result_dict = dumps(dict(
        objects=result['objects'].to_dict(),
        text=[str(i) for i in result['chars']['text']],
        tokens=result['chars']['tokens'],
        object_trees=result['object_trees']))

    return app.response_class(result_dict,  content_type='application/json')
