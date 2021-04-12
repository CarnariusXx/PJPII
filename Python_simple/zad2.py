x= int(input("Oblicz silnie z: "))

def silnia(x):
    silnia=1
    if x==0 or x==1:
        print(" Silnia wynosi 1 ")
    elif x>1:
        for i in range(2,x+1):
            silnia=silnia*i
        return silnia

print(silnia(x))
