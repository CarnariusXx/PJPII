x= int(input("wprowadz swoj wiek "))

def wiek(x):
    if 1>=x>=0:
        print("jestes noworodkiem")
    elif x>=2 and x<=10:
        print("jestes dzieckiem")
    elif 17>=x>=11:
        print("jestes nastolatkiem")
    elif x>=18:
        print("jestes dorosly")

wiek(x)