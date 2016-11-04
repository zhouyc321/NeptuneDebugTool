#!flask/bin/python

# all the imports
from flask import Flask, render_template
import logging

app = Flask(__name__)
logger = logging.getLogger('debugTool.log')

from routes.debugTool import bp as debug_page_routes
#ROUTERS
app.register_blueprint(debug_page_routes)

def initialize(): pass

app.before_first_request(initialize)

if __name__ == "__main__":
    logger.info('Running in debug mode.')
    app.run(host='0.0.0.0', port=5000, debug=True)
