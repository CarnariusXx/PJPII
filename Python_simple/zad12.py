def alfabet(a):
    words=a.split(" ")
    words= sorted(list(set(words))) # sorted- posortowane   set - bez powtorzen
    print(words)

alfabet("nie było jeszcze żadnego krSzewu polnego na ziemi ani")