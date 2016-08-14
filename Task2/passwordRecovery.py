## ST2512 Programming in Security: Python Task 2 - Password Recovery
## Lim Zhao Xiang (P1529559), DISM/FT/2A/01
## Gerald Peh Wei Xiang (P1445972), DISM/FT/2A/01
#!/usr/bin/python

from crypt import crypt
from datetime import datetime
from itertools import permutations

combinationList = []

## Returns the current date and time when called.
def currentDateTime():
    return unicode(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

## Generates all possible permutations of passwords for brute forcing later.
def generateCombinations():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for pwLength in range(1,7,1):
        for n in permutations(numbers, pwLength):
            combinationList.append("".join(n[0:]))

## Opens and reads shadow.txt, split the file accordingly, gets the
## encrypted password and salt and pass it to the decrypt function.
def passwordRecovery():
    with open("shadow.txt", "r") as shadowFile:
        for line in shadowFile:
            line = line.replace("\n", "").split(":")
            salt = "${}${}$".format(line[1].split("$")[1], line[1].split("$")[2])
            print("Attempting recovery on " + line[0] + "'s password...")
            print("Password found:\t\t" + decrypt(line[1], salt) + "\n")
        shadowFile.close()

## Using the passwords in the combinationsList generated beforehand and salt,
## attempt to find a match with the encrypted password and returns the
## password in plaintext.
def decrypt(encryption, salt):
    for password in combinationList:
        if crypt(password, salt) == encryption:
            return password

print("\nProgram start time:\t" + currentDateTime() + "\n")
generateCombinations()
passwordRecovery()
print("Program complete time:\t" + currentDateTime() + "\n")
