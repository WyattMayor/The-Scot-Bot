#Import the required libraries
from tkinter import *
from tkinter import ttk
import pandas as pd
import PassageRanker
import ApiRequest
from PIL import ImageTk, Image

# Load in the Logo for the top of the GUI
image1 = Image.open("Logo.png")

#Read in the syllabi dataset and configure the columns
syllabidf = pd.read_csv("SimpleSyllabiDataset.csv", encoding='cp1252')
syllabidf.columns = ['Passage', 'Department','Number','Name','Professor', 'Year']

#Get unique values in each column from the dataframe for drop down menu selection
Departmentlist = syllabidf["Department"].unique()
Professorlist = syllabidf["Professor"].unique()
ClassNumList = syllabidf["Number"].unique()

#Create the GUI and title it The Scot Bot
win= Tk()
win.title("The Scot Bot")

#Set the program window size
win.geometry("765x700")

#Display logo at the top of the program
test = ImageTk.PhotoImage(image1)
Logo = Label(image=test)
Logo.image = test
Logo.pack(pady = 20)

# answer box that will display the answer to the question
label=Text(win, font=("Courier 12 bold"), width=100, height = 9)
label.tag_configure("center", justify='center')
label.insert(INSERT,"")
label.config(state=DISABLED)
label.pack()

#Question box where the user can input their question
entry= Entry(win, width= 40)
entry.focus_set()
entry.pack(pady=20)

# Create Department drop down menu using unique values from the original dataset
Department = StringVar()
Department.set("Department")

drop= OptionMenu(win, Department, *Departmentlist)
drop.pack()

# Create Class number drop down menu using unique values from the original dataset
Number = StringVar()
Number.set("Class number")

drop= OptionMenu(win, Number, *ClassNumList)
drop.pack()

# Create professor drop down menu using unique values from the original dataset
Teacher = StringVar()
Teacher.set("Professor")

drop= OptionMenu(win, Teacher, *Professorlist)
drop.pack(pady=(0,20))

#Dislplays the answer and the passage that it used to find the answer
def display_text(answer, passage):
   label.configure(state='normal')
   label.delete('1.0', END)
   label.insert(INSERT,answer)
   label.configure(state='disabled')
   Paragraph.configure(state='normal')
   Paragraph.delete('1.0', END)
   Paragraph.insert(INSERT, ("Context Paragraph: " + passage))
   Paragraph.configure(state='disabled')

#Ask button function that is used to find the best passage suited to answer the question
def PassagePicked():
   passage = PassageRanker.StarterMain(Department.get(), Number.get(), Teacher.get(), entry.get())
   if entry.get() != "":
      Answer = ApiRequest.RequestQA(entry.get(), passage)
      display_text(Answer,passage)

#Exit function for exit button to quit the program
def ProgramExit():
   exit(0)

#Reset function that will clear all text boxes
def reset():
   label.configure(state='normal')
   label.delete('1.0', END)
   label.insert(INSERT,"")
   label.configure(state='disabled')
   Paragraph.configure(state='normal')
   Paragraph.delete('1.0', END)
   Paragraph.insert(INSERT, "")
   Paragraph.configure(state='disabled')

#Create three buttons ask, reset, exit
ttk.Button(win, text= "Ask!!", width= 20, command=PassagePicked).pack()
ttk.Button(win, text= "Reset", command=reset,width= 20).pack()
ttk.Button(win, text= "Exit", width= 20, command=ProgramExit).pack(pady=(0,20))

#create a text box that contains the context text that the question was answered from
Paragraph = Text(win, font=("Courier 12"), width = 100, height= 9)
Paragraph.tag_configure("center", justify='center')
Paragraph.config(state=DISABLED)
Paragraph.insert(INSERT, '')
Paragraph.pack()

# Start the main loop to start the GUI
win.mainloop()
