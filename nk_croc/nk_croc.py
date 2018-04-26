import io
import os
import time
import re
import string
from PIL import Image, ImageFilter

import requests
import spacy
from json import dumps
from tesserocr import PyTessBaseAPI
import numpy as np
import pandas as pd
from keras.preprocessing import image
from keras.applications.inception_v3 \
    import InceptionV3, decode_predictions, preprocess_input


class Croc():

    def __init__(self):
        self.target_size = (299, 299)
        self.model = InceptionV3(weights='imagenet')
        self.nlp = spacy.load('en')
        self.n_top_preds = 10

    def load_image(self, img_path, prep_func=lambda x: x):
        ''' load image given path and convert to an array
        '''
        img = image.load_img(img_path, target_size=self.target_size)
        x = image.img_to_array(img)
        return prep_func(x)

    def load_image_from_web(self, image_url):
        ''' load an image from a provided hyperlink
        '''
        # get image
        response = requests.get(image_url)
        with Image.open(io.BytesIO(response.content)) as img:
            # convert to jpeg
            if img.format is not 'jpeg':
                img = img.convert('RGB')
            img.save('target_img.jpg')

    def validate_url(self, url):
        url_validator = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return bool(url_validator.match(url))

    def cleanup_text(self, raw_chars):
        ''' use spacy to clean text and find tokens
        '''
        doc = self.nlp(raw_chars, disable=['parser', 'ner'])
        text = [t.text for t in doc]
        tokens = [tok.lemma_.lower().strip() for tok in doc
                  if tok.lemma_ != '-PRON-']
        tokens = [tok for tok in tokens
                  if tok not in self.nlp.Defaults.stop_words and
                  tok not in string.punctuation]

        return dict(tokens=list(set(tokens)), text=text)

    def classify_objects(self, image_array, decode_func):
        ''' Returns binary array with ones where the model predicts that
            the image contains an instance of one of the target classes
            (specified by wordnet id)
        '''
        predictions = self.model.predict(image_array)
        # decode the results into list of tuples (class, description, probability)
        predictions = decode_func(predictions, top=self.n_top_preds)
        return predictions

    def char_detect(self, img_path):
        ''' Run tesseract ocr on an image supplied
            as an image path.
        '''
        with PyTessBaseAPI() as ocr_api:
            with Image.open(img_path) as image:
                # will need a better preprocessing approach here
                # if we stay with tesseract:
                sharp_image = image.filter(ImageFilter.SHARPEN)

                ocr_api.SetImage(sharp_image)
                raw_chars = ocr_api.GetUTF8Text()
                # char_confs = ocr_api.AllWordConfidences()

                text = self.cleanup_text(raw_chars)

                # utf encode the clean raw output
                clean_chars = [i.encode('utf-8') for i in text['text']]

                return dict(tokens=text['tokens'], text=clean_chars)

    def predict(self, inputs):
        ''' Produce predictions for objects and text
        '''
        image_path = inputs

        print(image_path)

        if self.validate_url(image_path):
            filename = 'target_img.jpg'
            self.load_image_from_web(image_path)
        else:
            filename = image_path

        print('preprocessing image')
        X = np.array(
            [self.load_image(
                filename, prep_func=preprocess_input)])

        print('making object predictions')
        object_predictions = self.classify_objects(X, decode_predictions)

        object_predictions = pd.DataFrame.from_records(
            object_predictions[0], columns=['id', 'label', 'confidence'])

        print('performing character recognition')
        char_predictions = self.char_detect(filename)

        if filename == 'target_img.jpg':
            os.remove('target_img.jpg')

        return dumps(dict(
            objects=object_predictions.to_dict(),
            text=[str(i) for i in char_predictions['text']],
            tokens=char_predictions['tokens']))


if __name__ == '__main__':
    client = Croc()
    image_path = 'http://i0.kym-cdn.com/photos/images/facebook/001/253/011/0b1.jpg'
    result = client.predict(inputs=image_path)
    print(result)
