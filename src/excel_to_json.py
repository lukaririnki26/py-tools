from flask import Blueprint, render_template, request, jsonify, send_file
import pandas as pd
import io
import json
import numpy as np

excel_to_json = Blueprint('excel_to_json', __name__)

@excel_to_json.route('/', methods=['GET'])
def index():
    return render_template('excel_to_json.html')

@excel_to_json.route('/', methods=['POST'])
def convert():
    if 'file' not in request.files:
        error = "Error: No File Part"
        return render_template('excel_to_json.html', error=error)

    file = request.files['file']

    if file.filename == '':
        error = "Error: No Selected File"
        return render_template('excel_to_json.html', error=error)

    custom_keys = request.form.get('custom_keys')
    try:
        custom_keys = json.loads(custom_keys) if custom_keys else {}
    except json.JSONDecodeError as e:
        error = f"Error: Invalid JSON format for custom keys. {str(e)}"
        return render_template('excel_to_json.html', error=error)

    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(file, engine='openpyxl')

        # Replace NaN with None (which will be converted to null in JSON)
        df.replace({pd.NA: None, np.nan: None}, inplace=True)

        # Create a custom JSON structure with custom keys or default to column names
        result = []
        for _, row in df.iterrows():
            item = {}
            for col in df.columns:
                custom_key = custom_keys.get(col, col)  # Use custom key if available, otherwise default to column name
                item[custom_key] = row[col]
            result.append(item)

        # Convert JSON to string and write to a BytesIO object
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        output = io.BytesIO()
        output.write(json_str.encode('utf-8'))
        output.seek(0)

        # Send the JSON file as a download
        return send_file(output, as_attachment=True, download_name='output.json', mimetype='application/json')

    except Exception as e:
        error = f"Error: {str(e)}"
        return render_template('excel_to_json.html', error=error)
