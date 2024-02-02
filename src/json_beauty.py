from flask import Blueprint, render_template, request, jsonify
import json

json_beauty = Blueprint('json_beauty', __name__)

@json_beauty.route('/', methods=['GET', 'POST'])
def beautify_json():
    if request.method == 'POST':
        try:
            # Assuming the incoming data is a JSON string
            json_data = request.form.get('json_data')

            # Load JSON data and dump with indentation for readability
            result = json.dumps(json.loads(json_data), indent=4)

            return render_template('json_beauty.html', result=result)
        except Exception as e:
            error = f"Error: {str(e)}"
            return render_template('json_beauty.html', error=error)

    return render_template('json_beauty.html')

