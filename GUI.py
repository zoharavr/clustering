from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
from tkFileDialog import askopenfilename
import tkMessageBox
from logic import Model
from PIL import Image,ImageTk


class Clustering:
    def __init__(self, master):
        #build the GUI
        self.master = master
        master.title("Cluster")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.labelfile = Label(master, text="Select a File:")
        self.entryfile = Entry(master,bd=2)
        self.choose_button = Button(master, text="Browse", command=lambda: self.browse())
        self.labelK = Label(master, text="Num of clusters k:")
        self.entryK = Entry(master,bd=2)
        self.labelRun = Label(master, text="Num of runs:")
        self.entryRun = Entry(master,bd=2)
        self.pre = Button(master, text="Pre-process",command=self.pre_proc)
        self.cluster = Button(master, text="Cluster",command=self.clustering)
        # LAYOUT
        self.labelfile.grid(row=0, column=0, sticky=W)
        self.entryfile.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.choose_button.grid(row=1, column=4)
        self.labelK.grid(row=2, column=0, sticky=W)
        self.entryK.grid(row=2, column=1, columnspan=3, sticky=W+E)
        self.labelRun.grid(row=3, column=0, sticky=W)
        self.entryRun.grid(row=3, column=1, columnspan=3, sticky=W+E)
        self.pre.grid(row=4, column=0)
        self.cluster.grid(row=4,column=1)
        self.model=None
    #preprocessing the give data
    def pre_proc(self):
        try:
            input1=self.entryK.get()
            input2=self.entryRun.get()
            #ensure that the user inserted inputs
            if self.validate(n1=input1,n2=input2,path=self.path) :
                self.model=Model(path=self.path,KMeansNumber=input1,run_number=input2)
                self.cluster['state']='normal'
                if(not self.model.preprocess()) :
                    self.cluster['state']='disabled'

        except Exception as error: 
            tkMessageBox.showerror("Error","path is not exist")
            self.cluster['state']='disabled'
# responsible for running K-MEANS and show output
    def clustering(self):
        self.model.cluster()
        self.model.scatter()
        self.model.worldMap()
        self.showImages()
        tkMessageBox.showinfo("K Means Clustering","Clustering process finished successfully")
        
# show the two chats next to each other
    def showImages(self): 
        img_wm = Image.open("./worldMap.png")
        resized = img_wm.resize((500, 500), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        myvar = Label(self.master, image=tkimage)
        myvar.image = tkimage
        myvar.grid(row=5, column=4)
        im_sc = Image.open("./scatter.png")
        resized2 = im_sc.resize((500, 500), Image.ANTIALIAS)
        tkimage2 = ImageTk.PhotoImage(resized2)
        myvar2 = Label(self.master, image=tkimage2)
        myvar2.image = tkimage2
        myvar2.grid(row=5, column=0)
        


#check if the given inputs are correct
    def validate(self,n1,n2,path):
        #check if the inputs are numbers
        if n1.isdigit() !=True  or n2.isdigit()!=True:
            tkMessageBox.showerror("K Means Clustering","Please enter positive numbers")
            self.cluster['state']='disabled'
            return False
         #check if the user inserted a path to a file
        if not path:
            tkMessageBox.showerror("K Means Clustering","Please browse a file")
            self.cluster['state']='disabled'
            return False 
        return True
# user can choose an xlsx file as data
    def browse(self):
        # show an "Open" dialog box and return the path to the selected file
        filename = askopenfilename(title="Choose a file",filetypes=[('xlsx files', '.xlsx')]) 
        self.entryfile.insert(0,filename)
        self.path=filename
# handle the user exiting from the program
    def on_closing(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

root = Tk()
my_gui = Clustering(root)
root.mainloop()


