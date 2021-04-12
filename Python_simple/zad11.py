import math
a= int(input("wprowadz bok a prostopadloscianu"))
b=int(input("b"))
h=int(input("h"))

r=int(input("wprowadz r walca"))
h_walca=int(input("wproawdz h walca"))

def prostopdaloscian(a,b,h):
    v=a*b*h
    pc=2*a*b + 2*b*h+2*a*h
    return pc,v

def walec(r,h):
    v=math.pi*r*r*h
    pole_walca= 2*math.pi*r*r +2*math.pi*r*h
    return v, pole_walca

print(prostopdaloscian(a,b,h))
print(walec(r,h_walca))