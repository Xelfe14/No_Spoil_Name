from google.cloud import aiplatform
import vertexai
import streamlit as st
import spacy
import yake
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


nltk.download('wordnet')

PROJECT = os.getenv('PROJECT')
LOCATION = os.getenv('LOCATION')


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

# Topic Creation
def chapter_topic_creation(extractive_summary,final_summary):
    persons_list_2=[]
    places_list_2=[]

    # Running the Yake
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.15
    deduplication_algo= 'seqm'
    windowSize = 1
    numOfKeywords = 10

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(final_summary)

    keyword_list=[kw[0]for kw in keywords]

    # Load the pre-trained NER model
    nlp = spacy.load('en_core_web_md')

    # Process the text with spaCy's NER model
    doc = nlp(final_summary)

    for ent in doc.ents:
        if ent.label_== "PERSON" and ent.text not in persons_list_2:
            persons_list_2.append(f'{ent.text}')

    # for token in doc:
    #     if token.pos_=='PROPN' and token.text not in persons_list_2:
    #         persons_list_2.append(token.text)


    # Apply POS on the keyword_list
    doc2 = nlp(extractive_summary)
    for ent in doc2.ents:
        if ent.label_ in ["LOC","FAC","GPE"] and ent.text not in places_list_2:
            places_list_2.append(f'{ent.text}')


    # Creating the Dict

    topic_dict_2={}
    topic_dict_2['persons']= persons_list_2
    topic_dict_2['places']= places_list_2
    topic_dict_2['general']= keyword_list

    return topic_dict_2

# Main function to preprocess text for LexRank
def preprocess_for_lexrank(text):
    tokenized_sentences = tokenize_sentences(text)
    preprocessed_sentences = [tokenize_and_lemmatize(sentence) for sentence in tokenized_sentences]
    return preprocessed_sentences


def summarize_with_lexrank(text, summary_size):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, summary_size)  # Summarize to 2 sentences
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


# Your additional imports like Vertex AI, LexRank, etc. go here.

def main():
    st.markdown(
        "<h1 style='text-align: center; color: white;'>💯 No Sploil Zone! 💯</h1>",
        unsafe_allow_html=True
    )

    st.markdown("### 📚 Choose a Book and Discover Its Summary and Topics 📚")
    st.markdown("---")

    # Layout Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        author_name = st.selectbox("Select Author", ["Austen, Jane", "Shakespeare, William", "Twain, Mark"])
    with col2:
        book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
    with col3:
        chapter_number = st.number_input("Enter Chapter Number:", min_value=1, value=1)

    st.markdown("---")

    if st.button("Run Summarization 🚀"):
        with st.spinner('Running! No sploils here 😉'):
            try:
                chapters_text = get_chapter(author_name, book_name, chapter_number)
                if chapters_text is None:
                    st.error("No chapter data found.")
                    return

                master_chapter_text = ' ,'.join(chapters_text)
                master_lexrank_summarized = summarize_with_lexrank(master_chapter_text, 3 * chapter_number)

                # Initialize Vertex AI
                vertexai.init(project=PROJECT, location="us-central1")
                model = TextGenerationModel.from_pretrained("text-bison@001")
                parameters = {
                    "temperature": 0.6,
                    "max_output_tokens": 200,
                    "top_p": .8,
                    "top_k": 40,
                }

                # Master Summary
                master_response = model.predict(
                    f"""
                    Please summarize the following text: {master_lexrank_summarized}
                    """,
                    **parameters
                )

                if chapter_number == 1:
                    st.subheader(f"🤔💭 What happens in the first chapter of {book_name}?")
                else:
                    st.subheader(f"🤔💭 What happens in the first {chapter_number} chapters of {book_name}?")
                st.markdown(master_response.text)

                st.markdown("---")

                # Precompute LexRank summaries for all chapters
                precomputed_lexrank_summaries = []
                for chapter_text in chapters_text:
                    chapter_preprocessed = preprocess_for_lexrank(chapter_text)
                    lexrank_summarized_text = summarize_with_lexrank(chapter_preprocessed, 10)
                    precomputed_lexrank_summaries.append(lexrank_summarized_text)

                # Loop through the individual chapters
                for i, (chapter_text, lexrank_summarized_text) in enumerate(zip(chapters_text, precomputed_lexrank_summaries), start=1):
                    cleaned_lexrank_summary = clean_extractive_summary(lexrank_summarized_text)

                    response = model.predict(
                        f"""
                        This is a chapter from the book {book_name} by {author_name}. Please summarize the following text: {cleaned_lexrank_summary}
                        """,
                        **parameters
                    )

                    topic_dict = chapter_topic_creation(lexrank_summarized_text, response.text)

                    st.markdown(f"### Topics for Chapter {i}")
                    st.write(f"**People**: {', '.join(topic_dict['persons'])}")
                    st.write(f"**Places**: {', '.join(topic_dict['places'])}")
                    st.write(f"**General**: {', '.join(topic_dict['general'])}")

                    st.markdown(f"### Summary for Chapter {i}")
                    st.markdown(response.text)

                    st.markdown("---")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
