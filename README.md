# QR Code Link Extractor

This project provides a simple web application that extracts QR code links from uploaded PDF or image files. The extracted links are displayed on a separate page and can be opened directly in the browser.

## Features

- Upload PDF or image files to extract QR code links.
- Display extracted links on a separate page.
- Automatically open valid links in the browser.

## Technologies Used

- Backend: Flask, PyMuPDF, pyzbar, Pillow, requests
- Frontend: React, Axios, React Router

## Installation

### Backend

1. Clone the repository:
    git clone <repository-url>
    cd <repository-directory>

2. Set up a virtual environment and activate it:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app:
    ```bash
    python app.py
    ```

### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd qr-link-extractor
    ```

2. Install the required packages:
    ```bash
    npm install
    ```

3. Start the React app:
    ```bash
    npm start
    ```

## Usage

1. Open the React app in your browser (usually at `http://localhost:3000`).

2. Upload a PDF or image file using the upload form.

3. Click the "Find Links" button to extract QR code links from the uploaded file.

4. The extracted links will be displayed on a separate page, categorized into successfully opened links and failed links.
