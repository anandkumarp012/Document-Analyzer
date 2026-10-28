
from chatbot import answer_question

document = """
Python is a programming language created by Guido van Rossum.
It is commonly used in automation, web development, and data science.
"""

question = "Who created Python?"

print(answer_question(question, document))
