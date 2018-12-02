from tkinter import *
from PIL import Image, ImageTk

root = Tk();
screen_width=800
screen_height=600
buttoncolour = "#57463F"

class menu():
    def menucreate():

        button1 = Image.open("aud/new.png")
        button1 = button1.resize((242, 66), Image.ANTIALIAS)
        render1 = ImageTk.PhotoImage(button1)
        img1=Label(canvas, image = render1, borderwidth=0, bg = buttoncolour)
        img1.image = render1
        img1.place(x = 279, y = 300)

        button2 = Image.open("aud/board.png")
        button2 = button2.resize((242, 66), Image.ANTIALIAS)
        render2 = ImageTk.PhotoImage(button2)
        img2=Label(canvas, image = render2, borderwidth=0, bg = buttoncolour)
        img2.image = render2
        img2.place(x = 279, y = 400)

        button3 = Image.open("aud/exit.png")
        button3 = button3.resize((242, 66), Image.ANTIALIAS)
        render3 = ImageTk.PhotoImage(button3)
        img3=Label(canvas, image = render3, borderwidth=0, bg = buttoncolour)
        img3.image = render3
        img3.place(x = 279, y = 500)
        
           
        
def main():
    global root, canvas
    root.title("Ace of the sky")
    canvas = Canvas(root, width = screen_width, height = screen_height, bg = "blue")
    canvas.pack()
    menu.menucreate()
    


    root.mainloop()

main()

