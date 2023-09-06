from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re


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
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(sentence.lower())  # Lowercasing
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags]
    return ' '.join(lemmatized_words)


# Main function to preprocess text for LexRank
def preprocess_for_lexrank(text):
    tokenized_sentences = tokenize_sentences(text)
    preprocessed_sentences = [tokenize_and_lemmatize(sentence) for sentence in tokenized_sentences]
    return preprocessed_sentences


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
