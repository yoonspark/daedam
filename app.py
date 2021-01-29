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
from utils import (
    paginate,
    get_topic,
    get_panelist,
)
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
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

    # -------------------------------------------------------- #
    # Controllers
    # -------------------------------------------------------- #

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': "Welcome to Daedam!"
        })

    #  Calls
    #  ---------------------------------------------

    @app.route('/calls')
    @requires_auth('read:calls')
    def retrieve_calls(payload):
        calls = Call.query.order_by(
            Call.id.desc()  # Latest first
        ).all()

        current_calls = paginate(request, calls)

        return jsonify({
            'success': True,
            'calls': [c.format() for c in current_calls],
            'total_calls': len(calls)
        }), 200

    @app.route('/calls', methods=['POST'])
    @requires_auth('create:calls')
    def create_call(payload):
        body = request.get_json()
        if not body:
            abort(400, 'Request body is missing.')
        if body.get('question') is None:
            abort(400, '"question" is required in the request body.')

        # Create a new record
        c = Call(
            question=body.get('question'),
            description=body.get('description', ''),
            topics=[get_topic(name=t) for t in body.get('topics', [])]
        )
        try:
            c.insert()
            call_id = c.id
        except Exception:
            abort(422, 'Database error: Insertion failed.')

        return jsonify({
            'success': True,
            'message': 'Call record has been created successfully.',
            'id': call_id
        }), 201

    @app.route('/calls/<int:call_id>')
    @requires_auth('read:calls')
    def retrieve_call(payload, call_id):
        c = Call.query.get(call_id)
        if not c:
            abort(404, 'Call record does not exist.')

        return jsonify({
            'success': True,
            'calls': [c.format()],
            'total_calls': 1
        }), 200

    @app.route('/calls/<int:call_id>', methods=['PATCH'])
    @requires_auth('update:calls')
    def update_call(payload, call_id):
        body = request.get_json()
        if not body:
            abort(400, 'Request body is missing.')

        c = Call.query.get(call_id)
        if not c:
            abort(404, 'Call record does not exist.')

        # Update the record
        if body.get('question'):
            c.question = body.get('question')
        if body.get('description'):
            c.description = body.get('description')
        if body.get('topics'):
            c.topics = [get_topic(name=t) for t in body.get('topics')]
        try:
            c.update()
        except Exception:
            abort(422, 'Database error: Update failed.')

        return jsonify({
            'success': True,
            'message': 'Call record has been updated successfully.',
            'id': call_id
        }), 200

    @app.route('/calls/<int:call_id>', methods=['DELETE'])
    @requires_auth('delete:calls')
    def delete_call(payload, call_id):
        c = Call.query.get(call_id)
        if not c:
            abort(404, 'Call record does not exist.')

        try:
            c.delete()
        except Exception:
            abort(422, 'Database error: Deletion failed.')

        return jsonify({
            'success': True,
            'message': 'Call record has been deleted successfully.',
            'id': call_id
        }), 200

    #  Offers
    #  ---------------------------------------------

    @app.route('/offers')
    @requires_auth('read:offers')
    def retrieve_offers(payload):
        offers = Offer.query.order_by(
            Offer.id.desc()  # Latest first
        ).all()

        current_offers = paginate(request, offers)

        return jsonify({
            'success': True,
            'offers': [o.format() for o in current_offers],
            'total_offers': len(offers)
        }), 200

    @app.route('/offers', methods=['POST'])
    @requires_auth('create:offers')
    def create_offer(payload):
        body = request.get_json()
        if not body:
            abort(400, 'Request body is missing.')
        if body.get('title') is None:
            abort(400, '"title" is required in the request body.')

        # Create a new record
        o = Offer(
            title=body.get('title'),
            contents=body.get('contents', ''),
            event_time=body.get('event_time'),  # Null if not found
            finalized=body.get('finalized', False),
            topics=[get_topic(name=t) for t in body.get('topics', [])],
            panelists=[
                get_panelist(name=p) for p in body.get('panelists', [])
            ]
        )
        try:
            o.insert()
            offer_id = o.id
        except Exception:
            abort(422, 'Database error: Insertion failed.')

        return jsonify({
            'success': True,
            'message': 'Offer record has been created successfully.',
            'id': offer_id
        }), 201

    @app.route('/offers/<int:offer_id>')
    @requires_auth('read:offers')
    def retrieve_offer(payload, offer_id):
        o = Offer.query.get(offer_id)
        if not o:
            abort(404, 'Offer record does not exist.')

        return jsonify({
            'success': True,
            'offers': [o.format()],
            'total_offers': 1
        }), 200

    @app.route('/offers/<int:offer_id>', methods=['PATCH'])
    @requires_auth('update:offers')
    def update_offer(payload, offer_id):
        body = request.get_json()
        if not body:
            abort(400, 'Request body is missing.')

        o = Offer.query.get(offer_id)
        if not o:
            abort(404, 'Offer record does not exist.')

        # Update the record
        if body.get('title'):
            o.title = body.get('title')
        if body.get('contents'):
            o.contents = body.get('contents')
        if body.get('event_time'):
            o.event_time = body.get('event_time')
        if body.get('finalized'):
            o.finalized = body.get('finalized')
        if body.get('topics'):
            o.topics = [get_topic(name=t) for t in body.get('topics')]
        if body.get('panelists'):
            o.panelists = [get_panelist(name=p) for p in body.get('panelists')]
        try:
            o.update()
        except Exception:
            abort(422, 'Database error: Update failed.')

        return jsonify({
            'success': True,
            'message': 'Offer record has been updated successfully.',
            'id': offer_id
        }), 200

    @app.route('/offers/<int:offer_id>', methods=['DELETE'])
    @requires_auth('delete:offers')
    def delete_offer(payload, offer_id):
        o = Offer.query.get(offer_id)
        if not o:
            abort(404, 'Offer record does not exist.')

        try:
            o.delete()
        except Exception:
            abort(422, 'Database error: Deletion failed.')

        return jsonify({
            'success': True,
            'message': 'Offer record has been deleted successfully.',
            'id': offer_id
        }), 200

    # -------------------------------------------------------- #
    # Error Handlers
    # -------------------------------------------------------- #

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

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

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
