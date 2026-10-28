
import streamlit as st
import requests
from chatbot import answer_question

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Document Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI-Powered Document Analyzer")
st.write("Upload a PDF or TXT document to analyze its content.")

# Store the current document and analysis in Streamlit session state.
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "txt"],
)

if st.button("Analyze Document", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload a PDF or TXT file first.")
    else:
        try:
            with st.spinner("Analyzing document..."):
                response = requests.post(
                    f"{API_URL}/documents/analyze",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                            or "application/octet-stream",
                        )
                    },
                    timeout=120,
                )

            if response.ok:
                result = response.json()
                st.session_state.analysis_result = result

                # Extract text locally for the chatbot.
                file_bytes = uploaded_file.getvalue()

                if uploaded_file.name.lower().endswith(".pdf"):
                    from document_utils import extract_text_from_pdf
                    document_text = extract_text_from_pdf(file_bytes)
                else:
                    from document_utils import extract_text_from_txt
                    document_text = extract_text_from_txt(file_bytes)

                st.session_state.document_text = document_text
                st.session_state.chat_messages = []

                st.success("Document analyzed successfully!")

            else:
                try:
                    detail = response.json().get(
                        "detail", "Analysis failed."
                    )
                except ValueError:
                    detail = "Analysis failed."

                st.error(f"Error ({response.status_code}): {detail}")

        except requests.RequestException:
            st.error(
                "Could not connect to the API. "
                "Make sure FastAPI is running."
            )
        except Exception as exc:
            st.error(f"Document processing failed: {exc}")

# Display the most recent analysis.
result = st.session_state.analysis_result

if result:
    col1, col2 = st.columns(2)
    col1.metric("Analysis ID", result["id"])
    col2.metric("Characters", result["character_count"])

    st.subheader("Predicted Category")
    st.info(result["category"])

    st.subheader("Summary")
    st.write(result["summary"])

    st.subheader("Keywords")
    st.write(", ".join(result["keywords"]))

    st.caption(
        f"Filename: {result['filename']} | "
        f"Analyzed: {result['created_at']}"
    )

# Gemini document chatbot.
st.divider()
st.subheader("💬 Ask Questions About Your Document")

if st.session_state.document_text:
    st.write(
        "Ask questions in your own words about the document you analyzed."
    )

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about your document...")

    if question:
        st.session_state.chat_messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = answer_question(
                    question,
                    st.session_state.document_text,
                )
            st.markdown(answer)

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": answer}
        )
else:
    st.info("Analyze a document first to start chatting.")

st.divider()
st.subheader("📚 Analysis History")

if st.button("Refresh History"):
    try:
        response = requests.get(
            f"{API_URL}/documents/history",
            timeout=15,
        )
        response.raise_for_status()
        history = response.json()

        if history:
            st.dataframe(
                [
                    {
                        "ID": item["id"],
                        "Filename": item["filename"],
                        "Category": item["category"],
                        "Characters": item["character_count"],
                        "Created At": item["created_at"],
                    }
                    for item in history
                ],
                use_container_width=True,
            )
        else:
            st.info("No analyses found yet.")

    except requests.RequestException:
        st.error(
            "Could not retrieve history. "
            "Make sure FastAPI is running."
        )