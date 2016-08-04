## ST2512 Programming in Security
## Task 2 - Password Recovery

#!/usr/bin/python

from crypt import crypt
from datetime import datetime
from itertools import permutations

combinationList = []

def currentDateTime():
    return unicode(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def getCombinations():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for pwLength in range(1,7,1):
        for n in permutations(numbers, pwLength):
            combinationList.append("".join(n[0:]))

def passwordRecovery():
    with open("shadow.txt", "r") as shadowFile:
        for line in shadowFile:
            line = line.replace("\n", "").split(":")
            username = line[0]
            encryption = line[1]
            hashID = encryption.split("$")[1]
            userSalt = encryption.split("$")[2]
            salt = "${}${}$".format(hashID, userSalt)
            print("Attempting recovery on " + username + "'s password...")
            decrypt(encryption, salt)
        shadowFile.close()

def decrypt(encryption, salt):
    for tries in combinationList:
        if crypt(tries, salt) == encryption:
            print("Password found:\t\t" + tries + "\n")
            return

def main():
    print("\nProgram start time:\t" + currentDateTime() + "\n")
    getCombinations()
    passwordRecovery()
    print("Program complete time:\t" + currentDateTime() + "\n")

if __name__ == "__main__":
    main()
