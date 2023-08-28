import re

def get_chapter(book_name, chapter_number):
    
    filepath = book_name+'.txt'
    with open(filepath, "r", encoding="utf8") as file:
        text = file.read()
    text = text.replace('\n',' ')

    if len(re.findall('chapter',text,flags = re.IGNORECASE)) != 0:

        chapters = re.split("chapter ", text, flags = re.IGNORECASE)
        num = chapter_number+1

        return chapters[num]

    else:

        return None

    

get_chapter("A Boy's Fortune; Or, The Strange Adventures of Ben Baker",1)
