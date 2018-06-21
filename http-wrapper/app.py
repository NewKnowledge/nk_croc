#!/usr/bin/python3
import time

from flask import Flask, request, render_template
from json import dumps, loads

import pandas as pd
from keras.applications.inception_v3 import InceptionV3
from nk_croc import Croc
from utils import requires_auth


class CrocRestListener():
    """ **Class for managing croc config. Based off of CROC**
        CrocRestListener accepts an image path or URL
        and outputs a json file with the character and object
        information that has been deteected.
    """

    def __init__(self):
        self.croc = Croc()
        self.croc.model = InceptionV3(weights='imagenet')

    def analyze_image(self, image_path):
        """ analyze a given image and return text and detected objects
        """
        start = time.time()

        croc_result = self.croc.predict(input_path=image_path)

        print(
            "The whole script took %f seconds to execute"
            % (time.time()-start))
        return loads(croc_result)


# Init croc Class def'd above
listener = CrocRestListener()
# Hack-y work around for ensuring Keras Tensor map is available in the global scope.
# See https://github.com/keras-team/keras/issues/2397 for more info
listener.analyze_image(
    image_path="http://i0.kym-cdn.com/photos/images/facebook/001/253/011/0b1.jpg")
# Init Flask
app = Flask(__name__)


@app.route('/')
@requires_auth
def index():
    """ **Demo Landing Route**
    """
    return render_template('index.html')


@app.route("/demo-fileupload", methods=['POST'])
@requires_auth
def demo_analyze_uploaded_image():
    ''' **Demo Results Route**
        Listen for an image url being POSTed on root.
    '''
    request.get_data()

    image_path = request.form['image_path']

    result = listener.analyze_image(image_path=image_path)

    # Converting to pd.DataFrame seemed to be the fastest way to get results to a http table
    return render_template(
        'display.html', image_path=image_path,
        table=pd.DataFrame.from_dict(result['objects']).ix[:, [
            'label', 'confidence']].to_html(),
        chars={'text': result['text'], 'tokens': result['tokens']}, tree=result['object_trees'])


@app.route("/fileupload", methods=['POST'])
@requires_auth
def analyze_uploaded_image():
    ''' **Route for using croc as a http/web service**
        Listen for an image url being POSTed on root.
    '''
    request.get_data()

    image_path = request.form["image_path"]

    result = listener.analyze_image(image_path=image_path)

    result_dict = dumps(dict(
        objects=result['objects'],
        text=[str(i) for i in ['text']],
        tokens=result['tokens'],
        object_trees=result['object_trees']))

    return app.response_class(result_dict,  content_type='application/json')
