## Minesweeper
## 05/01/2019

## uses John Zelle's graphics.py
## Enter name first, then play the game
## create a txt called leaderboard.txt to keep track of past scores
## creates mineCheatSheet.txt that records the positions of each mine

from graphics import *
from random import randrange
from math import *
import time

# creates graphic window
def setUpWindow():
    win=GraphWin("Minesweeper", 800, 800)
    win.setBackground("gray")
    win.setCoords(0,0,8,9)
    return win

# makes the graphic window look like a proper board
def graphing(win):
# creates vertical and horizontal lines, creating "tiles"
    for i in range(7):
        hor=Line(Point(0, i+1), Point(8, i+1))
        ver=Line(Point(i+1, 0), Point(i+1, 8))
        hor.draw(win)
        ver.draw(win)
# creates a blank space above the tiles
    header=Rectangle(Point(0,8), Point(8,9))
    header.setFill("white")
    header.draw(win)

# writes necessary background text on the header
def setUpHeader(win):
    a=Text(Point(5,8.5), "Remaining Tiles:")
    b=Text(Point(6.8, 8.5), "Time:")
    tileText=Text(Point(6.2, 8.5), "54")
    timeText=Text(Point(7.5, 8.5), "0")
    e=Text(Point(0.5, 8.5), "Name")
    inputBox=Entry(Point(2.2, 8.5), 20)

    a.setSize(18)
    b.setSize(18)
    tileText.setSize(18)
    timeText.setSize(18)
    e.setSize(18)
    inputBox.setSize(18)
    
    a.draw(win)
    b.draw(win)
    tileText.draw(win)
    timeText.draw(win)
    e.draw(win)
    inputBox.draw(win)

# return the entry and text objects for later use (updating the text)
    return inputBox, tileText, timeText

# creates a button
def createButton(win):
    button=Rectangle(Point(3.55, 8.3), Point(3.95, 8.7))
    OK=Text(Point(3.75, 8.5), "OK")
    
    button.setFill("blue")
    OK.setSize(10)

    button.draw(win)
    OK.draw(win)
# return entry and text object for later use
    return button, OK

# creates a button the user has to press to enter their name
# inputBox is the entry box from setUpHeader, button and OK are from createButton
def getName(win, inputBox, button, OK):
    click=win.getMouse()
    x=click.getX()
    y=click.getY()
# guards against clicks not inside the button
    while not (x>3.55 and 3.95>x and y>8.3 and 8.7>y):
        click=win.getMouse()
        x=click.getX()
        y=click.getY()
    name=inputBox.getText()
# once the name is submitted removes the button, writes the name
    button.undraw()
    inputBox.undraw()
    OK.undraw()
    a=Text(Point(2.2, 8.5), name)
    a.setSize(18)
    a.draw(win)
# return name for later use
    return name

# creates a list of coordinates the mines will spawn in
# excludePoint is the first click the user inputs, prevents user losing immediately
def createTile(excludePoint):
    pointList=[excludePoint]
    tileList=[]
    k=0
    while k!=10:
# creates 10 random coordinates of x and y without any duplicates
        x=randrange(1,9)
        y=randrange(1,9)
        point="("+str(x)+","+str(y)+")"
        a=pointList.count(point)
        if a==0:
            pointList.append(point)
            tileList.append(x)
            tileList.append(y)
            k=k+1
    pointList.remove(excludePoint)
# pointList comprises 10 coordinates in point format
# tileList comprises 20 values, 10 x values and 10 y values in alternating order
# both to be used later
    return tileList, pointList

# gets the coordinates of the tile the user clicked on
def getClickPoint(win):
    clickPoint=win.checkMouse()
# if the user clicked, returns coordinates
    if clickPoint != None:
        x=int(clickPoint.getX()+1)
        y=int(clickPoint.getY()+1)
# prevents user from clicking on the header
        while y>8:
            clickPoint=win.getMouse()
            x=int(clickPoint.getX()+1)
            y=int(clickPoint.getY()+1)

        clickPoint="("+str(x)+","+str(y)+")"
