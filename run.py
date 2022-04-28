from uvicorn import run

from dndman_api import app

run(app, host="localhost", port=8080)
