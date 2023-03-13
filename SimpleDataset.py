from PyPDF2 import PdfReader
import csv
from pdf2docx import Converter
import textract
import re
import string 
import docx2txt
import time
import os

#Locate and Get file names out of directory
Path = "Syllibi/"
DirList = os.listdir(Path)
#DirList.remove('.DS_Store')
print(DirList)


def removeSpecialCharacter(s):
    t = ""
    la="abcdefghijklmnopqrstuvwxyz"
    ua="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nu="0123456789"
    space = ' '
    endline = '\n\r\t'
    punc=string.punctuation
    for i in s:
        if(i in la or i in ua or i in punc or i in nu or i in space or i in endline):
            t+=i
    return t

def extracttitle(Filetitle):
    Extractedlist = Filetitle.split(",")
    print(Extractedlist)
    if (len(Extractedlist) != 5):
        return 0
    classtype = Extractedlist[0]
    classnumber = Extractedlist[1]
    classtitle = Extractedlist[2]
    year = Extractedlist[3]
    professor = Extractedlist[4]
    professor = professor[:-5]
    print(classtype, classnumber, classtitle, year, professor)
    return classtype, classnumber, classtitle, professor, year

for x in range(0,len(DirList)):
    if ".pdf" in DirList[x]:
        tempe = DirList[x]
        path_input = Path + DirList[x]
        path_output = Path + tempe[:-4] + '.docx'
        cv = Converter(path_input)
        cv.convert(path_output, start=0, end=None)
        cv.close()
        os.remove(path_input)

#redefine File List
DirList = os.listdir(Path)
counter = 0
file = open('SimpleSyllabiDataset.csv', 'w', newline ='')

for x in range(0,len(DirList)):
    counter += 1

    #Make sure the file is in .docx form
    if ".docx" in DirList[x]:

        #extract dataset information from syllabis title
        department, number, name, professor, year = extracttitle(DirList[x])

        # Create the Path to the Doc File
        temp = ''
        tempdoc = Path + DirList[x]
        
        # extract the text then convert byte object to string
        text = docx2txt.process(tempdoc)
        text = removeSpecialCharacter(text)
        
        #Split by tab and enter
        Splittext = re.split('\n|\t',text)
        
        #remove empty strings and then remove unwanted spaces
        while("" in Splittext):
            Splittext.remove('')
        for p in range(0,len(Splittext)):
            Splittext[p] = re.sub("\s\s+" , " ", Splittext[p])
       
        #Use 1000 character threshold to combine strings.
        NewList = []
        NewList.append(Splittext[0])
        for y in range(1, len(Splittext)):
            if (len(NewList[-1]) < 1000):
                NewList[-1] = (NewList[-1] + ' ' + Splittext[y])
            else:
                NewList.append(Splittext[y])
        
        # writing the data into the csv file
        file = open('SimpleSyllabiDataset.csv', 'a', newline ='') 
        
        #open file
        with file:

            #Go through dataset and create 3 question,answer, and keyword pairs using openai text-divinci-003
            for x in range(1,len(NewList)):
                #Write the question/answer/keywords to corresponding passage entries
                improvemen = "This class is "+department+ ' '+ number+ ', '+ name+ ', taught by '+professor+ ' in '+ year+'. '  
                fieldnames = ['text', 'class type', 'class number','class name', 'class professor', 'class year']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerow({'text':improvemen + NewList[x], 'class type': department, 'class number': number,'class name': name, 'class year': year, 'class professor': professor })