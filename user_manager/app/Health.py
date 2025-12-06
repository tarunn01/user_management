from flask import Flask
from flask_restful import Resource


class Health(Resource):
    """
    GET /health
    Public endpoint to check if the service is running.
    Response: 200 OK with {"status": "healthy"}
    """
    def get(self):
        return {"status": "healthy"}, 200