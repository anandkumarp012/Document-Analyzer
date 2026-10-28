# AI-Powered Document Analyzer

An AI-powered web application that analyzes PDF and TXT documents, classifies document categories, extracts summaries and keywords, and answers user questions using the Google Gemini API.

## Features

- **Document Upload:** Upload PDF and TXT files through a Streamlit interface.
- **Text Extraction:** Extract text from uploaded documents using PyMuPDF.
- **Document Classification:** Predict document categories using a TF-IDF and Logistic Regression model.
- **Text Summarization:** Generate a basic extractive summary from document text.
- **Keyword Extraction:** Identify important words from the document.
- **AI Chatbot:** Ask natural-language questions about the uploaded document using Google Gemini.
- **REST API:** Process document analysis requests using FastAPI.
- **Database Persistence:** Store analysis records in SQLite using SQLAlchemy.
- **Analysis History:** View previously analyzed documents.
- **Input Validation:** Handle unsupported file types and invalid uploads.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Chatbot | Google Gemini API |
| Machine Learning | Scikit-learn |
| Text Processing | TF-IDF |
| PDF Processing | PyMuPDF |
| Database | SQLite |
| ORM | SQLAlchemy |
| Testing | Pytest |

## Project Structure

```text
docs-analyzer/
├── app.py
├── main.py
├── chatbot.py
├── model.py
├── document_utils.py
├── database.py
├── test_model.py
├── test_document_utils.py
├── test_chatbot.py
├── requirements.txt
├── .env
├── .gitignore
└── documents.db
```

The structure above lists the main project files; additional files may exist in the repository.

## Prerequisites

- Python 3.11 or a compatible Python version
- pip
- Google Gemini API key
- Internet connection for Gemini API requests

## Installation

Clone the repository or open the project directory.

Create and activate a virtual environment on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

If necessary, install the Gemini SDK and environment-variable loader:

```powershell
pip install google-genai python-dotenv
```

## Environment Configuration

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Replace the placeholder with your own API key from [Google AI Studio](https://aistudio.google.com/).

**Security:** Never commit `.env` or expose your API key publicly.

## Run the Application

Open two terminals in the project directory.

**Terminal 1 — Start the FastAPI backend**

```powershell
python -m uvicorn main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

**Terminal 2 — Start the Streamlit frontend**

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

## How It Works

1. The user uploads a PDF or TXT document.
2. The application extracts the document text.
3. The machine-learning model predicts a document category.
4. The application generates a basic summary and extracts keywords.
5. The analysis result is saved in the SQLite database.
6. The user can ask questions about the uploaded document through the Gemini-powered chatbot.
7. The user can view previous analyses through the history interface.

## Database

The application uses SQLite to store document analysis records.

Database file:

```text
documents.db
```

The database can be inspected using [DB Browser for SQLite](https://sqlitebrowser.org/).

## Testing

Run the existing model and document-processing tests:

```powershell
python test_model.py
python test_document_utils.py
```

Test the Gemini chatbot separately:

```powershell
python test_chatbot.py
```

The chatbot test makes a real API request and requires a valid API key, internet connectivity, and available API quota.

## Limitations

- The document classification model was trained on a small demonstration dataset and requires more representative training data for reliable predictions.
- The summary and keyword extraction methods are basic and may not capture every important detail.
- Chatbot answers depend on the text supplied as context and may occasionally be inaccurate.
- Gemini API usage is subject to the provider's quotas, availability, and pricing policies.
- The current database is local SQLite storage; production deployment may require a managed database and persistent storage.

## Future Enhancements

- Train and evaluate the classifier using a larger labeled dataset.
- Improve summarization and keyword extraction.
- Add persistent conversation history.
- Add document search, filtering, and deletion.
- Introduce user authentication and access controls.
- Deploy the application to a cloud platform.

## Project Purpose

This project demonstrates practical skills in Python development, machine learning, document processing, REST API development, database integration, and generative AI integration.
