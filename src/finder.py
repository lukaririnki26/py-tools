# flask_app/finder.py
from flask import Blueprint, render_template, request
import re

finder = Blueprint('finder', __name__)

def find_duplicate_sku(data):
    # Use raw string for regex pattern to avoid issues with backslashes
    pattern = re.compile(r'\b\d{10}\b')

    seen_numbers = set()
    duplicate_numbers = set()

    matches = pattern.findall(data)
    if matches:
        for number in matches:
            if number in seen_numbers:
                duplicate_numbers.add(number)
            else:
                seen_numbers.add(number)

    return list(duplicate_numbers)

def _finder(finder_input, finder_type):
    if finder_type == 'duplicate_sku':
        result = find_duplicate_sku(finder_input)
        return f"Duplicate SKU: ({result})"
    else:
        error = f"Error: Invalid Finder Type"
        return render_template('finder.html', error=error)

@finder.route('/', methods=['GET', 'POST'])
def finder_route():
    result = None
    old = None

    if request.method == 'POST':
        try:
            finder_input = request.form['finder_input']
            finder_type = request.form['finder_type']
            old = finder_input
            result = _finder(finder_input, finder_type)

        except ValueError:
            error = f"Error: {str(e)}"
            return render_template('finder.html', error=error)

    return render_template('finder.html', result=result, old=old)
