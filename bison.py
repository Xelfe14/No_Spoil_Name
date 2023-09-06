from google.cloud import aiplatform
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import os
import vertexai
from vertexai.language_models import TextGenerationModel

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

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [w for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_text)


def split_text_into_chunks(text, chunk_size=10000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    author_name = "Maupassant, Guy de"
    book_name = "Yvette"
    chapter_number = 4  # Assuming you want the first chapter

    chapter_text = get_chapter(author_name, book_name, chapter_number)
    if chapter_text is not None:
        preprocessed_text = preprocess_text(chapter_text)

        # Split preprocessed_text into chunks
        text_chunks = split_text_into_chunks(preprocessed_text)

        # Print the chapter text and the preprocessed text for debugging
        # print("===== Chapter Text =====")
        # print(chapter_text)
        # print("========================")
        # print("===== Preprocessed Text =====")
        # print(preprocessed_text)
        # print("=============================")

        vertexai.init(project="le-wagon-bootcamp-392422", location="us-central1")
        parameters = {
            "temperature": 0.6,
            "max_output_tokens": 512,
            "top_p": .8,
            "top_k": 40,
        }
        model = TextGenerationModel.from_pretrained("text-bison@001")

        # First Iteration

        summarized_text_list = []
        for i, chunk in enumerate(text_chunks):
            response = model.predict(
                f"""Please summarize the following text using natural language.
                Say it like you were telling a story.

                Text: {chunk}
                """,
            **parameters
            )
            summarized_text_list.append(response.text)

        summarized_text = ' '.join(summarized_text_list)

        # Second Iteration

        parameters = {
            "temperature": 0.6,
            "max_output_tokens": 600,
            "top_p": .8,
            "top_k": 40,
        }
        response = model.predict(
            f"""Please summarize the following text using natural language.

            Text: {summarized_text}
            """,
        **parameters
        )

        print("===== 1st Iteration Summarized Text =====")
        print(summarized_text)
        print("===========================")
        print("===== Summarized Text =====")
        print(response.text)
        print("===========================")

if __name__ == "__main__":
    main()
