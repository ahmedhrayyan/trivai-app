# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

Endpoints
* GET '/categories'
* GET '/questions'
* DELETE '/questions/question_id'
* POST '/questions'
* POST '/quizzes'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
  ```
  {
    'categories': {category_id: category_type...}
  }
  ```

### GET '/questions'
- Fetches a list of questions paginated by 10 questions a page with the total amount of questions available
- Request Arguments:
  - page
  - category
- Returns a dictionary with questions, total_questions, categories and current_category keys
  ```
  {
    'questions': [list of questions],
    'total_questions': <number>,
    'categories': {category_id: category_type...},
    'current_category': <category_id>
  }
  ```

### DELETE '/questions/<question_id>
- Delete the question which id was provided in the URI
- Request Arguments: None
- Return a dictionary with a single key, deleted_id
  ```
  {
    'deleted_id': <number>
  }

### POST '/questions'
- Post a new question to the database **OR** Post a search term
- Request Arguments: None
- Returns
  - if the post data have a search_term key the response would be a dictionary with a single key, questions, that contains a list of questions based on the search term
    ```
    {
      'questions': [list of questions]
    }
  - if the post data have a question, answer, category and difficulty keys, the request would insert a new question to the database and the response would be the created_id
    ```
    {
      'created_id': <number>
    }
    ```

### POST '/quizzes'
- Post categories and previous_questions list
- Request Arguments: None
- Return a question which is not one of the previous_questions and belongs to the provided category (if there were no match the question would be None)
  ```
  {
    'question': <question>
  }
  ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```