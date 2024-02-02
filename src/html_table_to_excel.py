from flask import Blueprint, render_template, request, send_file
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
import requests

html_table_to_excel = Blueprint('html_table_to_excel', __name__)

def fetch_html_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text

def _html_table_to_excel(html_content, table_id, sheet_name='converted_table'):
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find(id=table_id)
    if not table:
        raise ValueError("No table found in HTML content")

    # Read HTML table into a DataFrame
    df = pd.read_html(str(table))[0]

    # Create a workbook and add a worksheet
    output = BytesIO()
    workbook = Workbook()
    worksheet = workbook.active

    # Write DataFrame to worksheet
    for row in dataframe_to_rows(df, index=False, header=True):
        worksheet.append(row)

    # Ensure at least one sheet is visible
    worksheet.sheet_state = 'visible'

    # Save the modified workbook
    workbook.save(output)
    output.seek(0)
    return output

@html_table_to_excel.route('/', methods=['GET'])
def index():
    return render_template('html_table_to_excel.html')

@html_table_to_excel.route('/', methods=['POST'])
def convert():
    url = request.form.get('url', '')
    table_id = request.form.get('table_id', '')

    try:
        html_content = fetch_html_content(url)
        excel_output = _html_table_to_excel(html_content, table_id,  sheet_name='converted_table')
    except Exception as e:
        error = f"Error: {str(e)}"
        return render_template('html_table_to_excel.html', error=error)

    return send_file(excel_output, download_name='converted_table.xlsx', as_attachment=True)
