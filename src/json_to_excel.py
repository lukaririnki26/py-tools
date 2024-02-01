from flask import Blueprint, render_template, request, jsonify, send_file
import pandas as pd
import os
import io
import json

json_to_excel = Blueprint('json_to_excel', __name__)

@json_to_excel.route('/', methods=['GET'])
def index():
    return render_template('json_to_excel.html')

@json_to_excel.route('/', methods=['POST'])
def convert():
    data = request.form.get('data')

    if not data:
        return jsonify({"error": "No data provided"})

    try:
        data_json = json.loads(data)
        df = pd.DataFrame(data_json)
        temp_excel_file = 'temp_output.xlsx'
        df.to_excel(temp_excel_file, index=False)
        output = io.BytesIO()
        with open(temp_excel_file, 'rb') as file:
            output.write(file.read())
        os.remove(temp_excel_file)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='output.xlsx')

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})
