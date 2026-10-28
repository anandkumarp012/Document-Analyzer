
from document_utils import (
    extract_text_from_txt,
    generate_summary,
    extract_keywords,
)


def test_txt_extraction():
    text = extract_text_from_txt(
        b"Machine learning analyzes documents. Python is useful."
    )
    assert "Machine learning" in text


def test_empty_txt():
    try:
        extract_text_from_txt(b"   ")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_summary():
    text = (
        "Python processes documents. "
        "Machine learning predicts categories. "
        "FastAPI creates endpoints."
    )
    summary = generate_summary(text)
    assert "Python processes documents." in summary


def test_keywords():
    keywords = extract_keywords(
        "Python Python machine learning documents documents"
    )
    assert "python" in keywords
    assert "documents" in keywords


if __name__ == "__main__":
    test_txt_extraction()
    test_empty_txt()
    test_summary()
    test_keywords()
    print("All document processing tests passed!")
