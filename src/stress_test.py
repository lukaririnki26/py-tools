from flask import Blueprint, request, render_template
import requests
from concurrent.futures import ThreadPoolExecutor

stress_test = Blueprint('stress_test', __name__)

# Function to make a GET request to the API
def make_get_request(url, headers):
    response = requests.get(url, headers=headers)
    print(response.json())

# Function to make a POST request to the API
def make_post_request(url, headers, data):
    response = requests.post(url, json=data, headers=headers)
    print(response.json())

# Function to run stresstest with ThreadPoolExecutor
def run_stresstest(method, url, headers, data, workers, request_range):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        if method == 'GET':
            executor.map(make_get_request, [url] * request_range, [headers] * request_range)
        elif method == 'POST':
            executor.map(make_post_request, [url] * request_range, [headers] * request_range, [data] * request_range)

# Endpoint to render the stresstest form
@stress_test.route('/', methods=['GET', 'POST'])
def stresstest_form():
    if request.method == 'POST':
        method = request.form.get('method')
        url = request.form.get('url')
        headers = request.form.get('headers')
        data = request.form.get('data')
        workers = int(request.form.get('workers'))
        request_range = int(request.form.get('range'))

        headers_dict = {}
        if headers:
            headers_dict = json.loads(headers)

        data_dict = {}
        if data:
            data_dict = json.loads(data)

        run_stresstest(method, url, headers_dict, data_dict, workers, request_range)

    return render_template('stress_test.html')
