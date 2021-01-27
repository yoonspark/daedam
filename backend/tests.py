import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import (
    setup_db,
    Call,
    Offer,
    Panelist,
    Topic,
)
from config import (
    JWT_AUDIENCE,
    JWT_MODERATOR,
    JWT_ADMIN,
)


class DaedamTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize app
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, 'postgres://localhost:5432/daedam_test')

        # Bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # Make test headers
        self.headers_audience = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {JWT_AUDIENCE}'
        }
        self.headers_moderator = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {JWT_MODERATOR}'
        }
        self.headers_admin = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {JWT_ADMIN}'
        }

        # Make test data
        self.new_call = {
            'question': 'Does the universe have an end?',
            'description': 'I want a blend of diverse perspectives including those from philosophy, science, and religion.',
            'topics': ['philosophy', 'science', 'religion']
        }
        self.new_call_question_only = {
            'question': 'Do we live in a simulation?',
        }
        self.new_call_no_question = {
            'description': 'I want various scientific perspectives.',
            'topics': ['physics', 'chemistry', 'biology']
        }

    def tearDown(self):
        pass

    # --- RETRIEVE ALL CALLS --- #

    def test_retrieve_calls(self):
        res = self.client().get('/calls', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['calls'], list)
        self.assertIsInstance(data['total_calls'], int)

    def test_retrieve_calls_beyond_valid_page(self):
        res = self.client().get('/calls?page=99999', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['calls'], list)
        self.assertEqual(len(data['calls']), 0)

    def test_retrieve_calls_no_headers(self):
        res = self.client().get('/calls')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # --- CREATE NEW CALL --- #

    def test_create_call(self):
        res = self.client().post('/calls', headers=self.headers_audience, json=self.new_call)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been created successfully.')
        self.assertIsInstance(data['id'], int)

        # For reproducibility of DB, delete the created record
        _ = self.client().delete(f'/calls/{data["id"]}', headers=self.headers_audience)

    def test_create_call_no_body(self):
        res = self.client().post('/calls', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], 'Request body is missing.')

    def test_create_call_no_question(self):
        res = self.client().post('/calls', headers=self.headers_audience, json=self.new_call_no_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], '"question" is required in the request body.')

    def test_create_call_question_only(self):
        res = self.client().post('/calls', headers=self.headers_audience, json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been created successfully.')
        self.assertIsInstance(data['id'], int)

        # For reproducibility of DB, delete the created record
        _ = self.client().delete(f'/calls/{data["id"]}', headers=self.headers_audience)

    def test_create_call_no_headers(self):
        res = self.client().post('/calls', json=self.new_call)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_create_call_wrong_permission(self):
        res = self.client().post('/calls', headers=self.headers_moderator, json=self.new_call)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # --- DELETE CALL --- #

    def test_delete_call(self):
        # Create a test record
        res = self.client().post('/calls', headers=self.headers_audience, json=self.new_call)
        data = json.loads(res.data)
        call_id = data["id"]

        res = self.client().delete(f'/calls/{call_id}', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been deleted successfully.')
        self.assertEqual(data['id'], call_id)

    def test_delete_call_not_exist(self):
        res = self.client().delete('/calls/99999', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Call record does not exist.')

    def test_delete_call_no_headers(self):
        res = self.client().delete('/calls/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_delete_call_wrong_permission(self):
        res = self.client().delete('/calls/3', headers=self.headers_moderator)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # --- RETRIEVE SINGLE CALL --- #

    def test_retrieve_call(self):
        res = self.client().get('/calls/1', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['calls'], list)
        self.assertEqual(data['total_calls'], 1)

    def test_retrieve_call_not_exist(self):
        res = self.client().get('/calls/99999', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Call record does not exist.')

    def test_retrieve_call_no_headers(self):
        res = self.client().get('/calls/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # --- UPDATE CALL --- #

    def test_update_call_question_only(self):
        res = self.client().patch('/calls/1', headers=self.headers_audience, json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been updated successfully.')
        self.assertEqual(data['id'], 1)

    def test_update_call_no_question(self):
        res = self.client().patch('/calls/1', headers=self.headers_audience, json=self.new_call_no_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been updated successfully.')
        self.assertEqual(data['id'], 1)

    def test_update_call_no_body(self):
        res = self.client().patch('/calls/1', headers=self.headers_audience)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], 'Request body is missing.')

    def test_update_call_not_exist(self):
        res = self.client().patch('/calls/99999', headers=self.headers_audience, json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Call record does not exist.')

    def test_update_call_no_headers(self):
        res = self.client().patch('/calls/1', json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_update_call_wrong_permission(self):
        res = self.client().patch('/calls/1', headers=self.headers_moderator, json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
