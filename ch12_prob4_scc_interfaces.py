# Chapter 12, Problem 4 — Ship, Captain, and Crew With Textual and

import random
from graphics import *

class Die:

    def __init__(self):
        self.value = 0
        self.held = False

    def roll(self):
        if not self.held:
            self.value = random.randint(1, 6)
        return self.value

    def hold(self):
        self.held = True

    def isHeld(self):
        return self.held

    def reset(self):
        self.value = 0
        self.held = False


class DiceHand:

    def __init__(self, numDice):
        self.dice = []
        i = 0
        while i < numDice:
            self.dice.append(Die())
            i = i + 1

    def rollAll(self):
        i = 0
        while i < len(self.dice):
            self.dice[i].roll()
            i = i + 1

    def resetAll(self):
        i = 0
        while i < len(self.dice):
            self.dice[i].reset()
            i = i + 1

    def getValues(self):
        values = []
        i = 0
        while i < len(self.dice):
            values.append(self.dice[i].value)
            i = i + 1
        return values


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = DiceHand(5)
        self.hasShip = False
        self.hasCaptain = False
        self.hasCrew = False
        self.score = 0

    def resetForTurn(self):
        self.hand.resetAll()
        self.hasShip = False
        self.hasCaptain = False
        self.hasCrew = False
        self.score = 0

    def holdMatches(self, targetValue):
        dice = self.hand.dice
        i = 0
        found = False
        while i < len(dice) and not found:
            if not dice[i].isHeld() and dice[i].value == targetValue:
                dice[i].hold()
                found = True
            i = i + 1
        return found

    def processRoll(self):
        if not self.hasShip:
            if self.holdMatches(6):
                self.hasShip = True
        if self.hasShip and not self.hasCaptain:
            if self.holdMatches(5):
                self.hasCaptain = True
        if self.hasCaptain and not self.hasCrew:
            if self.holdMatches(4):
                self.hasCrew = True

    def cargoScore(self):
        total = 0
        dice = self.hand.dice
        i = 0
        while i < len(dice):
            if not dice[i].isHeld():
                total = total + dice[i].value
            i = i + 1
        return total


class TextInterface:

    def getNumPlayers(self):
        return int(input("Enter the number of players (2 or more): "))

    def getPlayerName(self, index):
        return input("Enter name for player " + str(index + 1) + ": ")

    def showMessage(self, text):
        print(text)

    def showRoll(self, playerName, rollNum, values):
        print("  Roll", rollNum, ":", values)

    def showScore(self, playerName, score):
        print(playerName, "scores", score)

    def showWinner(self, name, score):
        print()
        print(name, "wins the game with a score of", score, "!")


class GraphicalInterface:

    def __init__(self):
        self.win = GraphWin("Ship, Captain, and Crew", 600, 300)
        self.win.setBackground("lightyellow")
        self.status = Text(Point(300, 30), "Click anywhere to advance each roll")
        self.status.draw(self.win)
        self.line1 = Text(Point(300, 100), "")
        self.line1.setSize(14)
        self.line1.draw(self.win)
        self.line2 = Text(Point(300, 140), "")
        self.line2.setSize(14)
        self.line2.draw(self.win)

    def getNumPlayers(self):
        return int(input("Enter the number of players (2 or more): "))

    def getPlayerName(self, index):
        return input("Enter name for player " + str(index + 1) + ": ")

    def showMessage(self, text):
        self.line1.setText(text)
        print(text)

    def showRoll(self, playerName, rollNum, values):
        self.line1.setText(playerName + " -- roll " + str(rollNum))
        self.line2.setText(str(values))
        self.win.getMouse()

    def showScore(self, playerName, score):
        self.line1.setText(playerName + " scores " + str(score))
        self.line2.setText("")
        self.win.getMouse()

    def showWinner(self, name, score):
        self.line1.setText(name + " wins with a score of " + str(score) + "!")
        self.line2.setText("Click to exit.")
        self.win.getMouse()
        self.win.close()


def takeTurn(player, interface):
    player.resetForTurn()

    rollNum = 1
    while rollNum <= 3:
        player.hand.rollAll()
        interface.showRoll(player.name, rollNum, player.hand.getValues())
        player.processRoll()

        if player.hasShip and player.hasCaptain and player.hasCrew:
            player.score = player.cargoScore()
            interface.showMessage("Ship, captain, and crew complete -- cargo score is " + str(player.score))

        rollNum = rollNum + 1

    if not (player.hasShip and player.hasCaptain and player.hasCrew):
        player.score = 0
        interface.showMessage("Did not roll a ship, captain, and crew in 3 rolls -- score is 0")


class Game:

    def __init__(self, interface):
        self.interface = interface
        numPlayers = interface.getNumPlayers()

        self.players = []
        i = 0
        while i < numPlayers:
            name = interface.getPlayerName(i)
            self.players.append(Player(name))
            i = i + 1

    def playRound(self, contenders):
        i = 0
        while i < len(contenders):
            self.interface.showMessage(contenders[i].name + " is rolling...")
            takeTurn(contenders[i], self.interface)
            self.interface.showScore(contenders[i].name, contenders[i].score)
            i = i + 1

    def playGame(self):
        self.interface.showMessage("Starting Ship, Captain, and Crew with " + str(len(self.players)) + " players.")

        contenders = self.players
        winner = None

        while winner is None:
            self.playRound(contenders)

            highScore = -1
            i = 0
            while i < len(contenders):
                if contenders[i].score > highScore:
                    highScore = contenders[i].score
                i = i + 1

            tied = []
            i = 0
            while i < len(contenders):
                if contenders[i].score == highScore:
                    tied.append(contenders[i])
                i = i + 1

            if len(tied) == 1:
                winner = tied[0]
            else:
                names = ""
                i = 0
                while i < len(tied):
                    names = names + tied[i].name
                    if i < len(tied) - 1:
                        names = names + ", "
                    i = i + 1
                self.interface.showMessage("Tie at " + str(highScore) + " points between: " + names + " -- rolling again.")
                contenders = tied

        self.interface.showWinner(winner.name, winner.score)


def main():
    choice = input("Play with a (t)ext or (g)raphical interface? ")

    if choice.lower().startswith("g"):
        interface = GraphicalInterface()
    else:
        interface = TextInterface()

    game = Game(interface)
    game.playGame()

main()
