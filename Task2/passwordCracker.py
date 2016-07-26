## ST2512 Programming in Security
## Task 2 - Password Recovery

#!/usr/bin/python

import platform
from crypt import crypt
from datetime import datetime

def currentDateTime():
    nowDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return unicode(nowDateTime)

def getSystemInfo():
    os = " ".join(platform.linux_distribution()) + ", "
    kernel = platform.system() + " " + platform.release() + "\n"
    print("Operating System: " + os + kernel)

def getHashAlgorithm(hashID):
    if hashID == "1":
        return "MD5"
    elif hashID == "2a":
        return " Blowfish"
    elif hashID == "5":
        return "SHA-256"
    elif hashID == "6":
        return "SHA-512"
    else:
        return "DES"

def passwordCracker():
    print("Starting Password Recovery Script...\n\n")
    with open("shadow.txt", "r") as shadowFile:
        for line in shadowFile:
            line = line.replace("\n", "").split(":")
            username = line[0]
            encryption = line[1]
            decrypt(username, encryption)
        shadowFile.close()

def decrypt(username, encryption):
    hashID = encryption.split("$")[1]
    userSalt = encryption.split("$")[2]
    print("Attempting brute force on " + username + "'s password...")
    print("Hashing Algorithm " + getHashAlgorithm(hashID) + " detected.")
    salt = "${}${}$".format(hashID, userSalt)
    for tries in range(0,999999,1):
        attempt = crypt(str(tries), salt)
        if attempt == encryption:
            print("Password found:\t\t" + str(tries) + "\n")
            break
    return

def main():
    print("\nProgram start time:\t" + currentDateTime() + "\n")
    getSystemInfo()
    passwordCracker()
    print("Program complete time:\t" + currentDateTime() + "\n")

if __name__ == "__main__":
    main()
