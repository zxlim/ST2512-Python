## ST2512 Programming in Security: Python Task 3 - Chat Server
## Gerald Peh Wei Xiang (P1445972), DISM/FT/2A/01
## Lim Zhao Xiang (P1529559), DISM/FT/2A/01
#!/usr/bin/python
import datetime
import re
import time
import operator

# Q1
logEntries = 0

# Q2
associateHits = 0
associates = re.compile(r"/assets/js/the-associates.js")

# Q3
IPHits = 0
IP = re.compile(r"10.99.99.186")

# Q4
largestByte = 0
currentByte = 0
byte = re.compile(r" \d+$")
bytePO = "null"


# Q5
wordDict = {}
http = re.compile(r"^http://")
slashExist = re.compile(r"/")
start_time = time.time()
start = str(datetime.datetime.now())[:19]
print "Program started time:" , start

with open("access_log.txt","r") as f:

    while True:
        line = f.readline()

# Question 2: how many /assets/js/the-associates.js
        if associates.search(line):

            associateHits = associateHits + 1

# Question 3: how many 10.99.99.186
        if IP.search(line):

            IPHits = IPHits + 1

# Validation check for last line
        if line == '':
            break

# Question 4: byte size of largest page/object returned to requester
        if byte.search(line):
            currentLine = line.split()
            currentByte = int(line.split()[-1].strip())
            currentPO = str(line.split()[6].strip(''))
            if (currentByte > largestByte):
                largestByte = currentByte
                bytePO = currentPO

# Question 1: number of log entries
        logEntries = logEntries + 1

# Question 5: most visited page with number of hits
        currentPO = str(line.split()[6])
        if http.search(currentPO):
            currentPO = currentPO.replace("http://","")
            if slashExist.search(currentPO):
                updatedPO = currentPO.split("/",1)
                updatedPO = "/" + str(updatedPO[1])
                if updatedPO in wordDict:
                    wordDict[updatedPO] += 1
                else:
                    wordDict[updatedPO] = 1
        else:
            if currentPO in wordDict:
                wordDict[currentPO] += 1
            else:
                wordDict[currentPO] = 1
    f.close()

topHit = max(wordDict.iteritems(), key=operator.itemgetter(1))[0]

print "Total entries were", logEntries

print "Total hits of /assets/js/the-associates.js were", associateHits

print "Total hits made by 10.99.99.186 were", IPHits

print "The largest page/object was", bytePO ,"with the size of", largestByte, "bytes"

print "The highest number of hits was",wordDict[topHit],"for the page",topHit

end = str(datetime.datetime.now())[:19]

print "Program completed time:" , end
print "Program execution time:", (time.time() - start_time),"seconds"
