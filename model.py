
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Small demonstration dataset
documents = [
    "Python Java machine learning software developer skills education projects",
    "Experienced software engineer resume employment experience skills",
    "Invoice number total amount payment due billing purchase",
    "Bill payment invoice subtotal tax amount due date",
    "Research paper machine learning experiment methodology results analysis",
    "Scientific study abstract introduction conclusion references",
    "The weather is nice today and the garden has beautiful flowers",
    "This document contains general information about daily activities",
]

labels = [
    "Resume",
    "Resume",
    "Invoice",
    "Invoice",
    "Research Paper",
    "Research Paper",
    "General Document",
    "General Document",
]


def train_model():
    """Train and return a text classification pipeline."""
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    model.fit(documents, labels)
    return model


# Train the model when this module is imported
model = train_model()


def predict_category(text: str) -> str:
    """Predict the category of a document."""
    if not text or not text.strip():
        raise ValueError("Document text cannot be empty.")

    return model.predict([text])[0]
