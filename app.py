# flask_app/app.py
from flask import Flask, render_template
from src.finder import finder
from src.formatter import formatter

app = Flask(__name__)

app.register_blueprint(finder, url_prefix='/finder')
app.register_blueprint(formatter, url_prefix='/formatter')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
