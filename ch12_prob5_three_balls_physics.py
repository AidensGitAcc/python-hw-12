# Chapter 12, Problem 5 — Three Bouncing Balls With Real Physics

from graphics import *
import time

GRAVITY = -9.8
RESTITUTION = 0.7
TIME_STEP = 0.03


class Button:

    def __init__(self, win, center, width, height, label):
        halfWidth = width / 2.0
        halfHeight = height / 2.0
        x = center.getX()
        y = center.getY()
        p1 = Point(x - halfWidth, y - halfHeight)
        p2 = Point(x + halfWidth, y + halfHeight)

        self.rectangle = Rectangle(p1, p2)
        self.rectangle.setFill("lightblue")
        self.rectangle.draw(win)

        self.labelText = Text(center, label)
        self.labelText.draw(win)

        self.xMin = p1.getX()
        self.xMax = p2.getX()
        self.yMin = p1.getY()
        self.yMax = p2.getY()

    def clicked(self, point):
        x = point.getX()
        y = point.getY()
        return self.xMin <= x <= self.xMax and self.yMin <= y <= self.yMax


class Ball:

    def __init__(self, xFraction, height, color):
        self.xFraction = xFraction
        self.height = height
        self.vy = 0.0
        self.color = color
        self.circle = None

    def update(self, dt):
        self.vy = self.vy + GRAVITY * dt
        self.height = self.height + self.vy * dt
        if self.height <= 0:
            self.height = 0
            self.vy = -self.vy * RESTITUTION

    def isSettled(self):
        return self.height < 0.001 and abs(self.vy) < 0.05

    def draw(self, win, maxHeight, radius):
        normalizedY = self.height / maxHeight
        self.circle = Circle(Point(self.xFraction, normalizedY), radius)
        self.circle.setFill(self.color)
        self.circle.setOutline("black")
        self.circle.draw(win)

    def moveTo(self, maxHeight):
        normalizedY = self.height / maxHeight
        dy = normalizedY - self.circle.getCenter().getY()
        self.circle.move(0, dy)


def getHeightsFromInputWindow():
    win = GraphWin("Enter Release Heights", 400, 400)
    win.setBackground("lightyellow")

    prompt1 = Text(Point(200, 60), "Height for ball 1 (m):")
    prompt1.draw(win)
    entry1 = Entry(Point(200, 90), 6)
    entry1.draw(win)

    prompt2 = Text(Point(200, 150), "Height for ball 2 (m):")
    prompt2.draw(win)
    entry2 = Entry(Point(200, 180), 6)
    entry2.draw(win)

    prompt3 = Text(Point(200, 240), "Height for ball 3 (m):")
    prompt3.draw(win)
    entry3 = Entry(Point(200, 270), 6)
    entry3.draw(win)

    startButton = Button(win, Point(200, 340), 100, 40, "Start")

    clickedStart = False
    while not clickedStart:
        click = win.getMouse()
        clickedStart = startButton.clicked(click)

    height1 = float(entry1.getText())
    height2 = float(entry2.getText())
    height3 = float(entry3.getText())

    win.close()
    return height1, height2, height3


def main():
    height1, height2, height3 = getHeightsFromInputWindow()

    maxHeight = height1
    if height2 > maxHeight:
        maxHeight = height2
    if height3 > maxHeight:
        maxHeight = height3

    balls = []
    balls.append(Ball(0.2, height1, "tomato"))
    balls.append(Ball(0.5, height2, "mediumseagreen"))
    balls.append(Ball(0.8, height3, "cornflowerblue"))

    win = GraphWin("Three Bouncing Balls (Real Physics)", 600, 600)
    win.setBackground("white")
    win.setCoords(0, -0.05, 1, 1.05)

    radius = 0.03
    i = 0
    while i < len(balls):
        balls[i].draw(win, maxHeight, radius)
        i = i + 1

    anyMoving = True
    while anyMoving:
        anyMoving = False
        i = 0
        while i < len(balls):
            balls[i].update(TIME_STEP)
            balls[i].moveTo(maxHeight)
            if not balls[i].isSettled():
                anyMoving = True
            i = i + 1
        time.sleep(TIME_STEP)

    done = Text(Point(0.5, 0.95), "Done! Click to exit.")
    done.draw(win)
    win.getMouse()
    win.close()

main()
