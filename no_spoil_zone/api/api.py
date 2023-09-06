import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import get_chapter(), get_wordnet_pos(), tokenize_sentences(), tokenize_and_lemmatize(), chapter_topic_creation(), preprocess_for_lexrank(), summarize_with_lexrank(), clean_extractive_summary(), main()
# from bison import get_chapter, preprocess_text, split_text_into_chunks, main
# from your_module import predict_function1, predict_function2

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all  headers
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sumary")
def create_sumary(author_name, book_name, chapter_number):
    summary = thesuperfunc(author_name, book_name, chapter_number)
    return summary





def thesuperfunc(author_name, book_name, chapter_number):
    thesummaryfunc
    thetopicsfunc

    return dict
