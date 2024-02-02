# flask_app/app.py
from flask import Flask, render_template
from src.finder import finder
from src.formatter import formatter
from src.excel_to_json import excel_to_json
from src.json_to_excel import json_to_excel
from src.html_table_to_excel import html_table_to_excel

app = Flask(__name__)

app.register_blueprint(finder, url_prefix='/finder')
app.register_blueprint(formatter, url_prefix='/formatter')
app.register_blueprint(excel_to_json, url_prefix='/excel_to_json')
app.register_blueprint(json_to_excel, url_prefix='/json_to_excel')
app.register_blueprint(html_table_to_excel, url_prefix='/html_table_to_excel')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port= 50002)
