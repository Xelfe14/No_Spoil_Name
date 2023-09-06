import re

def chunk_chapter(text,len_lim):
    num_chunk = len(text)//len_lim
#     print(num_chunk)
    txt_list = []
    
    for i in range(1,num_chunk+1):
        txt_list.append(text[(i-1)*len_lim:i*len_lim])
        
    txt_list.append(text[num_chunk*len_lim:])
    return txt_list
    

def get_chapter(book_name, chapter_number,length_limitation=13000):
    
    filepath = book_name+'.txt'
    with open(filepath, "r", encoding="utf8") as file:
        text = file.read()
        text = text.replace('\n',' ')
        text = text.replace("\'re", " are")
        text = text.replace("\'d", " would")
        text = text.replace("\'ll", " will")
        text = text.replace("won't", "would not")

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
        # TO DO:
        # Cut Chapter into small pieces to fit the input limitation of models
        ch_txt = ''.join(chapters[1:num+fi_ch])
        txt_list = chunk_chapter(ch_txt,length_limitation)
        return txt_list


    elif case1:
        chapters = re.split("\*\s+\*\s+\*\s+\*\s+\*", text)
        num = chapter_number
        # TO DO:
        # Cut Chapter into small pieces to fit the input limitation of models
        ch_txt = ''.join(chapters[1:num])
        txt_list = chunk_chapter(ch_txt,length_limitation)
        return txt_list


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
        # TO DO:
        # Cut Chapter into small pieces to fit the input limitation of models
        ch_txt = ''.join(chapters[1:num+fi_ch])
        txt_list = chunk_chapter(ch_txt,length_limitation)
        return txt_list

    else:
        ch_txt = text
        txt_list = chunk_chapter(ch_txt,length_limitation)
        return txt_list

# result = get_chapter("Wait and Hope; Or, A Plucky Boy's Luck",5)
