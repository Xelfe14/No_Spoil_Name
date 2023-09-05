import os
import re

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
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

# Test the function
chapters = get_chapter("Austen, Jane", "Emma", 7)
print(chapters[0])  # Should print the number of chapters retrieved
