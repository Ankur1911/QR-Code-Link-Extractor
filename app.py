from flask import Flask, request, jsonify ,send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
from pyzbar.pyzbar import decode
from PIL import Image
import webbrowser
import requests
import logging
import warnings
from bs4 import BeautifulSoup
import pytesseract
import io

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_qr_from_image(image):
    decoded_objects = decode(image)
    qr_links = [obj.data.decode('utf-8') for obj in decoded_objects if obj.type == 'QRCODE']
    return qr_links

def extract_qr_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    qr_links = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        qr_links.extend(extract_qr_from_image(img))

    return qr_links

def open_urls_in_browser(urls):
    opened_links = []
    failed_links = []
    for url in urls:
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                logging.info(f"Opening URL: {url}")
                webbrowser.open(url)
                opened_links.append(url)
            else:
                logging.warning(f"URL not accessible: {url} (status code: {response.status_code})")
                failed_links.append(url)
        except requests.RequestException as e:
            logging.warning(f"Failed to open URL: {url} ({e})")
            failed_links.append(url)
    return opened_links,failed_links        

@app.route('/extract-qr', methods=['POST'])
def extract_qr():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        if filename.lower().endswith('.pdf'):
            qr_links = extract_qr_from_pdf(file_path)
        else:
            image = Image.open(file_path)
            qr_links = extract_qr_from_image(image)

        opened_links,failed_links=open_urls_in_browser(qr_links)
        return jsonify({
            "qr_links": qr_links,
            "opened_links": opened_links,
            "failed_links": failed_links
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

def get_extension_from_content_type(content_type):
    if 'application/pdf' in content_type:
        return '.pdf'
    elif 'image' in content_type:
        if 'jpeg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'bmp' in content_type:
            return '.bmp'
        elif 'tiff' in content_type:
            return '.tiff'
    return None

def perform_ocr_on_image(image_content):
    image = Image.open(io.BytesIO(image_content))
    text = pytesseract.image_to_string(image)
    return text

def perform_ocr_on_pdf(pdf_content):
    document = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)
    return text

@app.route('/process-link', methods=['POST'])
def process_link():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url, stream=True, verify=False)
        content_type = response.headers.get('Content-Type', '').lower()

        # Save the file locally
        extension = get_extension_from_content_type(content_type)
        file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(url.split('/')[-1] + (extension or '')))
        with open(file_name, 'wb') as f:
            f.write(response.content)

        # Perform web scraping
        soup = BeautifulSoup(response.content, 'lxml')
        web_text = soup.get_text()

        # Perform OCR
        ocr_text = ""
        if extension:
            if 'image' in content_type:
                ocr_text = perform_ocr_on_image(response.content)
            elif 'application/pdf' in content_type or file_name.lower().endswith('.pdf'):
                with open(file_name, 'rb') as f:
                    ocr_text = perform_ocr_on_pdf(f.read())

        combined_text = web_text + "\n" + ocr_text
        return jsonify({"content": combined_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
