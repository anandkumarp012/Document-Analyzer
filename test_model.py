
from model import predict_category


def test_empty_text():
    try:
        predict_category("")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_category_prediction():
    result = predict_category(
        "Python developer skills education work experience projects"
    )
    assert result in [
        "Resume",
        "Invoice",
        "Research Paper",
        "General Document",
    ]


if __name__ == "__main__":
    test_empty_text()
    test_category_prediction()
    print("All basic model tests passed!")
