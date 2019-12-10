from flask import Flask
from flask_restful import Api

from src.route.process import Process
from src.config.server_config import server_params

app = Flask(__name__)
api = Api(app)

api.add_resource(Process, '/process')

if __name__ == '__main__':
    app.run(host=server_params["host"], port=server_params["port"])
