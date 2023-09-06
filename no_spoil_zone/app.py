from google.cloud import aiplatform
import vertexai
import streamlit as st
from vertexai.language_models import TextGenerationModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re
import os
import requests

nltk.download('wordnet')

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_DIR = os.path.join(PARENT_DIR, "dataset", "Gutenberg_Text-master")

def get_chapter(author_name, book_name, chapter_number):
    filepath = os.path.join(BASE_DIR, author_name, f"{book_name}.txt")
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return None

    with open(filepath, "r", encoding="utf8") as file:
        text = file.read().replace('\n', ' ').replace("\'re", " are").replace("\'d", " would").replace("\'ll", " will").replace("won't", "would not")

    case1 = re.search('\*\s+\*\s+\*\s+\*\s+\*', text)
    case2 = (len(re.findall('chapter', text, flags=re.IGNORECASE)) != 0)
    result = []

    if case1 and case2:
        matches = [match.span()[0] for match in re.finditer('chapter', text, flags=re.IGNORECASE)]
        fi_ch = sum(1 for i in range(1, len(matches)) if matches[i] - matches[i - 1] < 50)
        chapters = re.split("chapter", text, flags=re.IGNORECASE)
        result = chapters[1:chapter_number + fi_ch + 1]

    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        result = chapters[1:chapter_number + 1]

    elif case2:
        matches = [match.span()[0] for match in re.finditer('chapter', text, flags=re.IGNORECASE)]
        fi_ch = sum(1 for i in range(1, len(matches)) if matches[i] - matches[i - 1] < 50)
        chapters = re.split("chapter", text, flags=re.IGNORECASE)
        result = chapters[1:chapter_number + fi_ch + 1]

    else:
        result = [text]  # Returns the full text as a single-element list if no chapter divisions are found

    return result

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    tag = tag[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Sentence tokenization
def tokenize_sentences(text):
    return sent_tokenize(text)

# Word Tokenization and Lemmatization
def tokenize_and_lemmatize(sentence):
    words = word_tokenize(sentence.lower())  # Lowercasing
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags]
    return ' '.join(lemmatized_words)

# Main function to preprocess text for LexRank
def preprocess_for_lexrank(text):
    tokenized_sentences = tokenize_sentences(text)
    preprocessed_sentences = [tokenize_and_lemmatize(sentence) for sentence in tokenized_sentences]
    return preprocessed_sentences


def summarize_with_lexrank(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 10)  # Summarize to 2 sentences
    return ' '.join(str(sentence) for sentence in summary)

def clean_extractive_summary(text):
    # Replace improperly formatted quotes and other punctuations
    text = text.replace("`` ", '"').replace("''", '"').replace(" .", ".").replace(" ,", ",")

    # Capitalize first letter of the sentences
    sentences = re.split('([.!?] *)', text)
    sentences = [s.capitalize() for s in sentences]
    text = ''.join(sentences)

    # Grammatical corrections (Example; this may need Natural Language Processing for robustness)
    text = text.replace("N't", "n't")

    # Remove any additional white spaces
    text = ' '.join(text.split())

    return text


def main():
    st.title("💯 No Sploil Zone! 💯")

    # User input
    author_name = st.selectbox("Select Author", ["Austen, Jane", "Shakespeare, William", "Twain, Mark"])
    book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
    chapter_number = st.number_input("Enter Chapter Number:", min_value=1, value=1)

    if st.button("Run Summarization"):
        try:
            st.write("Running! No sploils here 😉")
            chapters_text = get_chapter(author_name, book_name, chapter_number)
            # st.write(f"Returned from get_chapter, got {len(chapters_text) if chapters_text else 0} chapters.")

            if chapters_text is None:
                # st.write("No chapters_text. Exiting.")
                return

            # st.write("Initializing Vertex AI...")
            vertexai.init(project="le-wagon-bootcamp-392422", location="us-central1")

            model = TextGenerationModel.from_pretrained("text-bison@001")
            parameters = {
                "temperature": 0.6,
                "max_output_tokens": 200,
                "top_p": .8,
                "top_k": 40,
            }

            for i, chapter_text in enumerate(chapters_text, start=1):
                # st.write(f"Processing chapter {i}...")

                # Preprocessing and summarizing chapter
                chapter_preprocessed = preprocess_for_lexrank(chapter_text)
                lexrank_summarized_text = summarize_with_lexrank(chapter_preprocessed)
                cleaned_lexrank_summary = clean_extractive_summary(lexrank_summarized_text)

                # Further summarization with Vertex AI
                response = model.predict(
                    f"""
                    This is a chapter from the book {book_name} by {author_name}. Please summarize the following text: {cleaned_lexrank_summary}
                    """,
                    **parameters
                )

                # st.write(f"===== LexRank Summary for Chapter {i} =====")
                # st.write(cleaned_lexrank_summary)
                st.markdown(f"===== Summary for Chapter {i} =====")
                st.markdown(response.text)

        except Exception as e:
            st.write(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