# if the user did not click, returns dummy values
    else:
        clickPoint="10"
        x=10
        y=10
    return clickPoint, x, y

# gets the coordinates of the first tile the user clicks on after they enter their name
def getFirstClickPoint(win):
    clickPoint=win.getMouse()
    x=int(clickPoint.getX()+1)
    y=int(clickPoint.getY()+1)
# prevents user from clicking on the header
    while y>8:
        clickPoint=win.getMouse()
        x=int(clickPoint.getX()+1)
        y=int(clickPoint.getY()+1)

    clickPoint="("+str(x)+","+str(y)+")"
    return clickPoint, x, y  

# create Mine class
class Mine:
# x and y are natural numbers between 1 and 8, the coordinates of the center of a tile ends in .5, so adjust the values of x and y
    def __init__(self, x, y):
        self.x=x-0.5
        self.y=y-0.5
# this method draws the mine on a given tile
    def draw(self, win):
        
        circ=Circle(Point(self.x,self.y), 0.3)
        circ.setFill("black")
# the circle's radius is 0.3, and the lines protruding from the circle are 0.1 long
# a=squareroot([(0.3)^2]/2)
        a=0.21213
        b=0.31213

        line1=Line(Point(self.x,self.y+0.3), Point(self.x, self.y+0.4))
        line2=Line(Point(self.x+a,self.y+a), Point(self.x+b, self.y+b))
        line3=Line(Point(self.x+0.3,self.y), Point(self.x+0.4, self.y))
        line4=Line(Point(self.x+a,self.y-a), Point(self.x+b, self.y-b))
        line5=Line(Point(self.x,self.y-0.3), Point(self.x, self.y-0.4))
        line6=Line(Point(self.x-a,self.y-a), Point(self.x-b, self.y-b))
        line7=Line(Point(self.x-0.3,self.y), Point(self.x-0.4, self.y))
        line8=Line(Point(self.x-a,self.y+a), Point(self.x-b, self.y+b))

        line1.setWidth(3)
        line2.setWidth(3)
        line3.setWidth(3)
        line4.setWidth(3)
        line5.setWidth(3)
        line6.setWidth(3)
        line7.setWidth(3)
        line8.setWidth(3)

        circ.draw(win)
        line1.draw(win)
        line2.draw(win)
        line3.draw(win)
        line4.draw(win)
        line5.draw(win)
        line6.draw(win)
        line7.draw(win)
        line8.draw(win)

# creates mines and a list of those mines using tileList
def createMines(tileList):
    mine1=Mine(tileList[0], tileList[1])
    mine2=Mine(tileList[2], tileList[3])
    mine3=Mine(tileList[4], tileList[5])
    mine4=Mine(tileList[6], tileList[7])
    mine5=Mine(tileList[8], tileList[9])
    mine6=Mine(tileList[10], tileList[11])
    mine7=Mine(tileList[12], tileList[13])
    mine8=Mine(tileList[14], tileList[15])
    mine9=Mine(tileList[16], tileList[17])
    mine10=Mine(tileList[18], tileList[19])
    mineList=[mine1, mine2, mine3, mine4, mine5, mine6, mine7, mine8, mine9, mine10]
    return mineList

# draws the mines
def drawMines(win, mineList):
    for item in mineList:
        item.draw(win)    

# colors the tile the user clicked on white, "revealing" the tile
def revealTile(win, x, y):
    tile=Rectangle(Point(x-1, y-1), Point(x, y))
    tile.setFill("white")
    tile.draw(win)

