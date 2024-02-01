# flask_app/formatter.py
from flask import Blueprint, render_template, request

formatter = Blueprint('formatter', __name__)

def _formatter(format_input, format_type):
    if format_type == 'tupple':
        data_list = format_input.split()
        formatted_data = ', '.join(data_list)
        return f"({formatted_data})"
    elif format_type == 'binary':
        return bin(int(format_input))[2:]
    else:
        return "Invalid format type for number."


@formatter.route('/', methods=['GET', 'POST'])
def formatter_route():
    result = None
    old = None

    if request.method == 'POST':
        try:
            format_input = request.form['format_input']
            format_type = request.form['format_type']
            old = format_input
            result = _formatter(format_input, format_type)

        except ValueError:
            result = "Invalid input, please enter a valid number."

    return render_template('formatter.html', result=result, old=old)
