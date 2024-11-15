import os
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
from workers import file2text, store_extracted_text_in_db, txt2questions

# Init an app object
app = Flask(__name__)

# Set secret key for session management
app.secret_key = os.urandom(24)  # Use a random key for development, replace it with a fixed key in production.

@app.route('/')
def index():
    """ The landing page for the app """
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """ Handle upload and conversion of file + other stuff """

    UPLOAD_STATUS = False
    questions = dict()

    if request.method == 'POST':
        try:
            # Retrieve file from request
            uploaded_file = request.files['file']
            filename, file_exten = os.path.splitext(uploaded_file.filename)
            file_exten = file_exten[1:].lower()

            # Get contents of file
            uploaded_content = file2text(uploaded_file, file_exten)

            # Save contents in database
            is_stored = store_extracted_text_in_db(filename, file_exten, uploaded_content)

            # Convert the text into questions
            questions = txt2questions(uploaded_content)
            questions_cnt = len(questions)

            # Store questions count in session
            session['questions_cnt'] = questions_cnt

            # File upload + convert success
            if uploaded_content is not None and is_stored:
                UPLOAD_STATUS = True
        except Exception as e:
            print(e)

    return render_template(
        'quiz.html',
        uploaded=UPLOAD_STATUS,
        questions=questions,
        size=session.get('questions_cnt', 0))  # Get the count of questions from session


@app.route('/result', methods=['POST', 'GET'])
def result():
    correct_q = 0
    for k, v in request.form.items():
        correct_q += 1
    
    # Get the questions count from the session
    questions_cnt = session.get('questions_cnt', 0)

    return render_template('result.html', total=questions_cnt, correct=correct_q)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
