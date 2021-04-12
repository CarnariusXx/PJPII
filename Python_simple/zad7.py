x = int(input("podaj liczbe w zakresie 0-100"))


def ocena(x):
    if x<0 or x>100:
            print("wprowadziles nieprawidlowa liczbe")
    elif x>=95:
        print("Twoja ocena to bdb")
    elif x>=75 and x<95:
        print ("twoja ocena to db")
    elif x>=65 and x<75:
        print("Twoja ocena to dst")
    elif x<65:
        print("Twoja ocena to ndst")

ocena(x)
