# CROC flask-api wrapper

A Flask wrapper for CROC

## Getting Started 

From the root of the project 

1) `docker build -t croc-api:dev -f ./api.dockerfile .`
2) `docker run -dp 5000:5000 croc-api:dev`

## Routes

`GET /` - Landing page for demos. Has one input that is expecting a URL to a hosted image

`POST /demo-demo-fileupload` - A page for an example visualizing the response from croc for a given image URL. The route is expecting form-data with the key "image_path" with the value being a URL to a hosted image to be processed.

`POST /fileupload` - Returns JSON response from croc for a given image URL. The route is expecting form-data with the key "image_path" with the value being a URL to a hosted image to be processed.

## Developing

1) `docker build -t croc-api:dev -f ./api.dockerfile .`
2) `docker run -it --rm -p 5000:5000 -v $(pwd):/app croc-api:dev bash`
    - This drops you into an interactive shell in the container with your local/host files mounted so your changes are reflected in the container
3) In the interactive-shell/container run `python3 -m flask run --host 0.0.0.0 --port 5000`
4) When you make some changes kill the running process with `ctrl c` and rerun step 3.

This process probably could be improved. It takes a few moments to kill the flask process and it takes over a minute to re-mount/init the keras model which happens every time the process is started.
