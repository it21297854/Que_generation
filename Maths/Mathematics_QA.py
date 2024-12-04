import openai
import fitz
from nltk.tokenize import sent_tokenize
import nltk
import AI_format as AI


# NLTK resources
nltk.download('punkt')

# OpenAI API key
#api_key = ""
openai.api_key = api_key

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

# generating multiple questions
def preprocess_text_for_chunks(text, chunk_size=5):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]


# Process PDF
def process_pdf_and_generate_questions(pdf_path):
    print(f"Processing: {pdf_path}")

    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        print("No text.")
        return

    text_chunks = preprocess_text_for_chunks(pdf_text)

    for i, chunk in enumerate(text_chunks):
        print(f"\nProcessing Chunk {i+1}/{len(text_chunks)}...")
        result = AI.generate_question_and_answers(chunk)
        print(f"\nGenerated Questions for Chunk {i+1}:\n{result}\n")

#  PDF path
pdf_path = "Notes01.pdf"

# Process
process_pdf_and_generate_questions(pdf_path)
