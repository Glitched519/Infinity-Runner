#Imports and setups for the game
from tkinter import *
from math import *
from time import *
from random import *
try:    #If winsound cannot load because that package doesn't exist, it will be mentioned in the console
    from winsound import *
except ImportError:
    print("Failed to load winsound.")

root = Tk()
themeOfDay = ["skyblue", "midnight blue", "deep sky blue", "blue", "light sky blue"]
s = Canvas(root, width=1000, height=600, background=choice(themeOfDay))
root.attributes("-topmost", 1)
root.resizable(0, 0)
root.title("∞ Runner")




 #Initializes all of the variables need and their values and assignments
def setInitialValues():
    global gameMode, gameIsRunning, mouseX, mouseY, runnerGIF, score, time, obstacles, kickImage
    global jumpObstacle, ramObstacle, xObstacle1, yObstacle1, jumpImage, rdmFreq, score, scoreString
    global xObstacle2, yObstacle2, obstaclesX, obstaclesY, obstacleDrawings, runner, runnerImage, startTime
    global Frame, runnerX, runnerY, ySpeed, gravity, airborne, base, ground, kicking, crystalActive, clock, n
    xObstacle1 = 500
    yObstacle1 = 500
    xObstacle2 = 500
    yObstacle2 = 460
    runnerY = 480
    runnerX = 200
    ySpeed = 0
    gravity = 1
    score = 0
    base = 470
    jumpObstacle = PhotoImage(file="spike bush.gif")
    ramObstacle = PhotoImage(file="crystal.gif")
    ramObstacleBroken = PhotoImage(file="crystal broken.gif")
    jumpImage = PhotoImage(file="running/jump.gif")
    kickImage = PhotoImage(file="running/kicking.gif")
    runner = []
    runnerImage = []
    obstaclesX = []
    obstaclesY = []
    obstacleDrawings = [1]*200
    Frame = 0
    airborne = False
    kicking = False
    gameIsRunning = False
    gameMode = "play Normal"
    crystalActive = True
    gameOver = False
    ground = 0
    clock = 0
    n = 2

    #Appends the series of .gif runner images and loops then into an animation
    for x in range(6):
        runner.append(PhotoImage(file="running/running"+str(x)+".gif"))
        runnerImage.append(0)

    #Appends and random location for the obstacles
    for i in range(n):
        obstaclesX.append(randint(500,600))
        obstaclesX.append(randint(700, 800))
        n += 1
#Makes the runner run
def updateRunnerPosition():
    global runnerY, ySpeed, airborne
    runnerY += ySpeed

    if airborne == True: #If the runner is in the air from the jump
        runnerY += ySpeed
        ySpeed += gravity

        if runnerY > base:  #If the runner is above the ground
            airborne = False
            ySpeed = 0

#Draws the objects on the screen and sets the effects on them based on the conditions met
def drawObjects():
    global broken, ramObstacleBroken, crystalActive
    ramObstacleBroken = PhotoImage(file="crystal broken.gif")
    for i in range(1):
        obstacleDrawings[i] = s.create_image(obstaclesX[0], yObstacle1, image=jumpObstacle, anchor=CENTER)
        if crystalActive == True:
            obstacleDrawings[i+1] = s.create_image(obstaclesX[1], yObstacle2, image=ramObstacle, anchor=CENTER)
        if airborne == False:
            runnerImage[Frame] = s.create_image(runnerX, runnerY, image = runner[Frame])
        elif kicking == True and runnerX > obstaclesX[1] - 72 and runnerX < obstaclesX[1] + 72:
            runnerImage[Frame] = s.create_image(runnerX, runnerY, image = kickImage)
            broken = s.create_image(obstaclesX[1], 500, image=ramObstacleBroken)
        else:
            runnerImage[Frame] = s.create_image(runnerX, runnerY, image = jumpImage)

