from flask import (
    Flask,
    request,
    abort,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# from models import (
#     setup_db,
# )


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    # setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )

        return response


    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': "Welcome to Daedam!"
        })


    return app


app = create_app()

if __name__ == '__main__':
    app.run()
