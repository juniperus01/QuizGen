# QuizGen
# Dynamic MCQ Generator using NLP

This is a smart and dynamic Multiple Choice Question (MCQ) generator from any uploaded text/PDF document using NLP using Natural Language Processing (NLP) techniques. 

It implements automatic question generation (AQG) techniques. Automatic question generation (AQG) is concerned with the construction of algorithms for producing questions from text.


This can be used for self-analysis, question paper generation, and evaluation, thus reducing human effort.

# Process Flow

1. Input is taken in the form of a text/PDF file that consists of English text data.
2. Text is pre-processed so it can be in a format as expected by the natural-language models. All non-alphanumeric characters(except full stops) are dropped.
3. Spacy’s NER model is used to find the named entities from the given text. These consist of people’s names, dates, places, quantities, etc.
These entities are good candidate questions and are ranked based on their TF-IDF score ( a metric used to weigh a word across multiple documents )
4. For generating incorrect options, a Word2Vec model implemented in gensim is used to find the top 10 similar entities for a given entity. We then pick the least 4 entities as alternate options. We can also pick words from the given text itself if the entity is not present in the model vocabulary.

# Demo Link
Here is a demo of the project:
https://drive.google.com/file/d/1Q1S7hwuqbp6dv7MRy5-UaFrsRTQDzzhZ/view
