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
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

PROJECT = os.getenv('GCP_PROJECT_ID')
LOCATION = os.getenv('LOCATION')


def get_chapter(author_name, book_name, chapter_number):
    filepath = os.path.join("DEMO_DATASET", author_name, f"{book_name}.txt")
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

def get_one_chapter(author_name, book_name, chapter_number):
    filepath = os.path.join("DEMO_DATASET", author_name, f"{book_name}.txt")
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
        result = chapters[chapter_number + fi_ch + 1]

    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        result = chapters[chapter_number + 1]

    elif case2:
        matches = [match.span()[0] for match in re.finditer('chapter', text, flags=re.IGNORECASE)]
        fi_ch = sum(1 for i in range(1, len(matches)) if matches[i] - matches[i - 1] < 50)
        chapters = re.split("chapter", text, flags=re.IGNORECASE)
        result = chapters[chapter_number + fi_ch + 1]

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

    # Load the pre-trained NER model
    nlp = spacy.load('en_core_web_md')

    # Process the text with spaCy's NER model
    doc = nlp(final_summary)

    for ent in doc.ents:
        if ent.label_== "PERSON" and ent.text not in persons_list_2:
            persons_list_2.append(f'{ent.text}')

    # Apply POS on the keyword_list
    doc2 = nlp(extractive_summary)
    for ent in doc2.ents:
        if ent.label_ in ["LOC","FAC","GPE"] and ent.text not in places_list_2:
            places_list_2.append(f'{ent.text}')

    # Running the Yake
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.2
    deduplication_algo= 'seqm'
    windowSize = 1
    numOfKeywords = 10

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(final_summary)

    keyword_list=[kw[0]for kw in keywords if kw[0] not in persons_list_2 and places_list_2]


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


# print(get_chapter("Jane Austen", "Emma", 2))
