import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(resp):
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        resp.headers.add('Access-Control-Allow-Methods', 'POST, GET, DELETE')
        return resp

    def get_formated_categories():
        categories = Category.query.all()
        formated = {}
        for category in categories:
            formated[category.id] = category.type

        return formated

    def get_paginated_items(req, items, items_per_page=10):
        page = req.args.get('page', 1, int)
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        return items[start_index:end_index]

    @app.route('/categories')
    def get_categories():
        return jsonify({
            'success': True,
            'categories': get_formated_categories()
        })

    @app.route('/questions')
    def get_questions():
        current_category = request.args.get('category', None, int)
        if current_category is not None:
            questions = Question.query.join(Category, Category.id == Question.category
                                   ).filter(Category.id == current_category).all()
        else:
            questions = Question.query.all()

        current_questions = get_paginated_items(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in current_questions],
            'total_questions': len(questions),
            'categories': get_formated_categories(),
            'current_category': current_category
        })

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def remove_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted_id': question_id
            })
        except:
            abort(422)

    @app.route('/search', methods=['POST'])
    def search():
        search_term = request.get_json().get('search_term', None)
        if search_term is None:
            abort(400)

        search_term = '%{}%'.format(search_term)
        current_questions = Question.query.filter(
            Question.question.ilike(search_term)).all()

        return jsonify({
            'success': True,
            'questions':
                [question.format() for question in current_questions]
        })

    @app.route('/questions', methods=['POST'])
    def post_questions():
        data = request.get_json()
        if ('question' not in data or 'answer' not in data
                or 'category' not in data or 'difficulty' not in data):
            abort(400)
        new_question = Question(
            data['question'],
            data['answer'],
            data['category'],
            data['difficulty']
        )

        try:
            new_question.insert()

            return jsonify({
                'success': True,
                'created_id': new_question.id
            })
        except:
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        if 'category' not in data or 'previous_questions' not in data:
            abort(400)
            
        quiz_category = data.get('category')
        previous_questions = data.get('previous_questions')

        if quiz_category == 0:
            # all categories
            questions = Question.query.join(Category, Category.id == Question.category
                ).filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.join(Category, Category.id == Question.category
                ).filter(Category.id == quiz_category, Question.id.notin_(previous_questions)).all()

        try:
            question = random.choice(questions).format()
        except:
            question = None

        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def un_processable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'un processable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app
