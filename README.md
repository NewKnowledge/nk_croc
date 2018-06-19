# CROC
Character recognition and object classification system for images

The easiest way to get started is to clone and use `docker build .` to create a docker environment to run CROC. 

There are presently three ways to interact with CROC:
- a web-based GUI demonstration version
- a web-based REST interface conforming to the design pattern used with other containerized *New Knowledge* services 
- a "batch" script that can be pointed to a directory of images and executed out-of-the-box 

Once the container is running, the GUI and REST versions can be initiated with `sh start_flask_demo.sh` and `sh start_flask.sh`, respectively.

See `test_rest.py` for an example of how to interact with the REST version.

For the batch approach (`main.py`), you only need to change the `img_path` string variable to point to your directory of images and then run the script. It will produce a `.pickle` for you with the objects and characters detected in each of the images in the directory.

TODOs:
Inputs as images in buffer (i.e., `PIL.Image`) may be preferred to the current web-based URL/local path design.

`PIP`-installable option for integration into D3M
