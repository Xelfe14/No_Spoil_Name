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
        print('case1&2')
        matchesone=[match.span()[0] for match in re.finditer('chapter',text,flags=re.IGNORECASE)]
        fi_ch = 0
        for i in range(1,len(matchesone)):
            if matchesone[i]-matchesone[i-1]<50:
                fi_ch+=1
            else:
                continue
#         print(first_ch)
        chapters = re.split("chapter", text, flags = re.IGNORECASE)
        num = chapter_number
        return chapters[1:num+fi_ch]


    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        num = chapter_number
        return chapters[1:num]


    elif case2:
#         print('case2')
        matchesone=[match.span()[0] for match in re.finditer('chapter',text,flags=re.IGNORECASE)]
        fi_ch = 0
        for i in range(1,len(matchesone)):
            if matchesone[i]-matchesone[i-1]<50:
                fi_ch+=1
            else:
                continue
#         print(first_ch)
        chapters = re.split("chapter", text, flags = re.IGNORECASE)
        num = chapter_number
        return chapters[1:num+fi_ch]


    else:
        return None

result = get_chapter("Wait and Hope; Or, A Plucky Boy's Luck",5)
