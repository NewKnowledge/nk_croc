# CROC flask-api wrapper

More like `WRITEME.md` amiright?!

## Running 

From the root of the project 

1) `docker build -t croc-api:dev -f ./api.dockerfile .`
2) `docker run -it --rm -p 5000:5000 -v $(pwd):/app croc-api:dev bash`
    - This drops you into an interactive shell in the container with your local/host files mounted so your changes are reflected in the container
3) In the interactive-shell/container run `python3 -m flask run --host 0.0.0.0 --port 5000`
4) When you make some changes kill the running process with `ctrl c` and rerun step 3.
