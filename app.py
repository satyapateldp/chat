from transformers import pipeline
from flask import Flask, request, jsonify, render_template
import PyPDF2
import os

# Initialize the question-answering pipeline with the model
try:
    qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    print("QA pipeline initialized successfully.")
except Exception as e:
    print(f"Error initializing QA pipeline: {e}")
    qa_pipeline = None

app = Flask(__name__)

def extract_text_from_pdf(file):
    try:
        print("Starting PDF text extraction...")
        reader = PyPDF2.PdfReader(file)
        text = ""
        num_pages = len(reader.pages)
        print(f"PDF loaded successfully with {num_pages} pages.")
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                print(f"Extracted text from page {page_num}: {page_text[:100]}...")  # Print first 100 characters
                text += page_text
            else:
                print(f"No text found on page {page_num}.")
        print("Completed PDF text extraction.")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

@app.route('/ask', methods=['POST'])
def ask_question():
    if not qa_pipeline:
        return jsonify({'error': 'QA pipeline not initialized'}), 500

    data = request.form
    question = data['question']
    pdf_file = request.files.get('pdf_file')

    if not pdf_file:
        return jsonify({'error': 'No PDF file uploaded'}), 400

    pdf_text = extract_text_from_pdf(pdf_file)
    if pdf_text is None:
        return jsonify({'error': 'Failed to extract text from PDF'}), 500

    try:
        result = qa_pipeline(question=question, context=pdf_text)
        answer = result['answer']
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"Error processing QA pipeline: {e}")
        return jsonify({'error': 'Error processing question'}), 500

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return "Error loading the page", 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask server: {e}")