# creates a list of the coordinates of the 8 tiles surrounding a mine using tileList
# list contains 80 points, duplicates allowed
def getNearMines(tileList):
    tileVicinityList=[]
    for k in range(10):
        x1=tileList[2*k]
        x2=tileList[2*k]+1
        x3=tileList[2*k]+1
        x4=tileList[2*k]+1
        x5=tileList[2*k]
        x6=tileList[2*k]-1
        x7=tileList[2*k]-1
        x8=tileList[2*k]-1
        y1=tileList[2*k+1]+1
        y2=tileList[2*k+1]+1
        y3=tileList[2*k+1]
        y4=tileList[2*k+1]-1
        y5=tileList[2*k+1]-1
        y6=tileList[2*k+1]-1
        y7=tileList[2*k+1]
        y8=tileList[2*k+1]+1
        p1="("+str(x1)+","+str(y1)+")"
        p2="("+str(x2)+","+str(y2)+")"
        p3="("+str(x3)+","+str(y3)+")"
        p4="("+str(x4)+","+str(y4)+")"
        p5="("+str(x5)+","+str(y5)+")"
        p6="("+str(x6)+","+str(y6)+")"
        p7="("+str(x7)+","+str(y7)+")"
        p8="("+str(x8)+","+str(y8)+")"
        tileVicinityList.append(p1)
        tileVicinityList.append(p2)
        tileVicinityList.append(p3)
        tileVicinityList.append(p4)
        tileVicinityList.append(p5)
        tileVicinityList.append(p6)
        tileVicinityList.append(p7)
        tileVicinityList.append(p8)
# tileVicinityList contains the 80 points surrounding the 10 mines, duplicates allowed
    return tileVicinityList

# point is the tile the user clicks on
# using tileVicinityList, returns the number of mines that are adjacent to the tile the user clicked on
def getNearMineCount(point, tileVicinityList):
    count=tileVicinityList.count(point)
    return count

# displays the number of adjacent mines on the tile the user clicked on
def displayNearMineCount(win, count, x, y):
    mineNumText=Text(Point(x-0.5,y-0.5), count)
    mineNumText.draw(win)

# remTile is the number of remaining safe tiles, pointList is the list of points that mines are on
# combines functions to form the primary process that will take place when a tile is clicked
def mineProcess(win, pointList, tileVicinityList, remTile):
# gets the coordinates of the tile the user clicked on
    clickPoint, x, y=getClickPoint(win)
# colors the tile white
    revealTile(win, x, y)
# checks whether clicked tile is mined
    check=pointList.count(clickPoint)
# gets the number of adjacent mines
    mineNum=getNearMineCount(clickPoint, tileVicinityList)
# displays the number of adjacent mines
    displayNearMineCount(win, mineNum, x, y)
# if the user clicked on a tile, takes one tile away from the number of remaining tiles
    if clickPoint!="10": #"10" is the dummy value for checkMouse() from before
        remTile=remTile-1
    return check, mineNum, remTile, x, y

# num is the number of remaining tiles, text is the text o bject for tiles in the header
def updateRemTiles(num, text):
    text.setText(num)

# startTime is the time main() begins at, calculates how many seconds have passed
def getElapsedTime(startTime):
    dt=1
    time.sleep(dt)
    a=int(time.time())
    b=a-startTime
    return b

# time is the number of seconds that have passed, text is the text object for time in the header
def updateElapsedTime(time, text):
    text.setText(time)

# the text that will appear if the user wins
def victoryText(win):
    message=Text(Point(4, 4.5), "You win!")
    message.setSize(36)
    message.setStyle("bold")
    message.setTextColor("blue")
    message.draw(win)

# the text that will appear if the user loses
def defeatText(win):
    message=Text(Point(4, 4.5), "You lose")
    message.setSize(36)
    message.setStyle("bold")
    message.setTextColor("red")
    message.draw(win)

# creates a text document that has the coordinates of the tiles the mines spawn on
def mineCheatSheet(win, tileList):
    outfile=open("mineCheatSheet.txt", "w")
    print("x", "y", file=outfile)
    for k in range(10):
        print(tileList[2*k], tileList[2*k+1], file=outfile)
    outfile.close()

# updates the leaderboard with the new user's information
# name is the user's name, tiles is the number of cleared tiles, sec is the number of elapsed seconds
def updateLeaderboard(name, tiles, sec):
    infile=open("leaderboard.txt", "r")
    dataList=infile.readlines()
    num=len(dataList)
