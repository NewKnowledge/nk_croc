# nk_croc
Character recognition and object classification system for images

## Quick Start

Use CROC in your project via pip with `pip3 install -e <path/to/croc>`.

or

Start CROC as a service on your local-machine with:

1) `docker build -t croc-http:dev -f ./http.dockerfile .`
2) `docker run -p 5000:5000 croc-http:dev`

## Configuration

You can set the following env vars to change some behaviors.

- `GET_IMAGE_TIMEOUT`: int. max number of seconds to wait before triggering timeout error when downloading an image. *Default is 10s.*
- `USE_REQUESTS_SESSION`: boolean. Toggle option for using sessions when downloading images (True) or to create a new connection on every request (False). *Default is True.* 

## Structure of this repo

The core of this repo is `setup.py` and `nk_croc`. 

This repo is pip-installsable and makes the contents of `nk_croc` available after installation.

There is a flask wrapper for the library located in `http-wrapper`. It uses `nk_croc` and can be built with the `http.dockerfile`. For more information see [the README.md in `http-wrapper`](./http-wrapper/README.md)

## Coming soon

- Other wrappers for croc that are segmented out in other repos?
