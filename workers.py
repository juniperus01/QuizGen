from PyPDF2 import PdfReader
import mysql.connector
from question_generation_main import QuestionGeneration

# Constants
DB_CONFIG = {
    'host': '0.0.0.0',
    'user': 'root',
    'password': 'password',
    'database': 'quizgen_text_data'
}


def file2text(file, file_exten: str) -> str:
    """ Converts a given file to text content """
    
    _content = ''

    # Identify file type and get its contents
    if file_exten == 'pdf':
        # Read the PDF content from the file object
        _pdf_reader = PdfReader(file)
        for p in range(len(_pdf_reader.pages)):
            _content += _pdf_reader.pages[p].extract_text()
        print('PDF operation done!')

    elif file_exten == 'txt':
        # Read the content from the .txt file object
        _content = file.read().decode('utf-8')  # Assuming UTF-8 encoding
        print('TXT operation done!')

    return _content


def store_extracted_text_in_db(title, file_type, content):
    """ Store extracted text in MySQL database """
    try:
        # Establish database connection
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insert or update the document content
        sql = """
        INSERT INTO documents (title, file_type, content)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE content = VALUES(content), file_type = VALUES(file_type)
        """
        cursor.execute(sql, (title, file_type, content))
        connection.commit()
        return True

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()


def txt2questions(doc: str, n=5, o=4) -> dict:
    """ Get all questions and options """

    qGen = QuestionGeneration(n, o)
    q = qGen.generate_questions_dict(doc)
    for i in range(len(q)):
        temp = []
        for j in range(len(q[i + 1]['options'])):
            temp.append(q[i + 1]['options'][j + 1])
        print(temp)
        q[i + 1]['options'] = temp
    return q
