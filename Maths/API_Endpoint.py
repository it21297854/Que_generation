import openai
import fitz
from nltk.tokenize import sent_tokenize
import nltk
from flask import Flask, request, jsonify
import os
import AI_format as AI
nltk.download('punkt')
api_key = ""
openai.api_key = api_key

# Flask
app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Extract text
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Not able to read PDF: {e}"


# Preprocess
def preprocess_text_for_chunks(text, chunk_size=5):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]




def process_pdf_and_generate_questions(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        return "No text found in the PDF."

    text_chunks = preprocess_text_for_chunks(pdf_text)
    all_questions = []
    for i, chunk in enumerate(text_chunks):
        result = AI.generate_question_and_answers(chunk)
        all_questions.append(result)

    return all_questions


# API route
@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']


    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    questions = process_pdf_and_generate_questions(file_path)

    if isinstance(questions, str):
        return jsonify({"error": questions}), 500

    return jsonify({"questions": questions})



if __name__ == '__main__':
    app.run(debug=True)
