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

        # Make test variables
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
        res = self.client().get('/calls')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['calls'], list)
        self.assertIsInstance(data['total_calls'], int)

    def test_retrieve_calls_beyond_valid_page(self):
        res = self.client().get('/calls?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['calls'], list)
        self.assertEqual(len(data['calls']), 0)

    # --- CREATE NEW CALL --- #

    def test_add_call(self):
        res = self.client().post('/calls', json=self.new_call)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been created successfully.')

        _ = self.client().delete(f'/calls/{data["id"]}') # For reproducibility of DB

    def test_add_call_no_body(self):
        res = self.client().post('/calls')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request body is missing.')

    def test_add_call_no_question(self):
        res = self.client().post('/calls', json=self.new_call_no_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], '"question" is required in the request body.')

    def test_add_call_question_only(self):
        res = self.client().post('/calls', json=self.new_call_question_only)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Call record has been created successfully.')

        _ = self.client().delete(f'/calls/{data["id"]}') # For reproducibility of DB

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
