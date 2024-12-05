'''
Run.py runs the flask application from __init__.py
'''
from flask_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)