## ST2512 Programming in Security
## Task 2 - Password Recovery
## BETA: Use this python file to test new stuff
#!/usr/bin/python

from crypt import crypt
from datetime import datetime
from itertools import permutations

combinationList = []

def currentDateTime():
    return unicode(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def passwordRecovery():
    with open("shadow.txt", "r") as shadowFile:
        for line in shadowFile:
            line = line.replace("\n", "").split(":")
            salt = "${}${}$".format(line[1].split("$")[1], line[1].split("$")[2])
            print("Attempting recovery on " + line[0] + "'s password...")
            print("Password found:\t\t" + decrypt(line[1], salt) + "\n")
        shadowFile.close()

def decrypt(encryption, salt):
    for tries in combinationList:
        if crypt(tries, salt) == encryption:
            return tries

def main():
    print("\nProgram start time:\t" + currentDateTime() + "\n")
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for pwLength in range(1,7,1):
        for n in permutations(numbers, pwLength):
            combinationList.append("".join(n[0:]))
    passwordRecovery()
    print("Program complete time:\t" + currentDateTime() + "\n")

if __name__ == "__main__":
    main()
