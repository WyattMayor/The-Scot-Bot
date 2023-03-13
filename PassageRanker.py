import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
import re
import pandas as pd
import string
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def is_empty(self):
        return not self._queue
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
#Remove endings/Add endings to make keywords more specific
def ExtendKeywords(KW):
    print(KW)
    NewKeywords = []
    for elements in KW:
        NewKeywords.append(elements)
        if elements[-1] == "e":
            NewKeywords.append(elements[:-1]+"ing")
            NewKeywords.append(elements[:-1]+"y")
            NewKeywords.append(elements[:-1]+"s")
        elif elements[-3:] == "ing":
            NewKeywords.append(elements[:-3]+"e")
            NewKeywords.append(elements[:-3]+"y")
            NewKeywords.append(elements[:-3]+"s")
        elif elements[-1] == "y":
            NewKeywords.append(elements[:-1]+"e")
            NewKeywords.append(elements[:-1]+"ing")
            NewKeywords.append(elements[:-1]+"s")
        elif elements[-1] == "s":
            NewKeywords.append(elements[:-1]+"e")
            NewKeywords.append(elements[:-1]+"ing")
            NewKeywords.append(elements[:-1]+"y")
    print(NewKeywords)
    return NewKeywords

def KeywordExtractor(question):
    new_question = remove_stopwords(question)
    print(new_question)
    readyquestion = re.sub(r"[,.;@#?!&$]+\ *", "", new_question)
    SplitUpQuestion = readyquestion.split(" ")
    return SplitUpQuestion

def KeywordCounter(keywords, Modified_Dataset):
    x = 0
    Que = PriorityQueue()
    for x in range(0, Modified_Dataset.shape[0]):
        counter = 0
        for keyword in keywords:
          if keyword.lower() in (Modified_Dataset["Passage"].iloc[x]).lower():
              counter += 1
        print(counter)
        Que.push(Modified_Dataset["Passage"].iloc[x], 0 - counter) 
    String = Que.pop()
    String2 = String + Que.pop()
    string3 = String2 + Que.pop()
    print(string3)
    return string3

def StarterMain(class_type, class_number, professor, question):
    print(class_type)
    print(class_number)
    print(professor)
    if question == "":
        return 0
    syllabidf = pd.read_csv("SimpleSyllabiDataset.csv", encoding='cp1252')
    Keywords = KeywordExtractor(question)
    syllabidf.columns = ['Passage', 'Department','Number','Name','Professor', 'Year']
    Depart = False
    CNum = False
    prof = False
    if class_type != "Department":
        DepartmentDF = syllabidf[syllabidf["Department"].values == class_type]
        Depart = True
    if class_number != "Class number":
        if Depart == False:
            DepartmentDF = syllabidf.copy()
        DepNumSorted = DepartmentDF[DepartmentDF["Number"].values == int(class_number)]
        CNum = True
    if professor != "Professor":
        if Depart != True and CNum != True:
            DepNumSorted = syllabidf.copy()
        DepNumSorted = DepNumSorted[DepNumSorted["Professor"].values == professor]
        prof = True
    if prof == False and CNum == False and Depart == False:
        DepNumSorted = syllabidf.copy()
    NewKeywords = ExtendKeywords(Keywords)
    Prompt = KeywordCounter(NewKeywords, DepNumSorted)
    print(Prompt)
    return Prompt