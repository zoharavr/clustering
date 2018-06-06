from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E

from tkFileDialog import askopenfilename


class Calculator:

    def __init__(self, master):
        self.master = master
        master.title("Cluster")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.label = Label(master, text="File:")
        self.entry = Entry(master,bd=2)
        vcmd = master.register(self.validate) # we have to wrap the command
        self.choose_button = Button(master, text="Browse", command=lambda: self.browse())
        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.choose_button.grid(row=2, column=0)


    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False


    def browse(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
        self.entry.insert(0,filename)

root = Tk()
my_gui = Calculator(root)
root.mainloop()
