from tkinter import *
from PIL import Image, ImageTk

root = Tk();
screen_width=800
screen_height=600
buttoncolour = "#57463F"

class menu():
    def menucreate():

        button1 = Image.open("aud/title.png")
        button1 = button1.resize((711, 116), Image.ANTIALIAS)
        render1 = ImageTk.PhotoImage(button1)
        img1=Label(canvas, image = render1, borderwidth=0, bg = buttoncolour)
        img1.image = render1
        img1.place(x = 50, y = 50)

        button2 = Image.open("aud/back.png")
        button2 = button2.resize((242, 66), Image.ANTIALIAS)
        render2 = ImageTk.PhotoImage(button2)
        img2=Label(canvas, image = render2, borderwidth=0, bg = buttoncolour)
        img2.image = render2
        img2.place(x = 10, y = 520)
   
        
def main():
    global root, canvas
    root.title("Ace of the sky")
    canvas = Canvas(root, width = screen_width, height = screen_height, bg = "black")
    canvas.pack()
    menu.menucreate()
    


    root.mainloop()

main()

