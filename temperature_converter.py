# flask_app/temperature_converter.py
from flask import Blueprint, render_template, request

temperature_converter = Blueprint('temperature_converter', __name__)

def convert_temperature(temperature, conversion_type):
    if conversion_type == 'c_to_f':
        return f"{temperature}°C is {temperature * 9/5 + 32}°F"
    elif conversion_type == 'f_to_c':
        return f"{temperature}°F is {(temperature - 32) * 5/9}°C"
    else:
        return "Invalid conversion type for temperature."

@temperature_converter.route('/', methods=['GET', 'POST'])
def temperature_converter_route():
    temperature_result = None

    if request.method == 'POST':
        try:
            input_temperature = float(request.form['input_temperature'])
            temperature_conversion_type = request.form['temperature_conversion_type']
            temperature_result = convert_temperature(input_temperature, temperature_conversion_type)

        except ValueError:
            temperature_result = "Invalid input, please enter a valid temperature."

    return render_template('temperature_converter.html', temperature_result=temperature_result)
