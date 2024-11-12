'''This module ties together the
questions generation and incorrect answer
generation modules
'''
from question_extraction import QuestionExtractor
from incorrect_answer_generation import IncorrectAnswerGenerator
import re
from nltk import sent_tokenize


class QuestionGeneration:
    '''This class contains the method
    to generate questions
    '''

    def __init__(self, num_questions, num_options):
        self.num_questions = num_questions
        self.num_options = num_options
        self.question_extractor = QuestionExtractor(num_questions)

    import re

    def clean_text(self, text):
        text = text.replace('\n', ' ')  # remove newline chars
        sentences = sent_tokenize(text)
        cleaned_text = ""
        for sentence in sentences:
            # remove non-alphanumeric chars
            cleaned_sentence = re.sub(r'([^\s\w]|_)+', '', sentence)

            # substitute multiple spaces with a single space
            cleaned_sentence = re.sub(' +', ' ', cleaned_sentence)
            
            # Append a period if the cleaned sentence does not end with one
            if cleaned_sentence and cleaned_sentence[-1] != '.':
                cleaned_sentence += '.'
            
            cleaned_text += cleaned_sentence + ' '  # Add space after each sentence

        # Trim any trailing space at the end
        return cleaned_text.strip()

    def generate_questions_dict(self, document):
        document = self.clean_text(document)
        self.questions_dict = self.question_extractor.get_questions_dict(
            document)
        self.incorrect_answer_generator = IncorrectAnswerGenerator(document)

        for i in range(1, self.num_questions + 1):
            if i not in self.questions_dict:
                continue
            self.questions_dict[i]["options"] \
                = self.incorrect_answer_generator.get_all_options_dict(
                self.questions_dict[i]["answer"],
                self.num_options
            )

        return self.questions_dict