def endScreen():
    global score, runWasEndedBy, gameMode, retryButton, gameOverText, endingMsg, finalScore, finalTime
    endingMsg = ["Game Over!", "OOF!", "Ouched!", "Welp!", "Hertz!", "Wasted!"]
    if gameMode == "gameOver":        
        if runnerX > obstaclesX[0] - 48 and runnerX < obstaclesX[0] + 48:
            score = score
            gameOverText = s.create_text(500, 300, text=endingMsg[randint(0, 5)], font="Impact 72", anchor=CENTER)
            runWasEndedBy = s.create_text(500, 360, text="Your run was ended by a spike bush.", font="Impact 24", anchor=CENTER)
            finalScore = s.create_text(350, 390, text="Your final score is "+str(score), font="Impact 18", anchor=CENTER)
            finalTime = s.create_text(650, 390, text="Your final time is "+str(round(clock,2)), font="Impact 18", anchor=CENTER)
            retryButton = Button(root, text="Retry?", font="Impact 36", command = retry, anchor=CENTER)
            retryButton.pack()
            retryButton.place(x=500, y=50, width=250, height=60, anchor=CENTER)
        elif kicking == False and runnerX > obstaclesX[1] - 72 and runnerX < obstaclesX[1] + 72:
            score = score
            gameOverText = s.create_text(500, 300, text=endingMsg[randint(0, 5)], font="Impact 72", anchor=CENTER)
            runWasEndedBy = s.create_text(500, 360, text="Your run was ended by a crystal.", font="Impact 24", anchor=CENTER)
            finalScore = s.create_text(350, 390, text="Your final score is "+str(score), font="Impact 18", anchor=CENTER)
            finalTime = s.create_text(650, 390, text="Your final time is "+str(clock), font="Impact 18", anchor=CENTER)
            retryButton = Button(root, text="Retry?", font="Impact 36", command = retry, anchor=CENTER)
            retryButton.pack()
            retryButton.place(x=500, y=50, width=250, height=60, anchor=CENTER)
        stop()

def stop():
    global Frame, score, clock, runWasEndedBy, gameMode
    if gameMove == "gameOver":  #WARNING: This will output an error to the console, but the game will still continue to run whatsoever
        obstaclesX[0] += 10
        obstaclesX[1] += 10
        Frame -= 1
        score -= 1
        clock -= time()/30000000000
        sleep(1)
        s.delete(runWasEndedBy)

def retry():
    global runWasEndedBy, score, clock, retryButton, gameOverText, finalTime, finalScore
    s.delete(runWasEndedBy, gameOverText, finalTime, finalScore)
    retryButton.destroy()
    score = 0
    clock = 0    
    runGame()
    
#Detects for any collisions made runner - obstacle
def checkForCollisions():
    global score, gameMode, crystalActive        
    ramObstacleBroken = PhotoImage(file="crystal broken.gif")
    if runnerX > obstaclesX[0] - 48 and runnerX < obstaclesX[0] + 48:
        if runnerY -10 > yObstacle1  - 48:
            gameMode = "gameOver"
            
    elif runnerX > obstaclesX[0] - 48 and runnerX < obstaclesX[0] + 48  and runnerY < base:
        score += 40
    if kicking == True and airborne == True and runnerX > obstaclesX[1] - 72 and runnerX < obstaclesX[1] + 72:
        crystalActive = False
        broken = s.create_image(obstaclesX[1], yObstacle2, image=ramObstacleBroken, anchor=CENTER)
        ramObstacle  = broken
        score += 60 
    elif airborne == False and kicking == True and runnerX > obstaclesX[1] - 72 and runnerX < obstaclesX[1] + 72:
        crystalActive = False
        broken = s.create_image(obstaclesX[1], yObstacle2, image=ramObstacleBroken, anchor=CENTER)
        ramObstacle  = broken
    elif kicking == False and runnerX > obstaclesX[1] - 72 and runnerX < obstaclesX[1] + 72:
        endScreen()
        broken = s.create_image(obstaclesX[1], yObstacle2, image=ramObstacleBroken, anchor=CENTER)
        ramObstacle  = broken
        gameMode = "gameOver"

