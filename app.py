import streamlit as st
from agents import get_movie_data, answer_question, create_pdf

st.set_page_config(page_title="Movie Intelligence System", layout="wide")

st.title("🎬 Movie Intelligence System")

# -------- Step 1: Movie Input --------
movie_title = st.text_input("Enter Movie Title")

if st.button("Fetch Movie Data"):
    try:
        data = get_movie_data(movie_title)
        st.session_state["movie_data"] = data
        st.success("Movie data fetched successfully")
        st.json(data)
    except Exception as e:
        st.error(str(e))

# -------- Step 2: Ask Questions --------
if "movie_data" in st.session_state:
    question = st.text_input("Ask a question about the movie")

    if st.button("Get Answer"):
        with st.spinner("Analyzing using Llama3..."):
            answer = answer_question(
                st.session_state["movie_data"],
                question
            )

            st.subheader("Answer")
            st.write(answer)

            pdf_path = create_pdf(answer)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF Report",
                    f,
                    file_name="movie_report.pdf"
                )
