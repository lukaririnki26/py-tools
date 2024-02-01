# flask_app/app.py
from flask import Flask, render_template
from temperature_converter import temperature_converter
from number_formatter import number_formatter

app = Flask(__name__)

app.register_blueprint(temperature_converter, url_prefix='/temperature')
app.register_blueprint(number_formatter, url_prefix='/number')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