#First screen that appears on the startup of the game
def drawIntroScreen():
    global playButton, instructionsButton, gameMode, instructions, title, titleColours
    titleColours = ["white", "yellow", "green", "purple", "red", "blue"]
    gameMode = "intro"
    for b in range(6):
       s.create_rectangle(0, 100*b, 1000, 100*(b+1), fill=titleColours[b], outline=titleColours[b])
    title = s.create_text(500, 150, text="∞ RUNNER ", font="Impact 96", anchor=CENTER, fill="black")
    instructionsButton = Button(root, text="⇢ How To Play ⇠", font="Impact 36", bg=choice(titleColours), command = instructions, anchor=CENTER,)
    instructionsButton.pack()
    
    instructionsButton.place(x=500, y=300, width=400, height=80, anchor=CENTER)
    s.delete(instructions)
    try:
        PlaySound('InfoChase.wav', SND_ALIAS | SND_ASYNC | SND_LOOP)
    except NameError:
        print("Could not play sound because winsound failed to load.")

    gameMode = "intro"

#Starts the game and cleans up the instructions screen
def pressPlay():
    global playNormalButton, playHardButton, startButton, instructionsButton, gameMode, instructions, instructions2, instructions3, instructions4, instructions5, jumpRunner, kickRunner, gameOver
    gameOver = s.create_text(500, 300, font="Impact 72", text="", anchor=CENTER)
    playNormalButton.destroy()
    playHardButton.destroy()
    startButton.destroy()
    instructionsButton.destroy()
    s.delete(instructions, instructions2, instructions3, instructions4, instructions5, kickRunner, jumpRunner, gameOver)

    try:
        PlaySound('BlackoutCity.wav', SND_ALIAS | SND_ASYNC | SND_LOOP)
    except NameError:
        print("Could not play sound because winsound failed to load.")
    runGame()

#Brings you over to the instructions screen and cleans up the intro screen
def instructions():
    global playNormalButton, playHardButton, startButton, instructionsButton, gameMode, instructions, instructions2, instructions3, instructions4, instructions5, title, bush, crystal, jumpObstacle, ramObstacle, jumpRunner, kickRunner, jump, kick
    instructionsButton.destroy()
    jumpObstacle = PhotoImage(file="spike bush.gif")
    ramObstacle = PhotoImage(file="crystal.gif")
    jump = PhotoImage(file="running/jump.gif")
    kick = PhotoImage(file="running/kicking.gif")
    instructions = s.create_text(10, 250, text="Infinite Runner is an endless running game where you have to last as long as possible. ", font="Impact 18", anchor=W)
    instructions2 = s.create_text(10, 280, text="The controls for the game are fairly easily to memorize. Press left click to jump over a spike bush.", font="Impact 18", anchor=W)
    instructions3 = s.create_text(10, 310, text="Press right click to activate kick to break the crystal.", font="Impact 18", anchor=W)
    instructions4 = s.create_text(10, 370, text="Good luck and try to last as long as possible.", font="Impact 18", anchor=W)
    instructions5= s.create_text(10, 340, text="Your score at the top will tell you how many frames you've lasted. Every 30 frames is one second.", font="Impact 18", anchor=W)
    jumpRunner = s.create_image(300, 470, image=jump, anchor=CENTER)
    kickRunner = s.create_image(600, 500, image=kick, anchor=CENTER)
    playNormalButton = Button(root, text="Play it Normal", font="Impact 30", bg= "green", command = playNormal(), anchor=CENTER)
    playHardButton = Button(root, text="Play it Hard", font="Impact 30", bg= "red", command = playHard, anchor=CENTER)
    startButton = Button(root, text="Start", font="Impact 30", bg= "light green", command = pressPlay, anchor=CENTER)
    bush = s.create_image(300, 550, image=jumpObstacle, anchor=CENTER)
    crystal = s.create_image(700, 520, image=ramObstacle, anchor=CENTER)
    playNormalButton.pack()
    playHardButton.pack()
    startButton.pack()
    playNormalButton.place(x=500, y=40, width=300, height=60, anchor=CENTER)
    playHardButton.place(x=500, y=115, width=300, height=60, anchor=CENTER)
    startButton.place(x=500, y=190, width=200, height=60, anchor=CENTER)
    s.delete(title)
    s.update()

