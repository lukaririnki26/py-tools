from flask import Blueprint, render_template, request, send_file, make_response
import pdfkit
import requests

html_to_pdf = Blueprint('html_to_pdf', __name__)

# Configure pdfkit options
pdfkit_options = {
    'no-images': None,
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
}

@html_to_pdf.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        scale = request.form.get('scale', '1.0')
        paper_size = request.form.get('paper_size', 'A4')
        layout = request.form.get('layout', 'portrait')

        # Update pdfkit_options with user-defined options
        pdfkit_options.update({
            'zoom': float(scale),
            'page-size': paper_size,
            'orientation': layout,
        })

        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text

            pdf = pdfkit.from_string(html_content, False, options=pdfkit_options)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'
            return response
        except requests.exceptions.RequestException as e:
            error = f"Error: {str(e)}"
            return render_template('html_to_pdf.html', error=error)

    return render_template('html_to_pdf.html')
