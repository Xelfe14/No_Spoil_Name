from functions import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


PROJECT = os.getenv('GCP_PROJECT_ID')
LOCATION = os.getenv('LOCATION')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

PARAMETERS = {
        "temperature": 0.6,
        "max_output_tokens": 200,
        "top_p": .8,
        "top_k": 40,
    }

# Initialize Vertex AI (you'll have to replace this with appropriate initialization)
vertexai.init(project="le-wagon-bootcamp-392422", location="us-central1")
model = TextGenerationModel.from_pretrained("text-bison@001")

@app.get("/master_summary")
def get_master_summary(author_name, book_name, chapter_number:int):
    chapters_text = get_chapter(author_name, book_name, chapter_number)
    master_text = ' ,'.join(chapters_text)
    preprocessed_master_text = preprocess_for_lexrank(master_text)


    master_lexrank_summarized = summarize_with_lexrank(preprocessed_master_text, 2 * chapter_number)
    clean_master_lexrank_summarized = clean_extractive_summary(master_lexrank_summarized)

    # Master Summary
    master_response = model.predict(
        f"""
        Please summarize the following text: {clean_master_lexrank_summarized}
        """,
        **PARAMETERS
    )

    return {"master_sum": master_response.text}

@app.get("/chapter_summary")
def get_individual_chapter_summary(author_name, book_name, chapter_number:int):
    chapter_text = get_one_chapter(author_name, book_name, chapter_number)
    chapter_preprocessed = preprocess_for_lexrank(chapter_text)
    chapter_lexrank_summaries = summarize_with_lexrank(chapter_preprocessed, 10)
    cleaned_lexrank_summary = clean_extractive_summary(chapter_lexrank_summaries)

    response = model.predict(
        f"""
        This is a chapter from the book {book_name} by {author_name}. Please summarize the following text: {cleaned_lexrank_summary}
        """,
        **PARAMETERS
    )

    topic_dict = chapter_topic_creation(cleaned_lexrank_summary, response.text)

    # Append each chapter's summary and topics to the respective lists in big_dict
    return {"chapter_sum":response.text, "topics":topic_dict}

# print(get_individual_chapter_summary("Austen, Jane", "Emma", 2))

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}
