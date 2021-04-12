x = int(input("podaj 1 liczbe"))
y= int(input("podaj druga liczbe"))

def podzielnaprzez7nie5(x,y):
    for i in range(x,y+1):
        if i%7==0 and i%5!=0:
            print(i, end=", ")

podzielnaprzez7nie5(x,y)
