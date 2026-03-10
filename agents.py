from phi.agent import Agent
from phi.model.ollama import Ollama

from omdb_api import fetch_movie_data
from pdf_utils import generate_pdf

# ==============================
# LLM CONFIGURATION (OLLAMA)
# ==============================
llm = Ollama(
    id="llama3",          # Must exist in `ollama list`
    temperature=0.2
)

# ==============================
# AGENT 1: MOVIE ANALYSIS AGENT
# ==============================
analysis_agent = Agent(
    name="Movie Analysis Agent",
    role="Movie Intelligence Analyst",
    goal="Answer user questions strictly using the provided movie data",
    backstory=(
        "An expert film analyst skilled at interpreting movie metadata, "
        "box office performance, critical reception, and creative contributions."
    ),
    model=llm,
    verbose=True
)

# ==============================
# AGENT 2: PDF DOCUMENT AGENT
# ==============================
pdf_agent = Agent(
    name="Movie Document Agent",
    role="PDF Report Generator",
    goal="Convert analyzed movie insights into a professional PDF document",
    backstory=(
        "A document automation specialist who formats analytical content "
        "into clean, readable, and professional reports."
    ),
    model=llm,
    verbose=True
)

# ==============================
# DATA FETCHING FUNCTION
# ==============================
def get_movie_data(title: str):
    """
    Fetch movie data from OMDb API
    """
    return fetch_movie_data(title)

# ==============================
# QUESTION ANSWERING (AGENT 1)
# ==============================
def answer_question(movie_data: dict, question: str) -> str:
    """
    Uses the Movie Analysis Agent to answer questions
    based strictly on OMDb movie data
    """

    prompt = f"""
You are provided with movie information retrieved from the OMDb API.

Movie Details:
Title: {movie_data.get('Title')}
Year: {movie_data.get('Year')}
Released: {movie_data.get('Released')}
Genre: {movie_data.get('Genre')}
Director: {movie_data.get('Director')}
Actors: {movie_data.get('Actors')}
Ratings: {movie_data.get('Ratings')}
Awards: {movie_data.get('Awards')}
Box Office Collection: {movie_data.get('BoxOffice')}
Plot: {movie_data.get('Plot')}

User Question:
{question}

Instructions:
- Answer ONLY using the given movie data
- Do NOT add external knowledge
- Respond in a single clear, well-structured paragraph
"""

    response = analysis_agent.run(prompt)

    # IMPORTANT: New PhiData returns RunResponse
    return response.content

# ==============================
# PDF GENERATION (AGENT 2)
# ==============================
def create_pdf(answer_text: str) -> str:
    """
    Converts the analysis agent's answer into a PDF
    """
    pdf_path = generate_pdf(answer_text)
    return pdf_path
