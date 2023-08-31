from transformers import pipeline
from nltk.tokenize import sent_tokenize
import pandas as pd
from datasets import load_metric
import time
import re
import os

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
BASE_DIR = os.path.join(PARENT_DIR, "dataset", "Gutenberg_Text-master")


def get_chapter(author_name, book_name, chapter_number):
    filepath = os.path.join(BASE_DIR, author_name, f"{book_name}.txt")

    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return None

    with open(filepath, "r", encoding="utf8") as file:
        text = file.read()
        text = text.replace('\n', ' ')

    case1 = re.search('\*\s+\*\s+\*\s+\*\s+\*', text)
    case2 = (len(re.findall('chapter', text, flags=re.IGNORECASE)) != 0)

    if case1 and case2:
        matches = [match.span()[0] for match in re.finditer('chapter', text, flags=re.IGNORECASE)]
        fi_ch = 0
        for i in range(1, len(matches)):
            if matches[i] - matches[i-1] < 50:
                fi_ch += 1
        chapters = re.split("chapter", text, flags=re.IGNORECASE)
        num = chapter_number
        return ''.join(chapters[1:num+fi_ch])

    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        return ''.join(chapters[1:chapter_number])

    elif case2:
        matches = [match.span()[0] for match in re.finditer('chapter', text, flags=re.IGNORECASE)]
        fi_ch = 0
        for i in range(1, len(matches)):
            if matches[i] - matches[i-1] < 50:
                fi_ch += 1
        chapters = re.split("chapter", text, flags=re.IGNORECASE)
        return ''.join(chapters[1:chapter_number+fi_ch])

    else:
        return None

def generate_summary(selected_text, model, task='summarization'):
    pipe = pipeline(task, model=model)
    tokenized_sentences = sent_tokenize(selected_text)

    summarized_text = ""
    chunk = ""
    MAX_CHUNK_SIZE = 400  # Choose a size that you know is safe for your model

    for sentence in tokenized_sentences:
        if len(chunk) + len(sentence) < MAX_CHUNK_SIZE:
            chunk += " " + sentence
        else:
            # summarize the chunk and add it to the final summary
            summarized_chunk = pipe(chunk)
            summarized_text += " " + summarized_chunk[0]['summary_text']
            chunk = sentence

    # Don't forget to summarize the last chunk
    if chunk:
        summarized_chunk = pipe(chunk)
        summarized_text += " " + summarized_chunk[0]['summary_text']

    return summarized_text


def main():
    model_names = ["t5-small", "facebook/bart-large-cnn", "google/pegasus-cnn_dailymail"]
    chapter_numbers = [2,3,4]
    author_name = "Carroll, Lewis"
    book_name = "A Tangled Tale"
    task = 'summarization'

    records = []

    for chapter_number in chapter_numbers:
        selected_text = get_chapter(author_name, book_name, chapter_number)
        if not selected_text:
            print("Could not get the chapter text.")
            continue

        for model in model_names:
            start_time = time.time()

            summary = generate_summary(selected_text, model, task)
            if not summary:
                print("Could not generate summary.")
                continue

            elapsed_time = time.time() - start_time
            print(f"Time taken for model {model} and chapter {chapter_number}: {elapsed_time} seconds")

            record = {
                'Chapter': chapter_number,
                'Original_Text': selected_text[:100],  # Storing a slice of the original text for demonstration
                f'Summary_{model}': summary,
                f'Time_{model}': elapsed_time
            }
            records.append(record)

    df = pd.DataFrame(records)
    df.to_csv('summary_with_time.csv', index=False)

if __name__ == "__main__":
    main()
