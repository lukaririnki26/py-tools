# flask_app/number_formatter.py
from flask import Blueprint, render_template, request

number_formatter = Blueprint('number_formatter', __name__)

def format_number(input_number, format_type):
    if format_type == 'decimal':
        return f"{input_number:,}"
    elif format_type == 'binary':
        return bin(int(input_number))[2:]
    elif format_type == 'hexadecimal':
        return hex(int(input_number))[2:]
    else:
        return "Invalid format type for number."

@number_formatter.route('/', methods=['GET', 'POST'])
def number_formatter_route():
    number_result = None

    if request.method == 'POST':
        try:
            input_number = float(request.form['input_number'])
            format_type = request.form['format_type']
            number_result = format_number(input_number, format_type)

        except ValueError:
            number_result = "Invalid input, please enter a valid number."

    return render_template('number_formatter.html', number_result=number_result)
