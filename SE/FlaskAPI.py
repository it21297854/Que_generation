from flask import Flask, request, jsonify
import fitz
import os
import Generate as QA
app = Flask(__name__)


def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text



def format_question_data(question_data):
    formatted_output = ""

    for item in question_data:
        if "message" in item:
            formatted_output += f"PDF: {item['pdf_path']}\nMessage: {item['message']}\n\n"
        else:
            formatted_output += f"Question: {item['question']}\n"
            formatted_output += "Options:\n"
            for idx, option in enumerate(item['options'], 1):
                formatted_output += f"  {idx}. {option}\n"
            formatted_output += "\n"

    return formatted_output


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        file_path = os.path.join("uploads", pdf_file.filename)
        pdf_file.save(file_path)
        return jsonify({'message': 'PDF file uploaded successfully', 'file_path': file_path}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    data = request.get_json()
    if not data or 'pdf_paths' not in data:
        return jsonify({'error': 'PDF paths are required'}), 400

    pdf_paths = data['pdf_paths']
    question_data = []

    for pdf_path in pdf_paths:
        try:
            print("Processing:", pdf_path)
            pdf_text = convert_pdf_to_text(pdf_path)


            doc = fitz.open(pdf_path)
            extracted_paragraphs = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                paragraphs = page_text.split("\n \n")
                extracted_paragraphs.extend(paragraphs)
            doc.close()

            # Generate questions
            for paragraph in extracted_paragraphs:
                questions = QA.generate_question_answer(paragraph)

                if questions:
                    # Append
                    question_data.append(
                        {"pdf_path": pdf_path, "question": questions[0]["question"], "options": questions[0]["options"]}
                    )
                else:
                    question_data.append(
                        {"pdf_path": pdf_path, "message": "No questions generated for this paragraph."})

        except Exception as e:
            return jsonify({'error': f"Error processing {pdf_path}: {str(e)}"}), 500


    formatted_data = format_question_data(question_data)
    return jsonify({'formatted_data': formatted_data}), 200


if __name__ == '__main__':

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)
