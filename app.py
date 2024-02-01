# flask_app/app.py
from flask import Flask, render_template
from src.finder import finder
from src.formatter import formatter
from src.excel_to_json import excel_to_json

app = Flask(__name__)

app.register_blueprint(finder, url_prefix='/finder')
app.register_blueprint(formatter, url_prefix='/formatter')
app.register_blueprint(excel_to_json, url_prefix='/excel_to_json')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
