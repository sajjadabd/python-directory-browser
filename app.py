import glob

import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog


import subprocess


result = []
backUpResult = []

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', cnf={}, fg='black',
                 fg_placeholder='grey50', *args, **kw):
        super().__init__(master=None, cnf={}, bg='white', *args, **kw)
        self.fg = fg
        self.fg_placeholder = fg_placeholder
        self.placeholder = placeholder
        self.bind('<FocusOut>', lambda event: self.fill_placeholder())
        self.bind('<FocusIn>', lambda event: self.clear_box())
        self.fill_placeholder()

    def clear_box(self):
        if not self.get() and super().get():
            self.config(fg=self.fg)
            self.delete(0, tk.END)

    def fill_placeholder(self):
        if not super().get():
            self.config(fg=self.fg_placeholder)
            self.insert(0, self.placeholder)
    
    def get(self):
        content = super().get()
        if content == self.placeholder:
            return ''
        return content

# create root window
root = tk.Tk()
root.title('Treeview Demo - Hierarchical Data')
root.geometry('400x200')

# configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


style = ttk.Style()
style.configure("Treeview", font=(None, 10))

topFrame = ttk.Frame(root )

# create a treeview
tree = ttk.Treeview(root , show="tree")

def OnDoubleClick(event):
    global result
    item = tree.selection()
    index = int(item[0])
    path = result[index].replace("/" , "\\")
    print(path)
    subprocess.Popen(f"explorer /select, \"{path}\"")
    #print("you clicked on", tree.item(i, "values"))

def add_data() :
    global result
    length = len(result)

    for i in tree.get_children():
        tree.delete(i)

    counter = 0
    while counter < length :
        tree.insert('', tk.END, text=result[counter], iid=counter, open=False )
        counter += 1

    # adding children of first node
    # tree.insert('', tk.END, text='John Doe', iid=5, open=False)
    # tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
    # tree.move(5, 0, 0)
    # tree.move(6, 0, 1)

def openfile():
    global backUpResult
    global result
    result = []
    path = filedialog.askdirectory()
    #print(path)
    label.config(text=path)
    result = glob.glob(path + '/**/*', recursive=True)
    #print(result)
    add_data()
    backUpResult = result
    #return filedialog.askopenfilename()

label = ttk.Label(topFrame , text='select folder to load directories ...' , font=("Calibri",12) )
button = ttk.Button(topFrame , text = 'browse' , command=openfile)

#label.place( relx=0.5 , rely=0.5 )
#button.place( relx=0.5 , rely=0.5 )

label.pack( expand=True , fill='both'  , side=tkinter.LEFT , anchor=tkinter.NW)
button.pack( expand=False  , fill='none'  , side=tkinter.RIGHT  , anchor=tkinter.NE)

topFrame.pack(  fill='both' )

sv = tkinter.StringVar()

def return_pressed(event):
    global result
    global backUpResult

    searchString = str(search.get())

    print(searchString)

    if( searchString.strip() == '' ) :
        result = backUpResult
        add_data()
        return


    length = len(result)
    
    filteredResult = []
    counter = 0

    while counter < length : 
        print(result[counter].find(searchString))
        if( result[counter].find(searchString) != -1 ) :
            filteredResult.append(result[counter])
        else :
            pass
        counter += 1
    
    result = filteredResult
    add_data()
     

sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
#create search bar
search = ttk.Entry(root  , font=("Calibri",12))
#search.bind('<Return>', return_pressed)
search.bind('<KeyRelease>', return_pressed)

search.pack(fill="both")


#tree.heading('#0', text='', anchor=tk.W)
#tree.bind("<Double-1>", OnDoubleClick)
tree.bind("<Double-1>", OnDoubleClick)



# place the Searchbar widget on the root window
# search.grid(row=0, column=0 , sticky=tk.W , ipady = 2  )

# place the Treeview widget on the root window
#tree.grid(row=1, column=0, sticky=tk.NSEW )
tree.pack(fill="both" , expand=True)

# run the app
root.mainloop()