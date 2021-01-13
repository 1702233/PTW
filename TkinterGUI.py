from tkinter import *
print("start")
#make the root
root = Tk()
root.title("Steam")
root.geometry("1000x500")

#friendadd button function
def button_add():
    friendlist.insert(END, e.get())
    return

def sort_friendlist():
    temp_list = list(friendlist.get(0, END))
    temp_list.sort(key=str.lower)
    friendlist.delete(0, END)
    for i in temp_list:
        friendlist.insert(END, i)

def delete_friend():
    try:
        index = friendlist.curselection()[0]
        friendlist.delete(index)
    except IndexError:
        pass

#inputfield and add button
e = Entry()
e.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
e.insert(0, "Name of Friend")
add_button = Button(root, text="add friend", padx=5, pady=5, command=button_add)
add_button.grid(row=0, column=2, columnspan=1, padx=2, pady=5)

#friendlist and scrollbar
friendlist = Listbox(root)
friendlist.grid(row=2, column=0, columnspan=3, padx=0, pady=0)
scrollbar = Scrollbar(root)
scrollbar.grid(row=2, column=2, sticky='ns', padx=0, pady=0)
friendlist.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = friendlist.yview)

#sort button for friendlist
sort_button = Button(root, text="sort A-Z", padx=5, pady=5, command=sort_friendlist)
sort_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)
add_button = Button(root, text="delete friend", padx=5, pady=5, command=delete_friend)
add_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5)


root.mainloop()
print("end")