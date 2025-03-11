beurt_gevecht = 0
def beurt():
    global beurt_gevecht
    if beurt_gevecht == 0:
        print("De vijand is aan de beurt.")
        beurt_gevecht = 1
    elif beurt_gevecht == 1:
        print("jij bent aan de beurt.")
        beurt_gevecht = 0