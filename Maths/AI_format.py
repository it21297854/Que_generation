import openai

# LLM
def generate_question_and_answers(text_chunk):
    prompt = f"""
    Based on the following content:
    {text_chunk}
    Generate 3 multiple-choice questions with 4 answer options each. Format the response as:
    Question 1: <Your generated question>
    Answer Options:
    A. <Option A>
    B. <Option B>
    C. <Option C>
    D. <Option D>
    Correct Answer: <Correct Option>

    Question 2: ...
    Question 3: ...

    (for some question make calculation questions and answers also)
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Not able to  generate questions: {e}"