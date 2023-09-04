import yake
import spacy

def chapter_topic_creation_2(text_full,summary):
    persons_list_2=[]
    places_list_2=[]
    # Running the Yake
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.1
    deduplication_algo= ['seqm']
    windowSize = 1
    numOfKeywords = 10

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(summary)

    keyword_list=[kw[0]for kw in keywords]

    # Load the pre-trained NER model
    nlp = spacy.load('en_core_web_md')

    # Process the text with spaCy's NER model
    doc = nlp(summary)

    for ent in doc.ents:
        if ent.label_== "PERSON" and ent.text not in persons_list_2:
            persons_list_2.append(f'{ent.text}')

    for token in doc:
        if token.pos_=='PROPN' and token.text not in persons_list_2:
            persons_list_2.append(token.text)


    # Apply POS on the keyword_list
    doc2 = nlp(text_full)
    for ent in doc2.ents:
        if ent.label_ in ["LOC","FAC","GPE"] and ent.text not in places_list_2:
            places_list_2.append(f'{ent.text}')


    # Creating the Dict

    topic_dict_2={}
    topic_dict_2['persons']= persons_list_2
    topic_dict_2['places']= places_list_2
    topic_dict_2['general']= keyword_list

    return topic_dict_2
