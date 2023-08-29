import re

def get_chapter(book_name, chapter_number):
    
    filepath = book_name+'.txt'
    with open(filepath, "r", encoding="utf8") as file:
        text = file.read()
        text = text.replace('\n',' ')

    # Brute Force regular expression rules to fit most conditions

    # chapters divided by *  *  *  *  * 1179
    case1 = re.search('\*\s+\*\s+\*\s+\*\s+\*',text)
    #chapters divided by chpater Chapter CHAPTER chapters Chapters CHAPTERS 1845
    case2 = (len(re.findall('chapter',text,flags = re.IGNORECASE)) != 0)
    # both case 1 and case2 is 729


    # case3 = 

    if case1 and case2:
        matches=[match.span() for match in re.finditer('chapter',text,flags=re.IGNORECASE)]
        first_ch = 0
        for i in range(1,len(matchesone)):
            if matchesone[i]-matchesone[i-1]<250:
                first_ch+=1
            else:
                continue

        chapters = re.split("chapter ", text, flags = re.IGNORECASE)
        num = chapter_number
        return chapters[:num+first_ch]


    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        num = chapter_number
        return chapters[:num]


    elif case2:
        matches=[match.span() for match in re.finditer('chapter',text,flags=re.IGNORECASE)]
        first_ch = 0
        for i in range(1,len(matchesone)):
            if matchesone[i]-matchesone[i-1]<250:
                first_ch+=1
            else:
                continue

        chapters = re.split("chapter ", text, flags = re.IGNORECASE)
        num = chapter_number
        return chapters[:num+first_ch]


    else:
        return None

get_chapter("A Boy's Fortune; Or, The Strange Adventures of Ben Baker",1)
