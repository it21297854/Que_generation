
import fitz
import Generate as QA

# Convert a PDF to text
def convert_pdf_to_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# format structured manner
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


# PDF
pdf_paths = ["Notes1.pdf"]
question_data = []

# Loop
for pdf_path in pdf_paths:
    print("Processing:", pdf_path)
    pdf_text = convert_pdf_to_text(pdf_path)

    # Split the text into paragraphs
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
        questions = QA.generate_question_answer(paragraph) # call from genrate

        if questions:
            # Append
            question_data.append(
                {"pdf_path": pdf_path, "question": questions[0]["question"], "options": questions[0]["options"]})
        else:
            print()

formatted_data = format_question_data(question_data)
print(formatted_data)
