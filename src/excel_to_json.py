from flask import Blueprint, render_template, request, jsonify, send_file
import pandas as pd
import os
import io
import json

excel_to_json = Blueprint('excel_to_json', __name__)

@excel_to_json.route('/', methods=['GET'])
def index():
    return render_template('excel_to_json.html')

@excel_to_json.route('/', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    try:
        # Read Excel file into a DataFrame
        df = pd.read_excel(file, engine='openpyxl')

        # Convert DataFrame to JSON
        result = df.to_dict(orient='records')

        return render_template('excel_to_json.html', result=result)

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})

@excel_to_json.route('/download', methods=['GET', 'POST'])
def download():
    data = request.form.get('data')

    if not data:
        return jsonify({"error": "No data provided"})

    try:
        data_json = json.loads(data)
        json_str = json.dumps(data_json, indent=2, ensure_ascii=False)
        output = io.BytesIO()
        output.write(json_str.encode('utf-8'))
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='output.json', mimetype='application/json')

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})