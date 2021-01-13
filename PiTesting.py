from tkinter import *
print("start")
#make the root
root = Tk()
root.title("Steam")
root.geometry("1000x500")

def press_function():
    return

def distance_function():
    return

def servo_function():
    return

def led_function():
    return

def slide_function():
    return


#testing buttons for all raspberrypi functions
press_button = Button(root, text="press", padx=5, pady=5, command=press_function)
press_button.grid(row=4, column=0, columnspan=1, padx=5, pady=5)
distance_button = Button(root, text="distance", padx=5, pady=5, command=distance_function)
distance_button.grid(row=4, column=1, columnspan=1, padx=5, pady=5)
servo_button = Button(root, text="servo", padx=5, pady=5, command=servo_function)
servo_button.grid(row=4, column=2, columnspan=1, padx=5, pady=5)
led_button = Button(root, text="led", padx=5, pady=5, command=led_function)
led_button.grid(row=4, column=3, columnspan=1, padx=5, pady=5)
slide_button = Button(root, text="slide", padx=5, pady=5, command=slide_function)
slide_button.grid(row=4, column=4, columnspan=1, padx=5, pady=5)

root.mainloop()
print("end")