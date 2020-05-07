import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'admin', 'secret', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path, True)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        first_category = Category.query.first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['categories']['1'], first_category.type)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        first_quiestion = Question.query.first().format()
        total_quiestions = len(Question.query.all())
        first_category = Category.query.first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['categories']['1'], first_category.type)
        self.assertEqual(data['questions'][0], first_quiestion)
        self.assertEqual(data['total_questions'], total_quiestions)

    def test_404_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')

    def test_remove_questions(self):
        total_questions_before = len(Question.query.all())
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(total_questions_before - 1, total_questions_after)

    def test_404_remove_questions(self):
        res = self.client().delete('/questions/2832')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question(self):
        new_question = {
            'question': 'this is a question',
            'answer': 'this is an answer',
            'category': 1,
            'difficulty': 1
        }
        total_questions_before = len(Question.query.all())
        res = self.client().post(
            '/questions', data=json.dumps(new_question), content_type='application/json')
        data = json.loads(res.data)
        total_questions_after = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(total_questions_before + 1, total_questions_after)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
