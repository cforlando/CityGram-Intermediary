"""
cgorl.__init__ - High-level Flask application and routes
"""

# library
from flask import Flask
from flask_cors import CORS
# module
from cgorl.services import SERVICES

app = Flask(__name__)
cors = CORS(app, resources={
    r'/api/*': {'origins': '*'}
})

@app.route('/')
def home() -> str:
    """
    Returns the home page with a list of available services
    """
    return 'Available services: ' + ','.join(SERVICES.keys())

@app.route('/<tag>')
def service(tag: str) -> str:
    """
    """
    if tag in SERVICES:
        service = SERVICES[tag]
        return 'Good tag: ' + service.tag
    else:
        return 'Service not found'
