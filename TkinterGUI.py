from tkinter import *
from tkinter import ttk
from datetime import datetime
import json


print("start")
#load the steam.json file
with open('./steam.json') as f:
    jsondata = json.load(f)

#global variables
time_game_started = None
current_game = None

#make the root
root = Tk()
root.title("Steam")
root.geometry("1400x600")
root.configure()

#set grid for the frames
root.grid_rowconfigure(0, minsize=200, weight=1)
root.grid_columnconfigure(0, minsize=150, weight=1)
root.grid_columnconfigure(1, weight=1)

#style
style = ttk.Style()
style.configure(
    "TLabel",
    background="#696969",
)

#making two frames for games and friendlist
library_frame = Frame(root, bg="#696969")
library_frame.grid(row=0,column=0, sticky="nsew")
gameinfo_frame = Frame(root, bg="#696969")
gameinfo_frame.grid(row=0,column=1, sticky="nsew")
friendlist_frame = Frame(root, bg="#696969")
friendlist_frame.grid(row=0,column=2, sticky="nsew")

#temp text in entry field
def on_entry_click(event):
    if e.get() == 'Enter a username...':
       e.delete(0, "end") # delete all the text in the entry
       e.insert(0, '') #Insert blank for user input
       e.config(fg = 'black')
def on_focusout(event):
    if e.get() == '':
        e.insert(0, 'Enter a username...')
        e.config(fg = 'grey')

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

def update_game(game):
    global time_game_started
    global current_game
    time_game_started = datetime.now()
    current_game = game
    current_game_label.config(text="Playing: " + game)
    stop_playing_button.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
    time_played_label.grid_remove()
    show_game_statistics(game)

def stop_game():
    global current_game
    current_game_label.config(text="Currently not playing a game")
    stop_playing_button.grid_remove()
    time_played = (datetime.now() -time_game_started)
    time_played_label.config(text="Played " + current_game +" for : " + str(time_played).split(".")[0])
    time_played_label.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
    hide_game_statistics()


def show_game_statistics(game):
    #find the right jsonobject for currentgame
    global jsondata
    gamestatsprint = "stats not found"
    try:
        for gamedata in jsondata:
            if game == gamedata["name"]:
                displaygame = gamedata
        gamestatsprint =  (
        "developer : " + str(displaygame["developer"]) +
        "\npublisher : " + str(displaygame["publisher"]) + 
        "\nrelease_date : " + str(displaygame["release_date"]) +
        "\nachievements : " + str(displaygame["achievements"]) + 
        "\npositive_ratings : " + str(displaygame["positive_ratings"]) + 
        "\nnegative_ratings : " + str(displaygame["negative_ratings"]) + 
        "\nprice : " + str(displaygame["price"]) +
        "\naverage_playtime : " + str(displaygame["average_playtime"]) + 
        "\nowners : " + str(displaygame["owners"]) +
        "\ncategories : " + str(displaygame["categories"]) +
        "\ngenres : " + str(displaygame["genres"]) +
        "\nsteamspy_tags : " + str(displaygame["steamspy_tags"]) +
        "\nplatforms : " + str(displaygame["platforms"])
    )
    except:
        print("Could not find game in steam.json")
    
    gamestats_label.config(text=gamestatsprint)
    gamestats_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)




def hide_game_statistics():
    gamestats_label.grid_remove()


#inputfield and add button
e = Entry(friendlist_frame)
e.bind('<FocusIn>', on_entry_click)
e.bind('<FocusOut>', on_focusout)
e.config(fg = 'grey')
e.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
e.insert(0, "Enter a username...")
add_button = Button(friendlist_frame, text="add friend", padx=5, pady=5, command=button_add)
add_button.grid(row=0, column=2, columnspan=1, padx=2, pady=5)

#friendlist and scrollbar
friendlist = Listbox(friendlist_frame)
friendlist.grid(row=2, column=0, rowspan=3, columnspan=3, padx=0, pady=0)
scrollbar = Scrollbar(friendlist_frame)
scrollbar.grid(row=2, column=2, rowspan=3, sticky='ns', padx=0, pady=0)
friendlist.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = friendlist.yview)

#load names in friendlist
friendlistfile = open('friendlist.txt','r')
friendlistreader = friendlistfile.readlines()

for friend in friendlistreader:
    friendlist.insert(END, friend.rstrip("\n"))


#sort button for friendlist
sort_button = Button(friendlist_frame, text="sort A-Z", padx=5, pady=5, command=sort_friendlist)
sort_button.grid(row=5, column=0, columnspan=1, padx=5, pady=5)
add_button = Button(friendlist_frame, text="delete friend", padx=5, pady=5, command=delete_friend)
add_button.grid(row=5, column=2, columnspan=1, padx=5, pady=5)

#playing game display
current_game_label = ttk.Label(gameinfo_frame, text="Currently not playing a game", font=("TkDefaultFont", 33))
current_game_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

#stop playing button and timeplayed
stop_playing_button = Button(gameinfo_frame, text="stop game", command=stop_game)
time_played_label = ttk.Label(gameinfo_frame, text="")

#gamestatistics
gamestats_label = ttk.Label(gameinfo_frame, text="no statistics found")

#labelframe for library
labelframe = LabelFrame(library_frame, text="Game Library", font=("TkDefaultFont", 33), bg="#696969")
labelframe.grid(row=1, rowspan=1, column=0, columnspan=5)

#load gamelist
gamelistfile = open('gamelist.txt','r')
gamelist = gamelistfile.readlines()


#make buttons for each game
for i in range(len(gamelist)):
    new_button = Button(labelframe, text=gamelist[i].rstrip("\n"),
                    command=lambda j=i: update_game(gamelist[j].rstrip("\n")))
    new_button.grid(row=i+3, column=1, columnspan=1, padx=2, pady=2)

root.mainloop()
print("end")