#Gets the obstacles moving
def updateObjects():
    global xObstacle1, yObstacle1, xObstacle2, yObstacle2, crystalActive, n
    gameIsRunning = True
    if gameMode == "play Normal":
        if gameIsRunning == True:
            obstaclesX[0] -= 10
            obstaclesX[1] -= 10
            if obstaclesX[0] < randint(-150, -80):
                obstaclesX[0] = 1100
                crystalActive = True
            if obstaclesX[1] < randint(-150, -80):
                obstaclesX[1] = 1150
                crystalActive = True
    elif gameMode == "play Hard":
        if gameIsRunning == True:
            obstaclesX[0] -= 20
            obstaclesX[1] -= 20
            if obstaclesX[0] < randint(-150, -80):
                obstaclesX[0] = 1100
                crystalActive = True
            if obstaclesX[1] < randint(-150, -80):
                obstaclesX[1] = 1150
                crystalActive = True
    elif gameMode == "intro":
        gameIsRunning = False
        obstaclesX[0] -= 0
        obstaclesX[1] -= 0

#Press left click to jump
def mouseLeftClickHandler(event):
    global ySpeed, airborne, gameMode, gameIsRunning
    if gameMode == "play Normal" or gameMode == "play Hard":
        gameIsRunning = True
        if gameIsRunning == True:
            if airborne == False:
                ySpeed = -10

            airborne = True
    elif gameMode == "intro":
        pass

def playNormal():
    gameMode = "play Normal"

def playHard():
    gameMode = "play Hard"

#Press right click at the right time to kick
def mouseRightClickHandler(event):
    global gameMode, gameIsRunning, kicking
    if gameMode == "play Normal" or gameMode == "play Hard":
        gameIsRunning = True
        if gameIsRunning == True:
            kicking = True
    elif gameMode == "intro":
        pass

def keyDownHandler(event):
    pass

def keyUpHandler(event):
    pass

#Shows the score at the top-left corner
def showScore():
    global scoreString
    scoreString = s.create_text(10, 10, text="Score: "+str(score), font="Impact 24", anchor=NW)

#Shows the clock at the top right corner
def showClock():
    global clockString
    clockString = s.create_text(990, 10, text="Time: "+str(round(clock, 2)), font="Impact 24", anchor=NE)

#Runes the entire game by calling out all procedures
def runGame():
    global Frame, runnerImage, runnerY, ground, gameMode, score, clock, scoreString, clockString, gameMode, ground
    setInitialValues()
    
    while 1:
        while gameMode == "play Normal"or gameMode == "play Hard":
            ground = s.create_rectangle(0, 530, 1000, 600, fill="green", outline="green")
            if Frame == 6:
                Frame = 0
            drawObjects()
            showScore()
            showClock()
            s.update()
            sleep(1/30)
            s.delete(runnerImage[Frame], scoreString, clockString, ground)
            Frame += 1
            score += 1
            clock += time()/30000000000

            for i in range(len(obstacleDrawings)):
                s.delete(obstacleDrawings[i])

            updateObjects()
            updateRunnerPosition()
            checkForCollisions()
            s.delete(scoreString, clockString, score, clock)
        while gameMode == "gameOver":
            s.delete(scoreString, clockString)
            endScreen()
    
        
root.after( 0, drawIntroScreen )

#Keys are binded to their specific functions
s.bind_all( "<Button-1>", mouseLeftClickHandler )
s.bind_all( "<KeyPress>", keyDownHandler )
s.bind_all( "<KeyRelease>", keyUpHandler )
s.bind_all( "<Button-3>", mouseRightClickHandler )


s.pack()
s.focus_set()

