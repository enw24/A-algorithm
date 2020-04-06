import csv
datatfile = open('Colorado.csv','r')
datareader = csv.reader(datatfile)
data = []
altToEnd = []
destination = 0
traversed = []


# paths in queue is sorted list with xLoc, yLoc, totalAlt, altToSpot, altFromSpot, pathList
queueItem = []
queueList = []
#path is a simple list of grid coordinates that defines a path
path = []

def CalcSPAlt (CurX, CurY, EndPoint):
    alt = 0
    horiz = CurY
    for x in range(CurX, 480):
        if x == 479:
            for i in range(min(horiz, EndPoint),max(horiz,EndPoint)):
                alt += abs(data[479][i+1] - data[479][i])
            return alt
        if horiz < EndPoint:
            alt += abs(data[x+1][horiz+1] - data[x][horiz])
            horiz += 1
        elif horiz > EndPoint:
            alt += abs(data[x+1][horiz-1] - data[x][horiz])
            horiz -= 1
        else:
            alt += abs(data[x+1][horiz] - data[x][horiz])
    return alt




# this reads the data and converts it to integer
for r in datareader:
    data.append(r)
for i in range(0, len(data)):
    for j in range(0, len(data[0])):
        data[i][j] = int(data[i][j])

destination = 5
starting = 300

# Calculate altToEnd on shortest path
# for i in range(0, 480):
#    tempList = []
#    for j in range (0, 480):
#        tempList.append(CalcSPAlt(i, j, destination))
#    altToEnd.append(tempList)



def CleanseList():
    global queueList

    for x in range(0, len(queueList)-1):
        qL = queueList.copy()
        if x == len(qL)-1:
            break

        removeFlag = True

        #print(len(queueList))
        #print(x)
        #print('test', queueList[x][0], queueList[x][1])
        #print('x y coord', qL[x][0], qL[x][1])

        for i in range(max(qL[x][0] - 1, 0), min(qL[x][0] + 2, 480)):
            for j in range(max(qL[x][1] - 1, 0), min(qL[x][1] + 2, 480)):
                if traversed[i][j] == 0:
                    removeFlag = False
                    #print("getting here")
        if removeFlag:
            #print(queueList)
            #print("ql",qL)
            del queueList[x]
            #print('removing')



for i in range(0, 480):
    row = [0] *480
    traversed.append(row)



traversed[0][starting] = 1
path.append([0, starting])

queueItem.append(0)
queueItem.append(starting)
queueItem.append(CalcSPAlt(0, starting, destination))
queueItem.append(0)
queueItem.append(CalcSPAlt(0, starting, destination))
queueItem.append(path)

queueList.append(queueItem.copy())

there = False

# while not there:
for z in range(0,10000):

    # select grid from top of queue
    currentX = queueList[0][0]
    currentY = queueList[0][1]
    currentAltFromStart = queueList[0][3]
    currentPath = queueList[0][5].copy()
    if currentX == 479 and currentY == destination:
        print("DONE")
        break
    #print("current x and y", currentX, currentY)
    # add paths to queue
    for i in range(max(currentX-1, 0), min(currentX+2,480)):
        for j in range(max(currentY-1, 0), min(currentY+2, 480)):
            #print("here")
            traversed[i][j] = 1
            queueItem.clear()
            queueItem.append(i)
            queueItem.append(j)
            altfromStart = currentAltFromStart + abs(data[currentX][currentY] - data[i][j])
            queueItem.append(altfromStart+CalcSPAlt(i,j,destination))
            queueItem.append((altfromStart))
            queueItem.append(CalcSPAlt(i,j,destination))
            tempPath = []
            tempPath.clear()
            tempPath = currentPath.copy()
            tempPath.append([i, j])
            queueItem.append(tempPath)
            if not(currentX == i and currentY == j):
                addedFlag = False
                for p in range(0, len(queueList)):
                    if queueItem[2] < queueList[p][2]:
                        queueList.insert(p, queueItem.copy())
                        addedFlag = True
                    if addedFlag:
                        break
                if not addedFlag:
                    queueList.append(queueItem.copy())
    CleanseList()
    print('first five in queueList are:')
    l = len(queueList)
    if l > 10:
        l = 10
    for z in range(0, l):
        print(queueList[z])
