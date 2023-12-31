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


rowHeight = 22
fontSize = 11

style = ttk.Style()
style.configure("Treeview", font=(None, fontSize))
style.configure('Treeview', rowheight=rowHeight)
#style.theme_use("step")
style.map('Treeview',  background=[('selected', 'invalid' , '#d6ccc2')] , foreground=[('selected', 'invalid' , 'black')])
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
    global tree 

    result = backUpResult

    item = tree.selection()
    index = item[0]
    #print(index)
    searchString = index
    path = searchTheTable()
    path = path[0].replace("/" , "\\")
    #print(path)
    subprocess.Popen(f"explorer /select, \"{path}\"")
    #print("you clicked on", tree.item(i, "values"))


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
"""

backgroundColors = [ 'blue' , 
    '#023e8a' , 
    '#0077b6' , 
    '#90e0ef' , ##
    '#ade8f4' ,
    '#fff' ,
    ]


foregroundColors = [ 'black' , 
    'white' , 
    'white' , 
    'black' ,
    'black' ,
    'black' ,
    'black' ,
    'black' ,
    ]


def checkToSeeIfThereIsParents(parentArray , theIndex , currentIndex , parrantIndex) :
    global result
    global tree
    global backgroundColors
    global foregroundColors
    
    
    if ( currentIndex == 0 ) :
        return
    else :
        try :
            #print('try : ' , f'{parentArray[parrantIndex]}' , parentArray[currentIndex] , currentIndex , parrantIndex )
            checkToSeeIfThereIsParents(parentArray , theIndex - 1 , currentIndex - 1 , parrantIndex - 1 )
            tree.insert( parentArray[parrantIndex], tk.END, iid = parentArray[currentIndex] , text=parentArray[currentIndex], open=False , tags = (currentIndex) )
            tree.tag_configure( theIndex-1 , background = backgroundColors[theIndex-1] , foreground = foregroundColors[theIndex-1])
        except : 
            pass
    """
    try :
        print('try : ' , f'{parentArray[parrantIndex]}' , parentArray[currentIndex] , currentIndex , parrantIndex )
        if ( currentIndex == 0 ) :
            return
        else :
            tree.insert( parentArray[parrantIndex], tk.END, iid = parentArray[currentIndex] , text=parentArray[currentIndex], open=False , tags = (currentIndex) )
            tree.tag_configure( theIndex-1 , background = backgroundColors[theIndex-1] , foreground = foregroundColors[theIndex-1])
    except : 
        #tree.insert(parentArray[theIndex-1-2], tk.END, iid = parentArray[len(parentArray)-1-1] , text=parentArray[theIndex-1-1], open=False , tags = (theIndex) )
        #counter-=1
        print('error : ' , parentArray[parrantIndex] , parentArray[currentIndex] , currentIndex , parrantIndex )
        if ( currentIndex == 0 ) :
            return
        else :
            checkToSeeIfThereIsParents(parentArray , theIndex - 1 , currentIndex - 1 , parrantIndex - 1 )
    """

def add_data() :
    global result
    global path
    global tree
    global backgroundColors
    global foregroundColors

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
    

    counter = 0
    while counter < length :
        thePath = result[counter].replace( path , '' )
        parentArray = thePath.split('\\')
        theIndex = len(parentArray)
        currentIndex = theIndex - 1
        parrantIndex = theIndex - 1 - 1
        #print(parentArray)
        checkToSeeIfThereIsParents(parentArray , theIndex , currentIndex , parrantIndex)
        counter += 1

    # adding children of first node
    # tree.insert('', tk.END, text='John Doe', iid=5, open=False)
    # tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
    # tree.move(5, 0, 0)
    # tree.move(6, 0, 1)

def fetchAllFilesFromPath() :
    global search
    global result
    global path
    global backUpResult

    #print(path)

    if( path.strip() == '') :
        return

    try :
        search.delete(0,tkinter.END)
        result = glob.glob(path + '/**/*', recursive=True)
        #print(result)
        add_data()
        backUpResult = result
        label.config(text=(path + f" ({len(result)} files)"))
    except : 
        pass

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
        fetchAllFilesFromPath()
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


def searchTree():
    global searchString
    global tree
    query = searchString
    selections = []
    for child in tree.get_children():
        if query.lower() in tree.item(child)['text'].lower():   # compare strings in  lower cases.
            #print(tree.item(child)['text'])
            selections.append(child)
    #print(selections)
    tree.selection_set(selections)


def searchTheTable() :
    global result
    global filteredResult
    global searchString
    global path

    length = len(result)
    
    filteredResult = []
    counter = 0

    #print('----------------------------------')
    while counter < length : 
        #print(result[counter].find(searchString))
        if( (result[counter].replace(path , '').lower()).find(searchString.lower()) != -1 ) :
            #print(result[counter])
            filteredResult.append(result[counter])
        else :
            pass
        counter += 1
    #print('----------------------------------')
    

    #result = filteredResult
    return filteredResult




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
    

    result = searchTheTable()

    #searchTree()
    
    #print(result)
    add_data()
     

#sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
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




menubar = tkinter.Menu(root)
root.config(menu=menubar)

file_menu = tkinter.Menu(menubar , tearoff=0)

file_menu.add_command(
    label='Exit',
    command=root.destroy,
)

options_menu = tkinter.Menu(menubar , tearoff=0)

options_menu.add_command(
    label='Refresh',
    command=fetchAllFilesFromPath,
)

menubar.add_cascade(
    label="File",
    menu=file_menu,
)


menubar.add_cascade(
    label="Options",
    menu=options_menu,
)




# run the app
root.mainloop()



