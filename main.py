from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try: #it was run before
    data = pandas.read_csv("data/words_to_learn.csv") #dataframe
except FileNotFoundError: #if words to learn is not found or deleted
    original_data = pandas.read_csv("data/malayalam_words.csv")
    to_learn = original_data.to_dict(orient="records")
else: #try works
    to_learn = data.to_dict(orient="records") #converts datafram into dictionary, orient gives a list of dictionary with each language words

# print(data) #prints in column format
# print(to_learn) #formats into 2d dictionary
current_card = {}

def next_card(): #takes word from csv
    global current_card, flip_timer #made global to use in flip card function
    window.after_cancel(flip_timer) #cancels the ongoing timer when you click through x or check
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title,text="Malayalam", fill="black")
    canvas.itemconfig(card_word, text=current_card["Malayalam"], fill="black") #change word
    canvas.itemconfig(card_background, image=card_front_img) #flips from back to front
    flip_timer = window.after(3000, func=flip_card) #flips every card

def flip_card(): #flips to translation
    canvas.itemconfig(card_title, text="English", fill="white") #color now white
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known(): #signifies check mark meaning the card is known
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False) #stores the unknown words into a csv file, false does not add index values to csv
    next_card()

window = Tk() #creates window
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card) #flips card after 3 seconds passed

canvas = Canvas(width=800, height =526) #creates card, same as width and height of card
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img) #center of canvas
card_title = canvas.create_text(400,150,text="", font=("Ariel",40,"italic"))
card_word = canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0) #0 gets rid of border thickness
canvas.grid(row=0,column=0, columnspan =2) #columnspan aligns check and x (starts at column 0 and ends at column 2)

cross_image = PhotoImage(file="images/wrong.png") #x
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1,column=0)

check_image = PhotoImage(file="images/right.png") #check
known_button = Button(image=check_image, highlightthickness=0,command=is_known) #border still there so user knows they clicked it
known_button.grid(row=1, column=1)

next_card() #creates a card right when you start the application (instead of blank card)

window.mainloop()

