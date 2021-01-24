import json
from flask import (
    Flask,
    request,
    abort,
    jsonify,
)
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from models import (
    setup_db,
    Call,
    Offer,
    Panelist,
    Topic,
)
from utils import paginate


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
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

    #----------------------------------------------------------------------------#
    # Controllers
    #----------------------------------------------------------------------------#

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': "Welcome to Daedam!"
        })


    @app.route('/calls')
    def retrieve_calls():
        calls = Call.query.order_by(
            Call.id.desc() # Latest first
        ).all()

        current_calls = paginate(request, calls)

        return jsonify({
            'success': True,
            'calls': [c.format() for c in current_calls],
            'total_calls': len(calls)
        }), 200


    @app.route('/calls', methods=['POST'])
    def create_call():
        body = request.get_json()
        if not body:
            abort(400, 'Request body is missing.')

        c = Call(
            question = body.get('question'),
            description = json.dumps(body.get('description'))
        )
        if c.question is None:
            abort(400, '`question` is required in the request body.')

        try:
            c.insert()
            call_id = c.id
        except:
            abort(422, 'Database error: Insertion failed.')

        return jsonify({
            'success': True,
            'message': f'<Call ID: {call_id}> has been created successfully.'
        }), 201


    @app.route('/calls/<int:call_id>', methods=['DELETE'])
    def delete_call(call_id):
        c = Call.query.get(call_id)
        if not c:
            abort(404, f'<Call ID: {call_id}> does not exist already.')

        try:
            c.delete()
        except:
            abort(422, 'Database error: Deletion failed.')

        return jsonify({
            'success': True,
            'message': f'<Call ID: {call_id}> has been deleted successfully.'
        })

    #----------------------------------------------------------------------------#
    # Error Handlers
    #----------------------------------------------------------------------------#

    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        """
        HTTP error handler for all endpoints.
        """
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code


    @app.errorhandler(Exception)
    def exception_handler(error):
        """
        Generic error handler for all endpoints.
        """
        return jsonify({
            'success': False,
            'error': 500,
            'message': f'Something went wrong: {error}'
        }), 500


    return app


app = create_app()

if __name__ == '__main__':
    app.run()
