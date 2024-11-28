import logging

from flask import Flask

from init_db import init_neo4j
from init_db import init_redis
from bluprint.analysis_bp import analysis_bp
app = Flask(__name__)

app.register_blueprint(analysis_bp, url_prefix='/api/v1/analysis')

app.config['DEBUG'] = True
app.config['LOGGING_LEVEL'] = logging.DEBUG


with app.app_context():
    app.driver =  init_neo4j()
    app.redis = init_redis()

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0" ,port=5001)