import glob

result = glob.glob('.\\main\\**\\*', recursive=True)

print(result)


"""
for x in result :
    print(x)
"""

import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog

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

def openfile():
    path = filedialog.askdirectory()
    print(path)
    label.config(text=path)
    #return filedialog.askopenfilename()

label = ttk.Label(topFrame , text='label' , font=("Calibri",12) )
button = ttk.Button(topFrame , text = 'browse' , command=openfile)

#label.place( relx=0.5 , rely=0.5 )
#button.place( relx=0.5 , rely=0.5 )

label.pack( expand=True , fill='both'  , side=tkinter.LEFT , anchor=tkinter.NW)
button.pack( expand=False  , fill='none'  , side=tkinter.RIGHT  , anchor=tkinter.NE)

topFrame.pack(  fill='both' )

#create search bar
search = ttk.Entry(root , font=("Calibri",12))

search.pack(fill="both")

# create a treeview
tree = ttk.Treeview(root , show="tree")
#tree.heading('#0', text='', anchor=tk.W)


# adding data
tree.insert('', tk.END, text='Administration', iid=0, open=False )
tree.insert('', tk.END, text='Logistics', iid=1, open=False)
tree.insert('', tk.END, text='Sales', iid=2, open=False)
tree.insert('', tk.END, text='Finance', iid=3, open=False)
tree.insert('', tk.END, text='IT' , iid=4, open=False)

# adding children of first node
tree.insert('', tk.END, text='John Doe', iid=5, open=False)
tree.insert('', tk.END, text='Jane Doe', iid=6, open=False)
tree.move(5, 0, 0)
tree.move(6, 0, 1)

# place the Searchbar widget on the root window
# search.grid(row=0, column=0 , sticky=tk.W , ipady = 2  )

# place the Treeview widget on the root window
#tree.grid(row=1, column=0, sticky=tk.NSEW )
tree.pack(fill="both" , expand=True)

# run the app
root.mainloop()