# remove the "\n" from each line, add spaces between each word
    for i in range(num):
        data=dataList[i].split()
        dataString=str(data[0])+" "+str(data[1])+" "+str(data[2])
        dataList[i]=dataString
# add the user's information the the list
    newline=str(name)+" "+str(tiles)+" "+str(sec)
    dataList.append(newline)
    infile.close()
    outfile=open("leaderboard.txt", "w")
# update the file with the new list
    for k in range(num+1):
        print(dataList[k], file=outfile)
    outfile.close()

# displays the leaderboard
def displayLeaderboard(win):
# creates a blank white rectangle
    white=Rectangle(Point(1,1),Point(7,8))
    white.setFill("white")
    white.draw(win)
    name=Text(Point(2.5,7.5), "Name")
    tiles=Text(Point(4,7.5), "Tiles Cleared")
    time=Text(Point(5.5,7.5), "Seconds")
    name.draw(win)
    tiles.draw(win)
    time.draw(win)
    infile=open("leaderboard.txt","r")
    k=0.5
# prints information from file to the leaderboard
    for line in infile:
        dataList=line.split()
        name=Text(Point(2.5, 7.5-k), dataList[0])
        tiles=Text(Point(4, 7.5-k), dataList[1])
        seconds=Text(Point(5.5, 7.5-k), dataList[2])
        name.draw(win)
        tiles.draw(win)
        seconds.draw(win)
        k=k+0.5
    infile.close()

# waits for user to press button, then displays the leaderboard
# name is the user's name, tiles is the number of cleared tiles, sec is the number of elapsed seconds
def leaderboard(win, name, tiles, sec):
    box=Rectangle(Point(3,8), Point(5, 8.5))
    box.setFill("blue")
    box.draw(win)
    text=Text(Point(4,8.25), "Show History")
    text.draw(win)
    click=win.getMouse()
    x=click.getX()
    y=click.getY()
# waits for button press, if the user closes the window without pressing the button, the file is not updated and their information is not saved
    if x>3 and 5>x and y>8 and 8.5>y:
        updateLeaderboard(name, tiles, sec)
        displayLeaderboard(win)
    
def main():
# sets up graphic window, turns window into board and gets name
    win=setUpWindow()
    graphing(win)
    inputBox, remTileText, timeText=setUpHeader(win)
    button, OK=createButton(win)
    name=getName(win, inputBox, button, OK)
# get the first tile, create mines randomly excluding first tile, get starting time, create list of tiles surrounding each mine
    clickPoint, x, y=getFirstClickPoint(win)
    startTime=int(time.time())
    tileList, pointList=createTile(clickPoint)
    tileVicinityList=getNearMines(tileList)
    mineList=createMines(tileList)
# create cheat sheet
    mineCheatSheet(win, tileList)
# reveal first tile, update numbers on header
    revealTile(win, x, y)
    mineNum=getNearMineCount(clickPoint, tileVicinityList)
    displayNearMineCount(win, mineNum, x, y)
    check=pointList.count(clickPoint) #should be 0 since pointList is the list of mined tiles that the first tile is excluded from
    remTile=53
    updateRemTiles(remTile, remTileText)
# loop stops if user clicks on a mine or if there are no more safe tiles
    while check==0 and remTile!=0:
        check, mineNum, remTile, x, y=mineProcess(win, pointList, tileVicinityList, remTile)
# number of remaining tiles go down if the mouse is clicked, time goes up regardless of click
        updateRemTiles(remTile, remTileText)
        curTime=getElapsedTime(startTime)
        updateElapsedTime(curTime, timeText)
# victory condition: if there are no more safe tiles
    if remTile==0:
        victoryText(win)
        leaderboard(win, name, remTile, curTime)
# defeat condition: if the loop ends while safe tiles remain (so the user must have clicked on a mine)
    if remTile!=0:
        defeatText(win)
        drawMines(win, mineList)
        leaderboard(win, name, 53-remTile, curTime)


        

main()

