# app.py
from flask import Flask, render_template, request
import openai
import textwrap
import os
from IPython.display import display, Markdown
import google.generativeai as genai

app = Flask(__name__)

# Set your OpenAI API key
api_key1 = "YOUR_API_KEY"
openai.api_key = api_key1

genai.configure(api_key="YOUR_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/road')
def road():
    return render_template('road.html')

@app.route('/road-result', methods=['POST'])
def generate_road_plan():
    subject = request.form['subject']
    
    # Define the prompt
    prompt = f"Generate roadmap for {subject} ."

    # Generate the completion
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  # Use the model that supports stream=True
        prompt=prompt,
        max_tokens=150,
    )

    # Extract and return the response
    roadmap_plan = completion.choices[0].text.strip()
    return render_template('road-result.html', result=roadmap_plan)



@app.route('/study')
def study():
    return render_template('study.html')

@app.route('/generate_study_plan', methods=['POST'])
def generate_study_plan():
    subject = request.form['subject']
    
    # Define the prompt
    prompt = f"Generate a study plan for {subject} per day."

    # Generate the completion
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  # Use the model that supports stream=True
        prompt=prompt,
        max_tokens=550,
    )

    # Extract and return the response
    study_plan = completion.choices[0].text.strip()
    
    
    return render_template('study-result.html', study_plan=study_plan)



# Route for home page with file upload form
@app.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'Note_file' not in request.files:
            return render_template('error.html', message='No file part')

        file = request.files['Note_file']

        # Check if the file is empty
        if file.filename == '':
            return render_template('error.html', message='No selected file')

        # Check if the file is of allowed type
        if file and file.filename.endswith('.txt'):
            # Read the file content
            note_text = file.read().decode('utf-8')

            # Generate summary
            summary_text = generate_summary(note_text)
            
            # Render the result template with summary
            return render_template('note-result.html', summary_text=summary_text)

        else:
            return render_template('error.html', message='Invalid file type. Please upload a text file')

    return render_template('note.html')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def generate_summary(note_text):
    model = genai.GenerativeModel('gemini-pro')
    rply = model.generate_content("summarize my notes"+note_text)
    to_markdown(rply.text)
    return rply.text

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/pay')
def pay():
    # In a real application, you would retrieve the recipient address from a database or another secure source
    recipient_address = '0x3F3329F5B4280130a09b0d8FBE330d445AbF1F67'
    return render_template('pay.html', recipient_address=recipient_address)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tutor')
def tutor():
    return render_template('tutor.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.form['question']

    # Generate response from OpenAI's GPT-3.5 model
    prompt = f"Answer for my question in short: {user_question}"
    completion = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        stop=None,
        temperature=0.7
    )
    chatgpt_response = completion.choices[0].text.strip()

    return chatgpt_response



if __name__ == '__main__':
    app.run(debug=True)
