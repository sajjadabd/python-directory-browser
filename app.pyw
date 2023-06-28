import glob

import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog


import subprocess


result = []
backUpResult = []
path = ''

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
root.title('Easy Search')
root.geometry('500x400')

# configure the grid layout
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


style = ttk.Style()
style.configure("Treeview", font=(None, 10))
#style.theme_use("step")

#('aqua', 'step', 'clam', 'alt', 'default', 'classic')

topFrame = ttk.Frame(root )

# create a treeview
tree = ttk.Treeview(root , show="tree")

vsb = ttk.Scrollbar(orient="vertical",command=tree.yview)
vsb.pack( side=tkinter.RIGHT , fill='both' )
tree.configure(yscrollcommand=vsb.set)

def OnDoubleClick(event):
    global searchString
    global result
    global filteredResult
    global backUpResult

    result = backUpResult

    item = tree.selection()
    index = item[0]
    print(index)
    searchString = index
    path = searchTheTable()
    path = path[0].replace("/" , "\\")
    print(path)
    subprocess.Popen(f"explorer /select, \"{path}\"")
    #print("you clicked on", tree.item(i, "values"))

def add_data() :
    global result
    global path
    length = len(result)

    for i in tree.get_children():
        tree.delete(i)


    """
    tree.insert('', 'end', 'item1',text ='GeeksforGeeks')
 
    # Inserting child
    tree.insert('', 'end', 'item2',text ='Computer Science')
    tree.insert('', 'end', 'item3',text ='GATE papers')
    tree.insert('', 'end', 'item4',text ='Programming Languages')

    # Inserting more than one attribute of an item
    tree.insert('item2', 'end', 'Algorithm',text ='Algorithm') 
    tree.insert('item2', 'end', 'Data structure',text ='Data structure')
    tree.insert('item3', 'end', '2018 paper',text ='2018 paper') 
    tree.insert('item3', 'end', '2019 paper',text ='2019 paper')
    tree.insert('item4', 'end', 'Python',text ='Python')
    tree.insert('item4', 'end', 'Java',text ='Java')

    # Placing each child items in parent widget
    tree.move('item2', 'item1', 'end')
    tree.move('item3', 'item1', 'end')
    tree.move('item4', 'item1', 'end')
    """
    
    backgroundColors = [ 'blue' , 'black' , 
    '#03045e' , 
    '#023e8a' , 
    '#0077b6' , 
    '#0096c7' ,
    '#00b4d8' ,
    '#48cae4' ,
    '#90e0ef' ,
    '#ade8f4' ,
    ]

    backgroundColors = [ 'blue' , 'black' , 
    '#023e8a' , 
    '#0077b6' , 
    '#90e0ef' , ##
    '#ade8f4' ,
    '#ade8f4' ,
    ]


    foregroundColors = [ 'black' , 'black' , 
    'white' , 
    'white' , 
    'black' ,
    'black' ,
    'black' ,
    'black' ,
    'black' ,
    ]

    style.map('Treeview',  background=[('selected', 'orange')] , foreground=[('selected', 'black')])

    counter = 0
    while counter < length :
        thePath = result[counter].replace( path , '' )
        parentArray = thePath.split('\\')
        #print(parentArray)
        try :
            theIndex = len(parentArray)
            tree.insert(parentArray[theIndex-1-1], tk.END, iid = parentArray[len(parentArray)-1] , text=parentArray[theIndex-1], open=False , tags = (theIndex) )
            tree.tag_configure( theIndex , background = backgroundColors[theIndex] , foreground = foregroundColors[theIndex])
        except :
            pass
        counter += 1

    # adding children of first node
    # tree.insert('', tk.END, text='John Doe', iid=5, open=False)
    # tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
    # tree.move(5, 0, 0)
    # tree.move(6, 0, 1)

def openfile():
    global backUpResult
    global result
    global path
    result = []
    path = filedialog.askdirectory()
    #print(f"#{path}#")
    if( path.strip() == '' ) :
        pass
    else :
        search.delete(0,tkinter.END)
        result = glob.glob(path + '/**/*', recursive=True)
        #print(result)
        add_data()
        backUpResult = result
        label.config(text=(path + f" ({len(result)} files)"))
        #return filedialog.askopenfilename()
    

label = ttk.Label(topFrame , text='select folder to load directories ...' , font=("Calibri",12) )
button = ttk.Button(topFrame , text = 'browse' , command=openfile)

#label.place( relx=0.5 , rely=0.5 )
#button.place( relx=0.5 , rely=0.5 )

label.pack( expand=True , fill='both'  , side=tkinter.LEFT , anchor=tkinter.NW)
button.pack( expand=False  , fill='none'  , side=tkinter.RIGHT  , anchor=tkinter.NE)

topFrame.pack(  fill='both' )

sv = tkinter.StringVar()

searchString = ''



def searchTheTable() :
    global result
    global filteredResult
    global searchString

    length = len(result)
    
    filteredResult = []
    counter = 0

    while counter < length : 
        #print(result[counter].find(searchString))
        if( (result[counter].lower()).find(searchString.lower()) != -1 ) :
            filteredResult.append(result[counter])
        else :
            pass
        counter += 1
    
    result = filteredResult
    return result




def return_pressed(event):
    global result
    global backUpResult
    global searchString

    if ( len(searchString) > len( str(search.get()) ) ) :
        result = backUpResult

    searchString = str(search.get())

    #print(searchString)

    if( searchString.strip() == '' ) :
        result = backUpResult
        add_data()
        return
    

    searchTheTable()

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
#tree.pack( anchor=tk.NW , fill="y" , expand=True)
tree.pack( fill="both" , expand=True)

# run the app
root.mainloop()